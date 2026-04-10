function validateString(obj, objName) {
  if (typeof obj === "undefined")
    throw new Error(`${objName || "Provided parameter"} was not supplied.`);

  if (!obj)
    throw new Error(`${objName || "Provided parameter"} was not supplied.`);

  if (typeof obj !== "string")
    throw new Error(`${objName || "Provided data"} is not a string'.`);

  if (obj.trim().length === 0)
    throw new Error(`${objName || "Provided string"} consists of only spaces.`);

  return obj.trim();
}

function validateNumber(num, numName) {
  if (typeof num === "undefined")
    throw new Error(`${numName || "Provided parameter"} was not supplied.`);

  if (typeof num !== "number")
    throw new Error(
      `${
        numName || "Provided data"
      } is not of type 'number', but of type '${typeof num}'.`,
    );

  if (isNaN(num)) throw new Error(`${numName || "Provided number"} is NaN.`);

  return num;
}

function validateEndpointId(id, idName) {
  num = validateNumber(id, idName);

  if (num < 1)
    throw new Error(`${idName || "Provided number"} is not a valid id.`);

  return num;
}

async function fetchData(url, options) {
  const response = await fetch(url, options);
  const json = await response.json();

  if (response.ok) {
    return json;
  } else {
    throw new Error(`${response.statusText}: ${json["error"]}`);
  }
}
