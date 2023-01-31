# -*- coding: utf-8 -*-
import bibtexparser
from jinja2 import Environment, FileSystemLoader, select_autoescape


def sanitize_author(names: str, domestic: bool = False) -> str:
    names: list = names.split('and')
    if domestic:
        author_str: str = ', '.join([' '.join([i.strip() for i in n.split(',')]) for n in names])
    else:
        author_str: str = ', '.join([' '.join([i.strip() for i in n.split(',')][::-1]) for n in names])

    return author_str


def main() -> None:
    env = Environment(
        loader=FileSystemLoader('template'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('index.html')

    # publications
    bib_database = bibtexparser.load(open('references.bib'))

    journal: list = []
    international_conference: list = []
    domestic_conference: list = []
    preprint: list = []
    others: list = []
    for entry in bib_database.entries:
        if entry['type'] == 'journal':
            entry['author'] = sanitize_author(entry['author'], domestic=False)
            journal.append(entry)
        if entry['type'] == 'international_conference':
            entry['author'] = sanitize_author(entry['author'], domestic=False)
            international_conference.append(entry)
        elif entry['type'] == 'domestic_conference':
            entry['author'] = sanitize_author(entry['author'], domestic=True)
            domestic_conference.append(entry)
        elif entry['type'] == 'preprint':
            entry['author'] = sanitize_author(entry['author'], domestic=False)
            preprint.append(entry)
        elif entry['type'] == 'others':
            entry['author'] = sanitize_author(entry['author'], domestic=True)
            others.append(entry)

    # TODO: awards, activities...?

    html: str = template.render(
        journal=journal,
        international_conference=international_conference,
        domestic_conference=domestic_conference,
        preprint=preprint,
        others=others
    )
    print(html)


if __name__ == "__main__":
    main()
