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

- Body: IBM Plex Sans, 16 px, line height 1.6.
- H1: `clamp(36px, 4vw, 46px)`, weight 600, tight tracking.
- H2: `clamp(25px, 2.4vw, 30px)`, weight 600.
- H3: 18–19 px, weight 600.
- Mono: IBM Plex Mono for indices, parameter values, axes, and state labels.
- Reading measure: keep prose near 720–780 px.

Do not shrink dense technical content below 13 px. Prefer horizontal table scrolling to illegible text.

## Layout

Desktop articles use a shared composition:

```text
20% section rail | 60% article | 20% contextual note
```

- Header: sticky, 54 px tall.
- Section rail: sticky below the header; it belongs to the full article, not an individual subplot.
- Main sections: 64 px vertical rhythm with a thin top rule.
- Mobile: header becomes static, the rail moves above the article, and content becomes one column.

## Surfaces and shape

- Prefer border-separated regions over floating cards.
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

- switch to a white background and dark text;
- hide the top bar, article drawer, section rail, and plot controls;
- avoid splitting key figures, tables, and equations when possible;
- expose hidden articles only if the report explicitly supports printing all articles.

