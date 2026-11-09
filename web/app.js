const id = new URLSearchParams(location.search).get("id");
const API = "/api/gry/" + id;

const planszaEl = document.getElementById("plansza");
const graczeEl = document.getElementById("gracze");
const turaEl = document.getElementById("tura");
const pasEl = document.getElementById("pas");
const liczenieEl = document.getElementById("liczenie");
const czarneEl = document.getElementById("czarne");
const bialeEl = document.getElementById("biale");
const ikonaEl = document.getElementById("ikona");
const muzykaEl = document.getElementById("muzyka");

const CZARNY_KAMIEN_IKONA = ikonaEl.href;

let stan = null;
let pola = [];
let masha = false;

function zbudujPlansze(rozmiar) {
  planszaEl.innerHTML = "";
  planszaEl.style.setProperty("--n", rozmiar);
  pola = [];

  const h = rozmiar >= 13 ? 4 : 3; 

  for (let y = 1; y <= rozmiar; y++) {
    const rzad = [];

    for (let x = 1; x <= rozmiar; x++) {
      const pole = document.createElement("div");
      pole.className = "pole";

      if (x === 1) pole.classList.add("lewa");
      if (x === rozmiar) pole.classList.add("prawa");
      if (y === 1) pole.classList.add("gora");
      if (y === rozmiar) pole.classList.add("dol");
      if ((x === h || x === rozmiar + 1 - h) && (y === h || y === rozmiar + 1 - h)) pole.classList.add("hoshi");

      pole.innerHTML = '<span class="kamien"></span>';
      pole.onclick = () => kliknij(x, y);

      planszaEl.append(pole);
      rzad.push(pole);
    }

    pola.push(rzad);
  }
}

function rysuj(nowy) {
  if (stan === null || stan.rozmiar !== nowy.rozmiar) {
    zbudujPlansze(nowy.rozmiar);
  }

  stan = nowy;

  for (let y = 0; y < stan.rozmiar; y++) {
    for (let x = 0; x < stan.rozmiar; x++) {
      pola[y][x].dataset.pole = stan.plansza[y][x];
    }
  }

  planszaEl.classList.toggle("koniec", stan.faza !== "gra");

  graczeEl.textContent = "Czarne: " + stan.czarny + "\nBiałe: " + (stan.bialy || "...");

  if (stan.status === "czeka") {
    turaEl.textContent = "Czekam na przeciwnika";
  } else if (stan.status === "liczenie") {
    if (stan.akceptacje.includes(stan.ja)) {
      turaEl.textContent = "Czekam aż przeciwnik zaakceptuje wynik";
    } else {
      turaEl.textContent = "Kliknij martwe kamienie i zaakceptuj wynik";
    }
  } else if (stan.status === "koniec") {
    turaEl.textContent = "Koniec gry\nWygrywa " + stan.wygrywa;
  } else if (stan.ja === null) {
    turaEl.textContent = "Tura: " + (stan.tura === "czarne" ? "Czarne" : "Białe");
  } else {
    turaEl.textContent = stan.tura === stan.ja ? "Twój ruch" : "Ruch przeciwnika";
  }

  czarneEl.textContent = "Czarne: " + stan.punkty_czarne;
  bialeEl.textContent = "Białe: " + stan.punkty_biale;

  pasEl.disabled = !(stan.status === "trwa" && stan.tura === stan.ja);
  liczenieEl.hidden = !(stan.status === "liczenie" && stan.ja !== null);
}

function zagraj(kolor) {
  const dzwiek = document.getElementById("dzwiek-" + kolor);
  dzwiek.currentTime = 0;
  dzwiek.play();
}

async function akcja(adres, dane) {
  try {
    const odp = await zapytanie(adres, dane);
    rysuj(odp.stan);
    return odp;
  } catch (blad) {
    turaEl.textContent = blad.message;
  }
}

async function kliknij(x, y) {
  if (stan === null) return;

  if (stan.status === "liczenie") {
    akcja(API + "/oznacz", { x: x, y: y });
    return;
  }

  if (stan.status !== "trwa" || stan.tura !== stan.ja) return;

  const odp = await akcja(API + "/ruch", { x: x, y: y });
  if (odp && odp.legalny) {
    zagraj(odp.kolor);
  }
}

function pasuj() {
  if (stan && stan.status === "trwa" && stan.tura === stan.ja) {
    akcja(API + "/pas", {});
  }
}

// co sekundę pobieramy stan żeby zobaczyć ruch przeciwnika
async function odswiez() {
  try {
    const nowy = await zapytanie(API);

    // przeciwnik się ruszył
    if (stan && stan.ja && nowy.faza === "gra" && stan.tura !== stan.ja && nowy.tura === stan.ja) {
      zagraj(stan.ja === "czarne" ? "biale" : "czarne");
    }

    rysuj(nowy);
  } catch (blad) {
    turaEl.textContent = blad.message;
  }
}

function przelaczMashe() {
  masha = !masha;

  document.body.classList.toggle("masha", masha);
  document.title = masha ? "Go: Masha edition" : "Go";
  ikonaEl.href = masha ? "../assets/img/masha.jpeg" : CZARNY_KAMIEN_IKONA;

  if (masha) {
    muzykaEl.currentTime = 0;
    muzykaEl.play();
  } else {
    muzykaEl.pause();
  }
}

pasEl.onclick = pasuj;
document.getElementById("akceptuj").onclick = () => akcja(API + "/akceptuj", {});
document.getElementById("wznow").onclick = () => akcja(API + "/wznow", {});
document.getElementById("lobby").onclick = () => (location.href = "lobby.html?gra=go");
document.getElementById("masha").onclick = przelaczMashe;

document.addEventListener("keydown", (e) => {
  if (e.code === "Space") {
    e.preventDefault();
    pasuj(); // Pasowanie na spacji bo czemu nie
  }
});

odswiez();
setInterval(odswiez, 1000);
