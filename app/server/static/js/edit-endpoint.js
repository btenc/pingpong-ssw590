let currentEditId = null;

const error = document.getElementById("editError");
error.style.display = "none";

const cancelButton = document.getElementById("editCancelButton");

if (cancelButton) {
  cancelButton.addEventListener("click", () => {
    const dialog = document.getElementById("edit-dialog");
    if (dialog) {
      dialog.close();
    }
  });
}

const dialog = document.getElementById("edit-dialog");
const form = document.getElementById("editEndpointForm");
const editEndpointId = document.getElementById("editEndpointId");
const endpointName = document.getElementById("editEndpointName");
const endpointUrl = document.getElementById("editEndpointUrl");

async function showEditModal(id) {
  try {
    const endpoint = await fetchData(
      `http://127.0.0.1:5000/api/endpoints/${id}`,
    );

    currentEditId = id;
    id = validateEndpointId(id, "Endpoint Id");

    if (endpoint.name) endpointName.value = endpoint.name;
    if (endpoint.url) endpointUrl.value = endpoint.url;

    if (dialog) dialog.showModal();
  } catch (err) {
    error.style.display = "block";
    error.textContent = err;
  }
}

if (form) {
  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    try {
      const endpoint_id = validateEndpointId(currentEditId, "Endpoint Id");

      if (!endpointName.value && !endpointUrl.value)
        throw "Must input either endpoint name or url to proceed.";

      let endpointData = {};

      if (endpointName.value) {
        endpointName.value = validateString(
          endpointName.value,
          "Endpoint Name",
        );
        endpointData["endpointName"] = endpointName.value;
      }

      if (endpointUrl.value) {
        endpointUrl.value = validateString(endpointUrl.value, "Endpoint URL");
        endpointData["endpointUrl"] = endpointUrl.value;
      }

      await fetchData(`http://127.0.0.1:5000/api/endpoints/${endpoint_id}`, {
        method: "PATCH",
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
