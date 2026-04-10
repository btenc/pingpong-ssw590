const configDialog = document.getElementById("config-dialog");
const configForm = document.getElementById("configForm");
const configInterval = document.getElementById("configInterval");
const configError = document.getElementById("configError");
const configCancelButton = document.getElementById("configCancelButton");

configError.style.display = "none";

configCancelButton.addEventListener("click", () => {
  configDialog.close();
});

async function showConfigModal() {
  try {
    const config = await fetchData("/api/config");
    configInterval.value = config.check_interval_seconds;
    configError.style.display = "none";
    configDialog.showModal();
  } catch (err) {
    alert("Could not load settings: " + err);
  }
}

configForm.addEventListener("submit", async (e) => {
  e.preventDefault();

  const interval = parseInt(configInterval.value);

  if (isNaN(interval) || interval < 1) {
    configError.style.display = "block";
    configError.textContent = "Interval must be a positive number.";
    return;
  }

  try {
    await fetchData("/api/config", {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ checkIntervalSeconds: interval }),
    });

    configDialog.close();
    window.location.reload();
  } catch (err) {
    configError.style.display = "block";
    configError.textContent = err;
  }
});
