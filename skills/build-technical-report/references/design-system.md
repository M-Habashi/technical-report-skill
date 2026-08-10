# Design system

## Purpose

Reproduce a restrained engineering-report aesthetic: dark editorial surfaces, precise typography, thin separators, compact controls, and one accent color. The layout should feel like a technical publication with interactive instruments—not a dashboard.

## Tokens

The template defines all theme values in `styles/base.css`:

| Token | Default | Use |
|---|---:|---|
| `--background` | `#11110f` | page and sticky header |
| `--foreground` | `#f3f0e8` | primary text |
| `--surface` | `#191917` | restrained callouts and controls |
| `--muted` | `#aaa69d` | secondary copy |
| `--border` | `#34332e` | primary rules |
| `--border-soft` | `#292824` | internal separators |
| `--accent` | configurable | progress, active links, selection |
| `--accent-strong` | derived/configurable | compact labels and indices |

Set the report accent in `data/report-config.json`. JavaScript applies it to the document root. Keep one accent unless a signal-semantic palette is required.

## Typography

- Load IBM Plex Sans and IBM Plex Mono from Google Fonts in `index.html`; keep practical system fallbacks in CSS.
- Body: IBM Plex Sans, responsive 17–19 px (`clamp(1.0625rem, 1rem + 0.25vw, 1.1875rem)`), line height 1.6.
- H1: responsive 40–60 px, weight 600, tight tracking.
- H2: responsive 28–36 px, weight 600.
- H3: 22 px, weight 600.
- Mono: IBM Plex Mono for indices, parameter values, axes, and state labels.
- Reading measure: keep running prose at or below 72 characters (`72ch`).
- Compact labels, captions, and specialized controls may use 13–15 px; do not use compact sizes for running prose.

Do not shrink dense technical content below 13 px. Prefer horizontal table scrolling to illegible text. During first-build verification—or when the user explicitly requests it—confirm that the layout still reflows at 200% text scaling.

Readability basis:

- [GOV.UK's tested type scale](https://design-system.service.gov.uk/styles/type-scale/) uses 19 px body text.
- [U.S. Web Design System typography guidance](https://designsystem.digital.gov/components/typography/) recommends at least 16 px body text, 45–90 characters per line, and at least 1.5 line height for longer text.
- [W3C technique C21](https://www.w3.org/WAI/WCAG22/Techniques/css/C21) recommends line height between 1.5 and 2 for reading text.

## Layout

Desktop articles use a shared composition:

```text
20% section rail | 60% article | 20% contextual note
```

- Header: fixed outside the scrolling content viewport, 60 px tall.
- Content viewport: fill the remaining viewport height and own vertical scrolling so its scrollbar begins below the header.
- Scrollbar: use a thin rounded thumb in the configured accent at approximately 40% opacity; transition to the full accent color when the thumb is hovered. Keep its track transparent and retain Firefox and WebKit declarations.
- Section rail: sticky below the header; it belongs to the full article, not an individual subplot.
- Main sections: 64 px vertical rhythm with a thin top rule.
- Mobile: the header remains outside the content viewport, the rail moves above the article, and content becomes one column.

## Surfaces and shape

- Prefer border-separated regions over floating cards.
- Keep plot canvases transparent rather than placing white or separately colored rectangles behind them.
- Use 0–4 px radii for controls and bounded figures.
- Do not use gradients, glassmorphism, large shadows, decorative blobs, or excessive badges.
- Avoid repeated identical cards when a table, definition list, or ruled sequence communicates structure better.

## Motion

- Keep transitions between 120 and 220 ms.
- Animate opacity, border color, or short translations only.
- Do not animate reading text continuously.
- Disable nonessential motion under `prefers-reduced-motion`.

## Print

Print CSS must:

- rely on the browser or operating system print command; do not add a persistent Print button to the report header;
- switch to a white background and dark text;
- set a dedicated dark heading token so dark-theme headings remain legible on the light page;
- release the fixed-height content viewport and restore visible overflow;
- hide the top bar, article drawer, section rail, and plot controls;
- remove scrollbars from wide tables, release their screen-only minimum width, and wrap cell text inside the printable page;
- avoid splitting key figures, tables, and equations when possible;
- expose hidden articles only if the report explicitly supports printing all articles.

