function validateString(obj, objName) {
  if (typeof obj === "undefined")
    throw `${objName || "Provided parameter"} was not supplied.`;

  if (!obj) throw `${objName || "Provided parameter"} was not supplied.`;

  if (typeof obj !== "string")
    throw `${objName || "Provided data"} is not a string'.`;

  if (obj.trim().length === 0)
    throw `${objName || "Provided string"} consists of only spaces.`;

  return obj.trim();
}

async function fetchData(url, options) {
  const response = await fetch(url, options);
  const json = await response.json();

  if (response.ok) {
    return json;
  
  } else {
    throw `${response.statusText}: ${json["error"]}`;
  }
}