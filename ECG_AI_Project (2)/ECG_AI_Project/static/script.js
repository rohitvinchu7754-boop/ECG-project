const form = document.getElementById("ecgForm");
const fileInput = document.getElementById("ecgFile");
const statusBox = document.getElementById("status");
const fileLabel = document.getElementById("fileLabel");
let chart;

function makeChart(values) {
  const canvas = document.getElementById("ecgChart");
  const labels = values.map((_, i) => i);
  if (chart) chart.destroy();
  chart = new Chart(canvas, {
    type: "line",
    data: {
      labels,
      datasets: [{
        label: "ECG amplitude",
        data: values,
        borderColor: "#0eae94",
        backgroundColor: "rgba(14,174,148,.08)",
        borderWidth: 1.7,
        pointRadius: 0,
        fill: true,
        tension: 0.08
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      animation: false,
      plugins: { legend: { display: false } },
      scales: {
        x: { title: { display: true, text: "Sample index", color: "#8a97aa", font: { size: 10 } },
             ticks: { maxTicksLimit: 7, color: "#8a97aa", font: { size: 9 } },
             grid: { color: "#f0f3f7" } },
        y: { title: { display: true, text: "Amplitude", color: "#8a97aa", font: { size: 10 } },
             ticks: { maxTicksLimit: 5, color: "#8a97aa", font: { size: 9 } },
             grid: { color: "#f0f3f7" } }
      }
    }
  });
}

fileInput.addEventListener("change", () => {
  fileLabel.textContent = fileInput.files[0]?.name || "Choose an ECG CSV file";
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const file = fileInput.files[0];
  if (!file) return;

  const data = new FormData();
  data.append("ecg_file", file);
  const button = form.querySelector("button");
  button.disabled = true;
  statusBox.classList.remove("error");
  statusBox.textContent = "Processing signal...";
  document.getElementById("modelNote").textContent = "Please wait while the file is processed.";

  try {
    const response = await fetch("/analyze", { method: "POST", body: data });
    const result = await response.json();
    if (!response.ok) throw new Error(result.error || "Analysis failed");

    document.getElementById("sampleMetric").textContent = result.samples.toLocaleString();
    document.getElementById("meanMetric").textContent = result.mean;
    document.getElementById("stdMetric").textContent = result.std;
    document.getElementById("minMetric").textContent = result.min;
    document.getElementById("maxMetric").textContent = result.max;
    document.getElementById("chartInfo").textContent = `${result.signal.length.toLocaleString()} points displayed`;
    document.getElementById("modelMetric").textContent = result.prediction ? "Loaded" : "Not loaded";
    document.getElementById("predictionMetric").textContent = result.prediction ?? "Not available";
    document.getElementById("confidenceMetric").textContent =
      result.confidence == null ? "—" : `${result.confidence}%`;
    document.getElementById("modelNote").textContent = result.model_status;
    makeChart(result.signal);
    statusBox.textContent = "Signal processed successfully.";
  } catch (error) {
    statusBox.textContent = error.message;
    statusBox.classList.add("error");
    document.getElementById("modelNote").textContent = "The file could not be processed. Check the format and try again.";
  } finally {
    button.disabled = false;
  }
});
