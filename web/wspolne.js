async function zapytanie(adres, dane) {
  let opcje = {};
  if (dane !== undefined) {
    opcje = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(dane),
    };
  }

  const odp = await fetch(adres, opcje);
  const json = await odp.json();

  if (odp.status === 401) {
    location.href = "login.html";
  }
  if (!odp.ok) {
    throw new Error(json.blad);
  }

  return json;
}
