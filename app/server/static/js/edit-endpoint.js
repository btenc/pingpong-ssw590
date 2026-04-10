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
const endpointActive = document.getElementById("editEndpointActive");

async function showEditModal(id) {
  try {
    const endpoint = await fetchData(`/api/endpoints/${id}`);

    currentEditId = id;

    if (endpoint.name) endpointName.value = endpoint.name;
    if (endpoint.url) endpointUrl.value = endpoint.url;
    endpointActive.checked = endpoint.is_active === 1;

    error.style.display = "none";
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
        endpointName.value = validateString(endpointName.value, "Endpoint Name");
        endpointData["endpointName"] = endpointName.value;
      }

      if (endpointUrl.value) {
        endpointUrl.value = validateString(endpointUrl.value, "Endpoint URL");
        endpointData["endpointUrl"] = endpointUrl.value;
      }

      endpointData["isActive"] = endpointActive.checked;

      await fetchData(`/api/endpoints/${endpoint_id}`, {
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
