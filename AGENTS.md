# Curiosophy: instructions for AI assistants

Curiosophy is the author's public learning notebook, published at https://iammohithhh.github.io/Curiosophy.
The author sends notes, links, screenshots or dictation (often from a phone), or writes Markdown in Obsidian.
Your job is to turn that into clean, honest pages.

## Layout
- `content/`: the site. It's also an Obsidian vault.
  - `challenge/`: the Discovered Materials Speed–Accuracy Barrier challenge. `index.md` is the main write-up.
    Add subpages only when the author asks, and link them from the write-up.
  - `papers/`: one page per paper, for skimming instead of rereading. Sections: TL;DR, the problem, the key idea,
    how it works, results that matter, limitations, my take.
  - `learnings/`: anything else the author learns.
  - `images/`: all images. Embed them with `![[file.png]]`.
- `site/`: site settings (`quartz.config.yaml`) and `build.sh`, which downloads Quartz at build time.
  Never add Quartz's own files to this repo. Don't change site settings unless asked.
- Quartz lists a folder's pages automatically, so don't maintain lists by hand.

## Writing pages
- File names in kebab-case. Frontmatter: `title`, `date`, and `tags` where useful.
- Keep the author's ideas, examples and framing. Improve clarity, structure and math (KaTeX: `$...$`, `$$...$$`).
  Don't pad pages with textbook material the author didn't ask for.
- Link related pages with `[[wikilinks]]`.
- Only cite sources you've verified exist (DOI or arXiv link). Never invent references.
- End pages you write with a `> [!todo] Things to check` callout listing claims the author should verify.
- Never add PDFs of papers or long copied passages, and never put the author's private details in pages.
- Run `site/build.sh` and fix any errors before reporting back.

## Publishing
Don't commit or push unless the author asks. When they say "publish", commit with a short message and push to `main`,
which deploys the site. If only a branch push is allowed, push the branch, open a pull request and ask them to merge it.
