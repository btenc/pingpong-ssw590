const error = document.getElementById("error");
error.style.display = "none";

const cancelButton = document.getElementById("cancelButton");

if (cancelButton) {
  cancelButton.addEventListener("click", () => {
    const dialog = document.getElementById("add-dialog");
    if (dialog) {
      dialog.close();
    }
  });
}

const form = document.getElementById("addEndpointForm");
const endpointName = document.getElementById("endpointName");
const endpointUrl = document.getElementById("endpointUrl");

if (form) {
  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    try {
      endpointName.value = validateString(endpointName.value, "Endpoint Name");
      endpointUrl.value = validateString(endpointUrl.value, "Endpoint URL");

      const endpointData = {
        endpointName: endpointName.value,
        endpointUrl: endpointUrl.value,
      };

      await fetchData("http://127.0.0.1:5000/api/endpoints", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(endpointData),
      });

      window.location.href = "/";

    } catch (err) {
      error.style.display = "block";
      error.textContent = err;
    }
  });
}
