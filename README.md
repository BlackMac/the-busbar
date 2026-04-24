# The Busbar

**A weekly English-language news digest about low-voltage (DC) electrical systems — for campers, boats, and off-grid builds.**

- Live site: [busbar.voltplan.app](https://busbar.voltplan.app/)
- Feed: [busbar.voltplan.app/feed.xml](https://busbar.voltplan.app/feed.xml)

Each edition covers what happened in the DC world that week: firmware releases, product launches, recalls, standards changes, community discussion. One lead story, four to seven news items, an optional deep-dive background, a product radar, and safety notices. Readable at a reasonable pace, written for people who can read a wiring diagram.

Editions are produced by an AI agent working from a curated source pool, then reviewed before publication. The agent brief lives in [`AGENT_BRIEF.md`](./AGENT_BRIEF.md); operational rules for production live in [`CLAUDE.md`](./CLAUDE.md).

## Stack

- [Eleventy](https://www.11ty.dev/) v3 — static site generator
- Nunjucks templates + Markdown-front-matter editions
- Self-hosted WOFF2 fonts (Inter, Source Serif 4, Fraunces, DM Mono) — GDPR-friendly, no external requests
- [Umami](https://umami.is/) for privacy-respecting analytics
- GitHub Actions → GitHub Pages for build + deploy

## Local development

```bash
npm install
npm run dev       # http://localhost:8080
npm run build     # one-off build into _site/
```

## Publishing flow

A push to `main` triggers [`.github/workflows/deploy.yml`](./.github/workflows/deploy.yml), which builds with Eleventy and deploys `_site/` to GitHub Pages. No manual deploy step.

```bash
# typical weekly commit
git add src/editions editions/run-logs editions/published-topics.md
git commit -m "Edition: week of YYYY-MM-DD"
git push origin main
```

## Repo structure

```
busbar_agent.py               Python helper: fetches DC news from RSS/web sources
sources.json                  Tiered source pool (tier_a / tier_b / tier_c / event_driven)
AGENT_BRIEF.md                Agent mission, audience, scope, writing style
CLAUDE.md                     Operational instructions for the publishing workflow
editions/
  published-topics.md         Duplicate-prevention tracking
  run-logs/YYYY-MM-DD.md      Per-edition production logs
src/
  editions/YYYY-MM-DD.md      One file per edition (date = Monday of the week)
  index.njk                   Homepage (paginated)
  archive.njk                 Full archive
  about.njk                   About page
  _includes/layouts/
    base.njk                  Header/footer/theme toggle
    edition.njk               Edition layout (TOC, sections, disclosure)
  assets/
    css/main.css              Shared stylesheet (light + dark themes)
    fonts/                    Self-hosted WOFF2 fonts + @font-face
    images/                   Product images, YouTube thumbnails
.github/workflows/deploy.yml  Actions workflow for Pages deploy
```

## Affiliate links

Amazon affiliate links are rendered via [VoltPlan](https://voltplan.app)'s `/api/go` redirect. OneLink handles marketplace/tag rewriting at click time. Disclosure is rendered on every edition page.

Two optional fields are supported on `lead`, each `news` item, and each `product_radar` item:

- `amazon_query: "Victron SmartShunt"` — free-text Amazon search
- `amazon_product_id: "victron-smartshunt"` — direct ASIN via VoltPlan's registry (wins if both set)

Details in [`CLAUDE.md`](./CLAUDE.md#affiliate-links).

## Editorial independence

The Busbar is editorially independent. Products are selected on merit; affiliate commissions never influence coverage. Recalls, safety notices, and critical assessments are published regardless of commercial relationships. See the [About page](https://busbar.voltplan.app/about.html) for full disclosure.

## Content license

All code in this repository (templates, styles, workflow, agent scripts) is provided as-is for reference; no OSI license is granted yet. Edition content (text and editorial decisions) is © The Busbar — all rights reserved. If you want to quote or reuse content, get in touch.
