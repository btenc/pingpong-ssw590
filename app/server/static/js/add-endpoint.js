// Error Elements
const addError = document.getElementById("addError");
if (addError) addError.style.display = "none";

// Cancel Buttons
const addCancelButton = document.getElementById("addCancelButton");

if (addCancelButton) {
  addCancelButton.addEventListener("click", () => {
    const dialog = document.getElementById("add-dialog");
    if (dialog) dialog.close();
  });
}

// Form
const addForm = document.getElementById("addEndpointForm");
const addEndpointName = document.getElementById("addEndpointName");
const addEndpointUrl = document.getElementById("addEndpointUrl");

if (addForm) {
  addForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    try {
      addEndpointName.value = validateString(addEndpointName.value, "Endpoint Name");
      addEndpointUrl.value = validateString(addEndpointUrl.value, "Endpoint URL");

      const endpointData = {
        endpointName: addEndpointName.value,
        endpointUrl: addEndpointUrl.value,
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
      addError.style.display = "block";
      addError.textContent = err;
    }
  });
}