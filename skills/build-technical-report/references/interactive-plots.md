# Interactive SVG plots

## Module boundary

`scripts/interactive-plot.js` receives a container element and an adapter:

```js
initInteractivePlot(container, {
  condition: 0,
  series(condition) {
    return [
      { id: "measured", label: "Measured", color: "#007CA8", dashed: false, points: [...] },
      { id: "command", label: "Command", color: "#AC6420", dashed: true, points: [...] }
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

- Use buttons with `aria-pressed`.
- Preserve axes when a series is hidden unless the user explicitly requests rescaling.
- Pair color with dashed/solid styles and readable text.

### Zoom

- Magnifier mode is opt-in.
- Drag only inside the plot region.
- Draw a translucent selection rectangle while dragging.
- Remove the selection rectangle immediately on pointer release or cancellation.
- Ignore very small selections.
- Recalculate axis ticks after applying the selected domain.
- Expose a Reset button only after the domain changes.

### Responsive behavior

- Use one stable `viewBox`; let CSS size the SVG.
- Calculate pointer positions in SVG coordinates using the current bounding rectangle.
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

- Use SVG paths for lines and a single DOM update per path.
- Reuse axis and legend nodes.
- For large data, decimate before rendering; do not emit thousands of markers.
- Respect reduced motion and avoid animated axes during rapid slider input.

