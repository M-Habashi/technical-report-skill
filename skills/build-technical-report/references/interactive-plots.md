# Interactive Plotly plots

## Module boundary

`scripts/interactive-plot.js` receives a container element and an adapter:

```js
initInteractivePlot(container, {
  condition: 0,
  series(condition) {
    return [
      { id: "measured", label: "Measured", color: "#007CA8", dash: "solid", points: [...] },
      { id: "command", label: "Command", color: "#AC6420", dash: "dash", points: [...] }
    ];
  }
});
```

Keep scientific data in `data/` or a generated module. The renderer should not know plant/controller equations.

## Required interactions

### Slider

- Associate the range input with a visible label.
- Show the current engineering value, not only a normalized 0–1 coordinate.
- Update the plot in one animation frame.
- Keep the slider usable with arrow keys.

### Legend

- Use Plotly's native legend with `itemclick: "toggle"` and `itemdoubleclick: "toggleothers"`.
- Set stable trace `uid` values and `legend.uirevision` so hidden state survives updates.
- Pair color with dashed/solid styles and readable names.

### Zoom

- Prefer Plotly's native drag zoom, scroll zoom, double-click reset, and modebar Reset axes action.
- Remove selection and lasso controls unless the report needs them.
- Set `uirevision` when data updates should preserve the current view.

### Responsive behavior

- Set `responsive: true` and give the plot host a CSS `min-height`.
- Resize with `Plotly.Plots.resize` when the report shell changes size.
- Do not set a fixed pixel width in JavaScript.

## Axis rules

- Keep the SVG and plot-region background transparent.
- Use the report's typography and theme tokens: foreground for axis titles and active legend text, muted colors for ticks and supporting copy, border colors for grids, and the configured accent for interaction states.
- Derive domains from finite data only.
- Add 5–10% padding unless an engineering limit defines the boundary.
- Make the zero line lighter or thicker than ordinary grid lines when positive and negative values coexist.
- Keep tick precision stable while a slider moves.
- Display units in axis labels, not repeated on every tick.

## Performance

- Default to `scattergl` for line plots, especially long records and multi-trace overlays.
- Use `Plotly.react` rather than rebuilding the plot container.
- For density overlays, place alpha in the RGBA line color. Trace-level `opacity` is uniform across the completed trace and does not encode repeated-pass density.
- Decimate exceptionally large data before rendering and avoid markers unless they add evidence.
- Respect reduced motion and avoid animated axes during rapid slider input.

## Bundled runtime

The template vendors the pinned Plotly GL2D 3.7.0 partial bundle at `scripts/vendor/plotly-gl2d.min.js`. Keep the adjacent license file and load the bundle before `scripts/main.js`. Do not replace it with a CDN URL; scaffolded reports must remain runnable offline and without a build step.
