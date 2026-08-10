# Reusable blocks

Choose the block that makes a technical relationship easiest to verify.

## Decision or caveat

Use `.verdict` for one high-value conclusion beside an article introduction. Use `.note` inside the reading column for a limitation, interpretation, or warning.

## Status strip

Use `.status-line` for report maturity, data provenance, or an explicit “hypothesis—not result” statement.

## Metrics

Use `.metric-grid` for three to six comparable values. Every metric needs a label, primary value, units or context, and interpretation. Do not use metrics as decorative counters.

## Tables

Wrap tables in `.table-shell`. Use tables for exact mappings, literature comparisons, parameter audits, and pass/fail gates. Keep numeric columns right-aligned with `.number`.

## Equations

Use `.math-block` and native MathML. Mark the decisive equation with `.is-key`. Put the meaning or limitation immediately below in `.equation-caption`.

## Ruled sequences

Use `.step-list` for experimental or implementation sequences. Use `.idea-rank` for ordered alternatives with short explanations.

## Architecture strip

Use `.system-strip` for three or more dependent blocks in a signal chain. Keep labels short; put derivations in prose or MathML below.

## Plot block

Each `.plot-block` contains:

1. `.plot-header` with title, interpretation, and controls;
2. `.plot-workbench` with the SVG and sticky/adjacent controls;
3. an accessible legend with toggle buttons;
4. `.plot-note` explaining normalization, limits, and caveats.

Never place a legend or slider where it stops midway through a long subplot group. Sticky controls should be scoped to the complete plot workbench.

