# Divy — public journey portfolio

A real static portfolio inspired by the **four uploaded .dc.html reference pages**. Uses the same JetBrains Mono + IBM Plex Sans terminal feel, deep near-black navy surfaces, amber `#FFB454`, restrained borders, status panel, numbered sections, and case-file format. The generated `site/` folder works on GitHub Pages, Netlify, or Vercel (static hosting). No React, server, database, account, or monthly CMS subscription needed.

## Open the website

Run `python build.py`, then open `site/index.html` in a browser. Pages work locally without a development server (Google Fonts need internet access).

## Publish a journal entry — exact workflow

1. Go to the **`posts/`** folder.
2. Copy `POST-TEMPLATE.md` to a new file named like `2026-10-25-first-siem-lab.md`. **Do not edit the original template.**
3. Change `title`, `date` (YYYY-MM-DD), `category`, and `summary` at the top. Set **`draft: false`** once ready to publish.
4. Write your article under the second `---` using Markdown: `## Heading`, `**bold**`, `- list`, fenced triple-backtick code, and `[link](https://...)`.
5. Run **`python build.py`** from this folder. It rebuilds the homepage latest entries, journal index, and individual article pages automatically. Posts are sorted newest-first.
6. Push the rebuilt `site/` folder to your website host. If you deploy the whole repository with Vercel or Netlify, configure the output/publish directory as **`site`** and build command as **`python build.py`**. For GitHub Pages, use the included Actions workflow (push repo to GitHub; Settings → Pages → Source: GitHub Actions).

**Example:** `posts/2026-10-26-learning-sysmon.md` becomes `site/journal/2026-10-26-learning-sysmon.html`. You do **not** need to edit links in the homepage manually.

**Draft control:** `draft: true` entries do not appear anywhere. The included opening entry is sample copy, not a claim that you've already written it; rewrite it before deploying publicly.

**Local Windows:** Open PowerShell in this folder and run `py build.py` if `python` is not recognized.

## Change your site details

- **Your intro, status, roadmap, projects, and contact:** edit the clearly labeled `hero`, `status`, `projects`, `about` and `detections` sections in `build.py`, then rebuild.
- **Fonts/colors/layout:** `assets/style.css`. Main colors are `--bg`, `--surface`, `--amber`, and `--text` at top.
- **New everyday entries:** only `posts/*.md`. No other file needs editing.
- **Project URLs:** the `projects` list in `build.py`.
- **LinkedIn/email:** `about` HTML near the bottom of `build.py` (not filled in because addresses weren't provided).

## Suggested categories

`journey`, `learning`, `cybersecurity`, `detection`, `projects`, `career`, `reflection` — free-form labels; use any category you want.

## What is not included

There's no private web admin login, comments system, database, rich text editor, or upload button. Publishing means editing Markdown in a text editor or directly in GitHub and pushing changes. Keep personal secrets, credentials, private employer/client data, or sensitive logs out of public posts.

## Deploy on GitHub Pages (free)

1. Create a GitHub repository and upload all files **including** `.github/workflows/pages.yml`.
2. Open repository **Settings → Pages → Build and deployment → Source: GitHub Actions**.
3. Each time you edit a post in GitHub and commit to `main`, the workflow automatically runs `python build.py` and deploys `site/`.
4. Your public site URL will be shown in the workflow / Pages settings.

Posts can therefore be added from the GitHub website: **Add file → Create new file → `posts/2026-10-25-my-entry.md` → write → Commit changes**, and the blog updates automatically.
