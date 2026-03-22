// charts.js - chart rendering for timeline, risk, explainability
// Requires Chart.js (add CDN in HTML)
function renderTimelineChart(canvasId, data) {
  const ctx = document.getElementById(canvasId).getContext('2d');
  new Chart(ctx, {
    type: 'line',
    data: {
      labels: data.visits,
      datasets: [{
        label: 'Risk Probability',
        data: data.probabilities,
        borderColor: '#2563eb',
        fill: false
      }]
    },
    options: {responsive: true}
  });
}
function renderRiskStratification(canvasId, data) {
  const ctx = document.getElementById(canvasId).getContext('2d');
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: data.groups,
      datasets: [{
        label: 'Patient Risk',
        data: data.values,
        backgroundColor: '#2563eb'
      }]
    },
    options: {responsive: true}
  });
}
function renderExplainabilityHeatmap(canvasId, data) {
  const ctx = document.getElementById(canvasId).getContext('2d');
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: data.labels,
      datasets: data.datasets
    },
    options: {responsive: true}
  });
}
window.renderTimelineChart = renderTimelineChart;
window.renderRiskStratification = renderRiskStratification;
window.renderExplainabilityHeatmap = renderExplainabilityHeatmap;
