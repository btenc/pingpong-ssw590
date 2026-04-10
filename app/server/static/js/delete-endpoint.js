const deleteError = document.getElementById("deleteError");
deleteError.style.display = "none";

const deleteCancelButton = document.getElementById("deleteCancelButton");
if (deleteCancelButton) {
  deleteCancelButton.addEventListener("click", () => {
    const dialog = document.getElementById("delete-dialog");
    if (dialog) {
      dialog.close();
    }
  });
}

const deleteButton = document.getElementById("deleteButton");
const deleteId = document.getElementById("delete-endpoint-id");

if (deleteButton) {
  deleteButton.addEventListener("click", async () => {
    try {
      let id = Number(deleteId.textContent)
      id = validateEndpointId(id, "Endpoint Id");

      const result = await fetchData(`/api/endpoints/${id}`, {
        method: "DELETE",
      });

      if (result.is_deleted) {
        window.location.href = "/";

      } else {
        deleteError.textContent = "We were unable to delete this endpoint. Please try again later."
        deleteError.style.display = "block";
      }
    } catch (err) {
        deleteError.textContent = err;
        deleteError.style.display = "block";
    }
  });
}

function showDeleteModal(id, name) {
  const deleteWarning = document.getElementById("delete-warning");
  if(deleteWarning) deleteWarning.textContent = `Are you sure you want to delete \"${name}\"?`;

  deleteId.textContent = id;

  const dialog = document.getElementById("delete-dialog");
  if (dialog) dialog.showModal();
}