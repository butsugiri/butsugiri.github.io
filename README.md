# butsugiri.github.io

A Jekyll site for Shun Kiyono's profile and publications.
Published at https://butsugiri.github.io.

## Development

Start Docker, then run these commands from the repository root.
You do not need to install Ruby on the host.

```sh
docker compose build
docker compose up
```

Open http://localhost:4000. LiveReload uses port 35729.
Restart the server after changing the configuration file.

## Build validation

```sh
docker compose run --rm -e JEKYLL_ENV=production service_jekyll bundle exec jekyll build --trace
python3 scripts/check_site.py
```

Generated files are written to `my-blog/_site/` and are excluded from Git.
CI validates the Docker build and generated HTML for pull requests targeting any branch
and for pushes to main. The HTML checker verifies abstract content, metadata, local
resources, and fragment targets using only the Python 3 standard library.
CI caches Docker layers, including installed gems, between runs. After validation
succeeds on main, the generated site is passed to the deployment job as an artifact
and published to the gh-pages branch without rebuilding. GitHub Pages uses the root
of that branch as its publishing source.

## Content updates

- `my-blog/index.md`: career, education, and activities
- `my-blog/_bibliography/*.bib`: publication metadata
- `my-blog/repository/`: paper, slide, and poster PDFs
- `my-blog/_data/menu.yml`: homepage section navigation
- `my-blog/_config.yml`: production URL, author, SEO, and theme settings

A publication's `url` is labeled PDF when its path ends in `.pdf`, and Paper otherwise.
The `slide`, `poster`, and `spotlight` fields appear as separate resource links.
Use `/repository/filename.pdf` for local resources.
Set `abstract` to display the abstract in an expandable disclosure.

## Updating gems and Ruby

Always update `Gemfile.lock` inside the Linux container.

```sh
docker compose run --rm service_jekyll bundle update
docker compose build
docker compose run --rm -e JEKYLL_ENV=production service_jekyll bundle exec jekyll build --trace
```

When updating Ruby, change Dockerfile, then follow the same update procedure.
CI uses the same Dockerfile. See [AGENTS.md](AGENTS.md) for the project rules.

## Legacy site

`obsolete/` preserves the previous Python-based site and is excluded from the current
build and deployment. Keep the archived materials for historical reference; PDFs
linked from the current publication list are also stored in `my-blog/repository/`.
The Docker build context includes only Dockerfile, Gemfile, and the lockfile.
