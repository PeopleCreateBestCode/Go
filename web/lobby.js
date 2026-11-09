// lobby jest wspólne dla obu gier, gra=go albo gra=szachy w adresie
const szachy = new URLSearchParams(location.search).get("gra") === "szachy";
const API = szachy ? "/api/szachy" : "/api/gry";
const STRONA_GRY = szachy ? "szachy.html" : "index.html";

const lista = document.getElementById("lista");
const bladEl = document.getElementById("blad");

document.getElementById("tytul").textContent = szachy ? "Szachy" : "Go";
document.getElementById("wybor-czasu").hidden = !szachy;

async function odswiezListe() {
  const dane = await zapytanie(API);

  lista.innerHTML = "";

  if (dane.gry.length === 0) {
    lista.innerHTML = "<li>Brak gier, utwórz własną</li>";
    return;
  }

  for (const gra of dane.gry) {
    const li = document.createElement("li");
    li.textContent = "Gra gracza " + gra.gospodarz + (gra.czas ? " (" + gra.czas + ") " : " "); // textContent a nie innerHTML bo nazwę wpisuje gracz

    const przycisk = document.createElement("button");
    przycisk.textContent = "Dołącz";
    przycisk.onclick = () => dolacz(gra.id);

    li.append(przycisk);
    lista.append(li);
  }
}

async function dolacz(id) {
  try {
    await zapytanie(API + "/" + id + "/dolacz", {});
    location.href = STRONA_GRY + "?id=" + id;
  } catch (blad) {
    bladEl.textContent = blad.message;
  }
}

document.getElementById("utworz").onclick = async () => {
  let dane = {};
  if (szachy) {
    const [minuty, dodatek] = document.getElementById("czas").value.split("+");
    dane = { minuty: Number(minuty), dodatek: Number(dodatek) };
  }

  const odp = await zapytanie(API, dane);
  location.href = STRONA_GRY + "?id=" + odp.id;
};

document.getElementById("menu").onclick = () => (location.href = "menu.html");

odswiezListe();
setInterval(odswiezListe, 2000);
