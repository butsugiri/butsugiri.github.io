"""Check generated HTML metadata, disclosure content, and local resources."""

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import sys


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.references = []
        self.metadata = {}
        self.stack = []
        self.abstracts = []
        self.current_abstract = None
        self.in_summary = False
        self.errors = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            if attrs["id"] in self.ids:
                self.errors.append(f"Duplicate ID: {attrs['id']}")
            self.ids.add(attrs["id"])
        for attr in ("href", "src"):
            if attrs.get(attr):
                self.references.append(attrs[attr])
        if tag == "meta":
            for attr in ("name", "property"):
                if attrs.get(attr):
                    self.metadata[attrs[attr]] = attrs.get("content")
        if tag == "link" and attrs.get("rel") == "canonical":
            self.metadata["canonical"] = attrs.get("href")
        if tag in ("a", "button"):
            if self.stack:
                self.errors.append("Nested interactive link/button")
            self.stack.append(tag)
        if tag == "details" and "publication-abstract" in attrs.get("class", "").split():
            self.current_abstract = []
        if tag == "summary":
            self.in_summary = True

    def handle_endtag(self, tag):
        if tag in ("a", "button") and self.stack:
            self.stack.pop()
        if tag == "summary":
            self.in_summary = False
        if tag == "details" and self.current_abstract is not None:
            self.abstracts.append("".join(self.current_abstract).strip())
            self.current_abstract = None

    def handle_data(self, data):
        if self.current_abstract is not None and not self.in_summary:
            self.current_abstract.append(data)


def check(root):
    pages = {}
    errors = []
    for path in root.rglob("*.html"):
        page = Page()
        page.feed(path.read_text(encoding="utf-8"))
        pages[path.resolve()] = page
        errors.extend(f"{path}: {error}" for error in page.errors)
        for abstract in page.abstracts:
            if not abstract:
                errors.append(f"{path}: Empty abstract disclosure")
    assert pages, f"No generated HTML found in {root}"
    home = pages[(root / "index.html").resolve()]
    for key in ("description", "og:title", "og:description", "og:url", "canonical"):
        if not home.metadata.get(key):
            errors.append(f"Missing homepage metadata: {key}")
    if home.metadata.get("canonical") != "https://butsugiri.github.io/":
        errors.append("Incorrect production canonical URL")
    if home.metadata.get("author") != "Shun Kiyono":
        errors.append("Incorrect homepage author")
    if home.metadata.get("twitter:creator") != "@shunkiyono":
        errors.append("Incorrect Twitter creator")
    if not home.abstracts:
        errors.append("No abstract disclosures rendered")
    for path, page in pages.items():
        for reference in page.references:
            url = urlsplit(reference)
            if url.scheme or url.netloc:
                continue
            target = ((root / unquote(url.path).lstrip("/")) if url.path.startswith("/")
                      else path.parent / unquote(url.path)) if url.path else path
            if target.is_dir():
                target /= "index.html"
            if not target.exists():
                errors.append(f"{path}: Missing local resource: {reference}")
            elif url.fragment and target.resolve() in pages:
                if unquote(url.fragment) not in pages[target.resolve()].ids:
                    errors.append(f"{path}: Missing fragment: {reference}")
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"Checked {len(pages)} HTML page(s): metadata, abstracts, links and local resources OK")


if __name__ == "__main__":
    check(Path(sys.argv[1] if len(sys.argv) > 1 else "my-blog/_site").resolve())
