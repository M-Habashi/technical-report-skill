"use strict";

function exampleSeries(condition) {
  const measured = [];
  const command = [];
  const desired = [];
  const damping = 3.25 - 0.9 * condition;
  const frequency = 10.4 - 2.1 * condition;

  for (let index = 0; index < 241; index += 1) {
    const time = 2.2 * index / 240;
    measured.push({ x: time, y: 1 - Math.exp(-damping * time) * (Math.cos(frequency * time) + 0.18 * Math.sin(frequency * time)) });
    command.push({ x: time, y: 1 + (1.2 + 0.35 * condition) * Math.exp(-7.4 * time) - 0.22 * Math.exp(-2.8 * time) * Math.sin(8.5 * time) });
    desired.push({ x: time, y: 1 });
  }

  return [
    { id: "desired", label: "Desired", color: "#F3F0E8", dash: "dash", points: desired },
    { id: "measured", label: "Measured", color: "#007CA8", dash: "solid", points: measured },
    { id: "command", label: "Command", color: "#AC6420", dash: "dash", points: command }
  ];
}

export function initInteractivePlot(container, options = {}) {
  const plot = container.querySelector("[data-plot-host]");
  const slider = container.querySelector("[data-condition-slider]");
  const conditionValue = container.querySelector("[data-condition-value]");
  const seriesAdapter = options.series || exampleSeries;
  let frame = null;

  function token(name) {
    return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
  }

  function render() {
    const condition = Number(slider.value) / 100;
    conditionValue.textContent = condition.toFixed(2);
    const traces = seriesAdapter(condition).map(item => ({
      type: "scattergl",
      mode: "lines",
      uid: item.id,
      name: item.label,
      x: item.points.map(point => point.x),
      y: item.points.map(point => point.y),
      line: { color: item.color, width: 2.5, dash: item.dash || (item.dashed ? "dash" : "solid") },
      hovertemplate: `${item.label}<br>x %{x:.3f}<br>y %{y:.3f}<extra></extra>`
    }));

    Plotly.react(plot, traces, {
      paper_bgcolor: "rgba(0,0,0,0)",
      plot_bgcolor: "rgba(0,0,0,0)",
      font: { color: token("--foreground"), family: token("--font-sans"), size: 14 },
      margin: { l: 68, r: 22, t: 24, b: 58 },
      showlegend: true,
      legend: { orientation: "h", x: 0, y: 1.02, yanchor: "bottom", itemclick: "toggle", itemdoubleclick: "toggleothers", uirevision: "response-series" },
      dragmode: "zoom",
      hovermode: "closest",
      uirevision: "response-view",
      xaxis: { title: { text: "Time (s)" }, range: [0, 2.2], gridcolor: token("--border"), zerolinecolor: token("--muted"), linecolor: token("--muted-strong"), mirror: true },
      yaxis: { title: { text: "Normalized amplitude" }, range: [-0.2, 2.35], gridcolor: token("--border"), zerolinecolor: token("--muted"), linecolor: token("--muted-strong"), mirror: true }
    }, {
      responsive: true,
      scrollZoom: true,
      displaylogo: false,
      doubleClick: "reset+autosize",
      modeBarButtonsToRemove: ["select2d", "lasso2d"]
    });
  }

  slider.addEventListener("input", () => {
    if (frame) cancelAnimationFrame(frame);
    frame = requestAnimationFrame(() => {
      frame = null;
      render();
    });
  });
  window.addEventListener("resize", () => Plotly.Plots.resize(plot), { passive: true });
  render();
}
