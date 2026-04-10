function getCurrentTheme() {
  return window.matchMedia("(prefers-color-scheme: dark)").matches
    ? "dark"
    : "light";
}

const pieData = JSON.parse(document.getElementById("chart-data").textContent);

const labels = Object.keys(pieData);
const series = Object.values(pieData);

if (series.length === 0) {
  document.querySelector("#codes-chart").textContent = "No checks yet.";
} else {

theme = getCurrentTheme();

const options = {
  series: series,
  labels: labels,
  chart: {
    type: "pie",
    height: 300,
    width: 300,
    background: "transparent",
    accessibility: {
      enabled: true,
      keyboard: {
        enabled: true,
        wrapAround: true,
      },
    },
  },
  plotOptions: {
    pie: { donut: { size: "65%" } },
  },
  dataLabels: {
    enabled: true,
    style: {
      colors: [theme === "dark" ? "var(--color-black)" : "var(--color-white)"],
    },
    dropShadow: {
      enabled: true,
      color: theme === "dark" ? "var(--color-white)" : "var(--color-black)",
    },
  },
  theme: { mode: theme },
  stroke: {
    colors: [theme === "dark" ? "var(--color-white)" : "var(--color-black)"],
  },
};

let chart = new ApexCharts(document.querySelector("#codes-chart"), options);
chart.render();

window
  .matchMedia("(prefers-color-scheme: dark)")
  .addEventListener("change", () => {
    const current = getCurrentTheme();
    chart.updateOptions(
      {
        dataLabels: {
          style: {
            colors: [
              theme === "dark" ? "var(--color-black)" : "var(--color-white)",
            ],
          },
          dropShadow: {
            color:
              theme === "dark" ? "var(--color-white)" : "var(--color-black)",
          },
        },
        theme: { mode: current },
        stroke: {
          colors: [
            current === "dark" ? "var(--color-white)" : "var(--color-black)",
          ],
        },
      },
      true,
    );
  });
}
