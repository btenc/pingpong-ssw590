function filterChecks(checkbox) {
  document.querySelectorAll("#checksTable tr[data-success]").forEach(row => {
    if (checkbox.checked && row.dataset.success === "1") {
      row.style.display = "none";
    } else {
      row.style.display = "";
    }
  });
}

async function runCheck(endpointId) {
  const button = document.getElementById("runCheckButton");
  button.disabled = true;
  button.textContent = "Checking...";

  try {
    await fetchData(`/api/endpoints/${endpointId}/check`, { method: "POST" });
    window.location.reload();
  } catch (err) {
    alert("Check failed: " + err);
    button.disabled = false;
    button.textContent = "Run Check Now";
  }
}
