---
name: build-technical-report
description: Build or refactor polished component-based technical report websites with a restrained dark editorial layout, multi-article navigation, sticky section rails, reusable evidence blocks, MathML equations, and dependency-free interactive SVG plots with sliders and zoom. Use when Codex needs to create an engineering/research report in HTML/CSS/JavaScript, reproduce this report architecture, add articles or technical visualizations, or turn analysis results into an organized browsable report.
---

# Build Technical Report

Create technical reports from the bundled static template. Preserve evidence, equations, caveats, and source links; visual polish must not hide uncertainty.

## Workflow

1. Inspect the source material and identify the report's claims, evidence, methods, limitations, and decisions.
2. Scaffold the template:

   ```powershell
   python scripts/scaffold_report.py <output-directory> --title "Report title" --brand "Short brand" --accent "#39BF5E"
   ```

3. Read [design-system.md](references/design-system.md) before changing layout, typography, motion, or colors.
4. Read [articles-and-components.md](references/articles-and-components.md) before adding, removing, or renaming articles.
5. Read [reusable-blocks.md](references/reusable-blocks.md) when selecting tables, metrics, callouts, equations, timelines, or workflow blocks.
6. Read [interactive-plots.md](references/interactive-plots.md) before changing SVG plots, sliders, legends, zoom, axes, or data adapters.
7. Replace the example content and data. Keep article HTML in `components/`, behavior in `scripts/`, data/configuration in `data/`, and presentation in `styles/`.
8. Choose the verification cadence:

   - **First build of a newly scaffolded report:** complete steps 9–11 before delivery.
   - **Any later edit to an existing report:** do not run validators, browser checks, print/PDF exports, screenshots, or other verification unless the user explicitly asks for it. If asked, run only the requested checks.

9. For a first build, run structural validation:

   ```powershell
   python scripts/validate_report.py <report-directory>
   ```

10. For a first build, serve over HTTP—component loading does not work reliably from `file://`:

   ```powershell
   python -m http.server 8010 --directory <report-directory>
   ```

11. For a first build, inspect the rendered desktop and mobile layouts. Test the article drawer, section links, content scrollbar position and hover state, slider, legend toggles, zoom drag, reset, print view, and console.

## Non-negotiable architecture

- Keep `index.html` as the shell, not a monolithic report.
- Register articles in `data/report-config.json`; load their HTML components dynamically.
- Give every article a stable `article-N` id and every section a globally unique id.
- Keep the 20/60/20 desktop composition: section rail, reading column, contextual aside.
- Collapse to a single readable column on small screens with no horizontal page overflow.
- Load IBM Plex Sans and IBM Plex Mono from Google Fonts. Use the sans face for prose and the mono face for labels, measurements, and indices.
- Keep running text at a responsive 17–19 px with at least 1.5 line height and a reading measure no wider than 72 characters.
- Keep the top bar outside the scrolling content viewport so the rounded accent scrollbar begins below it and becomes fully opaque on thumb hover.
- Do not add a persistent Print button; use browser or operating-system print commands for print testing and export.
- Use restrained surfaces, thin rules, small radii, and one configurable accent. Do not add gradients, glass effects, decorative shadows, or dashboard filler.
- Animate only state changes and progressive disclosure. Respect `prefers-reduced-motion`.
- Use native MathML for equations when practical. Add descriptive `aria-label` values to important equations and figures.
- Keep plots dependency-free unless the user's existing stack requires a library.
- Never encode meaning by color alone. Pair color with labels, line styles, or symbols.

## Content rules for agents

- Lead each article with the decision or technical question.
- Separate demonstrated results from hypotheses and recommendations.
- Put qualifications next to the claim they limit.
- Label proxy metrics as proxies; do not rename them as exact certificates.
- Link primary sources directly and distinguish local evidence from literature evidence.
- Prefer one useful table or diagram over repeated card grids.
- Keep signal colors and line styles consistent across every plot in one report.
- Show actual limits and tolerances explicitly on plots and in equations.

## Adding an article

1. Copy an existing component under `components/`.
2. Change its article id and all section ids.
3. Add one entry to `data/report-config.json` with `id`, `label`, `summary`, and `component`.
4. Add matching section links inside the article's `.nav`.
5. If this article is part of the report's first build, or the user explicitly requests verification, run `validate_report.py` and browser-test direct hashes such as `#article-3` and `#new-section`. Otherwise stop after implementing the article.

Do not hard-code article names or counts in `index.html` or `app-shell.js`; the registry owns them.

## Plot contract

The bundled plot demonstrates the required interaction contract:

- a labeled range slider changes an operating condition;
- a stable SVG view box keeps axes responsive;
- legend buttons toggle series without changing layout;
- magnifier mode enables drag-to-zoom;
- the selection highlight disappears after the zoom completes;
- Reset restores the complete domain and every control state;
- axes are recalculated from the active domain and visible series.

Adapt `scripts/interactive-plot.js` rather than rewriting the interaction from scratch. Keep data generation or exported arrays outside the renderer.

## Initial-build completion gate

Apply this gate only to the first build of a newly scaffolded report, or when the user explicitly asks for full verification. Do not rerun it after later edits by default.

Finish the initial build only when:

- the bundled validator passes;
- every registered component loads over HTTP;
- article and section hashes work after reload;
- interactive controls work with mouse and keyboard;
- no console errors remain;
- desktop and mobile views are readable;
- the content scrollbar begins below the top bar, uses a translucent accent at rest, and uses the full accent on hover;
- print mode removes navigation controls, preserves equations/tables, and renders headings with strong dark-on-light contrast;
- the final report contains no example claims or placeholder data unless the user requested a demo.

