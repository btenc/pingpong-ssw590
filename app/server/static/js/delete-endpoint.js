async function deleteEndpoint(id) {
  const confirmed = window.confirm("Are you sure you want to delete this endpoint? This will also delete all of its check history.");

  if (!confirmed) return;

  try {
    const result = await fetchData(`/api/endpoints/${id}`, {
      method: "DELETE",
    });

    if (result.is_deleted) {
      window.location.href = "/";
    } else {
      alert("Failed to delete endpoint.");
    }
  } catch (err) {
    alert("Error: " + err);
  }
}
