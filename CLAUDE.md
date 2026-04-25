# The Busbar

This project produces a weekly English-language DC electrical systems news digest and publishes it to GitHub Pages.

## Repo structure

```
busbar_agent.py               # Python script: fetches DC news from RSS/web sources
sources.json                  # Tiered source pool (tier_a, tier_b, tier_c, event_driven)
editions/published-topics.md  # Tracking of published stories (duplicate prevention)
editions/run-logs/            # Per-edition run logs (not published)
about.html                    # About page (static)

src/                          # Eleventy source files
  editions/                   # One .md file per edition (YYYY-MM-DD.md = Monday of week)
  index.njk                   # Homepage with pagination (10 editions per page)
  archive.njk                 # Full archive of all editions
  _includes/layouts/
    base.njk                  # Base layout (header, footer, dark mode script)
    edition.njk               # Edition layout (TOC, lead, news, background, product radar…)
  assets/
    css/main.css              # Shared stylesheet — copper/amber accent, readability-first
    fonts/                    # Self-hosted WOFF2 fonts (Inter + Source Serif 4)
    fonts/fonts.css           # @font-face declarations

_site/                        # Eleventy build output (gitignored in source repo)
```

## Publishing

- Repo: `BlackMac/the-busbar` (source on `main`, built output deployed via GitHub Actions)
- Build + deploy: pushing to `main` triggers `.github/workflows/deploy.yml`, which runs `npm run build` and publishes `_site/` to GitHub Pages.
- URL: `https://busbar.voltplan.app/` (custom domain via `CNAME` in repo root, passthrough-copied by Eleventy)
- Local preview: `npm run dev` serves on `http://localhost:8080`.

Typical weekly workflow:

```bash
# after writing src/editions/YYYY-MM-DD.md and editions/run-logs/YYYY-MM-DD.md:
npm run build                     # optional — verify locally
git add src/editions editions/run-logs editions/published-topics.md
git commit -m "Edition: week of YYYY-MM-DD"
git push origin main
# Actions runs build + deploy automatically (~1–2 min).
```

## Agent brief

The agent brief (mission, audience, scope, writing style, etc.) is in `AGENT_BRIEF.md`.
Read it before every run.

## Design system

Same readability-first approach as Die Inferenz, adapted for The Busbar:
- **Source Serif 4** — body text, TL;DR, article bodies
- **Inter** — headlines, tags, meta, navigation
- **Accent colour**: copper/amber `#b45309` (light) / `#f59e0b` (dark) — reflects the physical busbar
- **Content width**: 800px max, article text at 68ch
- Dark mode via `data-theme` attribute + `localStorage`
- No external requests (fonts self-hosted, GDPR-compliant)

## Edition YAML schema

Each edition file is `src/editions/YYYY-MM-DD.md` where the date is the **Monday** of the week.

```yaml
---
date: 2026-04-28          # Monday of the week — Eleventy uses this for sorting
week_of: "Week of 2026-04-21"   # Display string in edition header
edition: 1                # Sequential edition number
week_summary: "One-sentence summary of the week's biggest story."

# ── Section 5.2: The Lead (200–350 words) ──
lead:
  tag: Battery            # Ressort tag (see list below)
  headline: "Epoch recalls 48V 100Ah over internal busbar defect; 2,400 units affected"
  tl_dr: "One or two sentences. The TL;DR shown in italic under the headline."
  body: |
    <p>Full lead text here. 200–350 words. HTML paragraphs.</p>
  # Optional: surface an Amazon affiliate link. Prefer amazon_product_id (direct
  # ASIN via VoltPlan registry) over amazon_query (Amazon search). If both set,
  # product_id wins. Leave empty to omit the "Find on Amazon" CTA.
  amazon_query: "Epoch 48V 100Ah LiFePO4"
  # amazon_product_id: "victron-smartshunt"   # from VoltPlan's blog-affiliate-links.ts registry
  sources:
    - label: "Epoch Batteries — Official Recall Notice"
      url: "https://..."

# ── Section 5.3: News (4–7 items, 80–150 words each) ──
news:
  - id: news-1
    tag: Solar
    headline: "..."
    tl_dr: "..."
    body: |
      <p>...</p>
    amazon_query: "..."           # optional — Amazon search link via /api/go
    # amazon_product_id: "..."    # optional — direct ASIN via VoltPlan registry
    sources:
      - label: "..."
        url: "..."

# ── Section 5.4: The Background (400–700 words) — optional ──
background:
  type: market_analysis   # product_comparison | market_analysis | standards_explainer | teardown_roundup | trend_piece
  headline: "..."
  body: |
    <p>...</p>
    <h3>Subheading if needed</h3>
    <p>...</p>
  sources:
    - label: "..."
      url: "..."

# ── Section 5.5: Community Pulse (100–200 words) — optional ──
community_pulse:
  body: |
    <p>...</p>
  threads:
    - label: "Thread title / forum name"
      url: "https://..."

# ── Section 5.6: On the Bench — YouTube picks (2–4 videos) — optional ──
youtube:
  - id: "VIDEO_ID"          # YouTube video ID (from the watch?v= URL)
    title: "Video title"
    channel: "Channel Name"
    published: "April 2026"  # Publication date (freeform string)
    label: "Build Walk-through"  # Card label: Build Walk-through | Review | Firmware Deep-dive | Teardown | Tutorial
    description: "One or two sentences about why this is worth watching."
    featured: false          # true = full-width 2-col card with "Must Watch" badge

# Thumbnail download (run before build):
#   curl -sL "https://i.ytimg.com/vi/VIDEO_ID/mqdefault.jpg" \
#        -o src/assets/images/thumbs/VIDEO_ID.jpg

# ── Section 5.7: Product Radar (3–6 items) ──
product_radar:
  - tag: Battery
    name: "SOK 206Ah 48V LiFePO4"
    manufacturer: "SOK Battery"
    description: "One-sentence description of what the product is."
    price: "$1,299"
    availability: "Available now, ships from US warehouse"
    url: "https://sokbattery.com/..."
    editorial: "First 48V pack from SOK with built-in heater — optional, one line max."
    image: "sok-206ah-48v.jpg"        # optional — filename in src/assets/images/products/
    image_alt: "SOK 206Ah 48V pack"   # optional — defaults to product name
    amazon_query: "SOK 206Ah 48V LiFePO4"   # optional — Amazon search link via /api/go
    # amazon_product_id: "..."              # optional — direct ASIN via VoltPlan registry

# ── Section 5.8: Recalls & Safety — optional ──
recalls:
  - tag: Safety
    headline: "..."
    body: |
      <p>...</p>
    source_label: "CPSC Recall Notice #24-xxx"
    source_url: "https://..."
---
```

## Ressort tags

Exactly one tag per news item, news piece, and product radar item:

| Tag | When to use |
|-----|-------------|
| `Battery` | cells, packs, BMS, battery management |
| `Solar` | panels, mounting, MPPT, solar-side topics |
| `Inverter` | inverters, inverter/chargers |
| `Charging` | DC-DC, shore power, alternator regulation |
| `Monitoring` | shunts, GX devices, apps, displays |
| `Thermal` | fridges, diesel/electric heating, DC aircon, battery thermal |
| `Safety` | recalls, standards, fire incidents, regulatory changes |
| `Marine` | boat-specific news (ABYC, galvanic isolation, 24V-boat topics) |
| `Overland` | vehicle/caravan-specific (TÜV, 4WD, alternator-dominant setups) |
| `Industry` | company news, M&A, market moves, pricing |
| `Firmware` | software/firmware releases that affect users |

## Weekly workflow

1. **Fetch raw news**: `python3 busbar_agent.py --format json --output /tmp/busbar-raw.json`
   - Articles without a date (`"published": null`) are included — verify with WebSearch
2. **Supplement with WebSearch**: search for DC electrical news from the past 7–10 days
   - Always check `professional.victronenergy.com/news/` directly — best source for Victron firmware
   - Key searches: `Victron firmware [month year]`, `LiFePO4 battery recall CPSC`, `site:diysolarforum.com [topic]`
3. **Duplicate check**: compare *every section* of the planned edition against `editions/published-topics.md`. Six tracked dimensions:
   - Stories (news items + Lead) — same firmware version, same product launch, same recall, same forum-driven story should not be re-covered
   - Product Radar — same manufacturer + product name should not appear twice (newer revision is fine, but say so)
   - Recalls — same recall ID should not be repeated unless materially expanded
   - Background deep-dives — don't repeat the same angle on the same topic within ~6 months
   - Community Pulse — same forum thread / Reddit post URL should not appear twice
   - On the Bench — each YouTube `VIDEO_ID` appears at most once across all editions
4. **Fact-check**: verify specs/prices against primary sources. Never fabricate.
5. **Download images** for any YouTube videos or product images included:
   ```bash
   # YouTube thumbnails (one per video):
   curl -sL "https://i.ytimg.com/vi/VIDEO_ID/mqdefault.jpg" -o src/assets/images/thumbs/VIDEO_ID.jpg
   # Product images: save to src/assets/images/products/FILENAME.jpg
   ```
6. **Write edition file**: `src/editions/YYYY-MM-DD.md` — use this CLAUDE.md schema above
7. **Write run log**: `editions/run-logs/YYYY-MM-DD.md` (see Run Log section below)
8. **Build and deploy** (see Publishing above)
9. **Update tracking**: append entries to *every relevant section* of `editions/published-topics.md` — Stories, Product Radar, Recalls, Background, Community Pulse, On the Bench. One bullet per item. The file is the single source of truth for dedup; if it's incomplete, future editions repeat themes.

## Run log format

Every edition produces a run log at `editions/run-logs/YYYY-MM-DD.md`:

```markdown
# Run Log — Week of YYYY-MM-DD

## Run metadata
- Date: YYYY-MM-DD HH:MM UTC
- Edition: #N

## Sources scanned
- [Source name] — N articles found

## Items considered but rejected
- [Title/topic] — reason (e.g.: "older than 7 days", "out of scope: home solar", "unverifiable claim")

## Items included
- Lead: [headline]
- News 1–N: [headlines]
- Background: [headline or "skipped — no strong story"]
- Community Pulse: [included / skipped — reason]
- Product Radar: [product names]
- Recalls: [included / none this week]

## Sections skipped
- Background: [reason if skipped]

## REVIEW FLAGS
1. [Flag description — what needs human check]
2. ...

## Broken sources
- [Source name] — reason (unreachable / feed format change)
```

## Affiliate links

Amazon affiliate links are rendered via VoltPlan's `/api/go` redirect
(`https://voltplan.app/api/go?q=<query>&source=busbar_<edition-date>`). OneLink
handles marketplace/tag rewriting at click time — we never build Amazon URLs
directly. Revenue accrues to the VoltPlan Associate ID (`voltplan0a-21`).

Two fields are supported on `lead`, each `news` item, and each `product_radar` item:

- `amazon_query` — free-text search string (e.g. product name)
- `amazon_product_id` — ID from VoltPlan's `src/lib/blog-affiliate-links.ts`
  registry (e.g. `victron-smartshunt`) for a direct ASIN. Wins if both set.

Add them only when the product is plausibly on Amazon (consumer electronics,
off-the-shelf components). Skip for manufacturer-only items, niche industrial
gear, or anything where an Amazon search would return noise. A disclosure
aside is rendered on every edition page automatically.

Eleventy filters:
- `{{ 'Victron SmartShunt' | amazonGo(dateStr) }}` → full `/api/go` URL
- `{{ 'victron-smartshunt' | amazonGoId(dateStr) }}` → registry-based variant

## Language

All edition content in English. Code comments and technical docs in English.

## Author

All editions are authored by **The Busbar AI Agent**. Never use the site owner's name in edition content.

## Prices

USD primary, EUR and GBP in parentheses when relevant. Format: $1,234 / €1,100 / £950.

## Units

Amps (A), Amp-hours (Ah), Watts (W), Watt-hours (Wh), Volts (V). No space between number and unit: 100Ah, 48V, 3000W.
