// szachownica ta sama co na lichess.org
import { Chessground } from "./lib/chessground/chessground.min.js";

const id = new URLSearchParams(location.search).get("id");
const API = "/api/szachy/" + id;

const statusEl = document.getElementById("status");
const historiaEl = document.getElementById("historia");
const promocjaEl = document.getElementById("promocja");
const remisEl = document.getElementById("remis");

let stan = null;
let wersja = -1;
let odebrano = 0; 

const plansza = Chessground(document.getElementById("szachownica"), {
  movable: {
    free: false,
    showDests: true,
    events: { after: poRuchu },
  },
  premovable: { enabled: true },
  animation: { duration: 200 },
  highlight: { lastMove: true, check: true },
});

function mozliweRuchy(ruchy) {
  const mapa = new Map();
  for (const pole in ruchy) {
    mapa.set(pole, ruchy[pole]);
  }
  return mapa;
}

function kolorCg(kolor) {
  if (kolor === "biale") return "white";
  if (kolor === "czarne") return "black";
  return undefined;
}

function rysuj(nowy) {
  if (stan && nowy.liczba_ruchow > stan.liczba_ruchow) {
    document.getElementById("dzwiek").play();
  }

  stan = nowy;
  wersja = stan.wersja;
  odebrano = performance.now();

  const moj = kolorCg(stan.ja);

  plansza.set({
    orientation: moj === "black" ? "black" : "white",
    fen: stan.fen,
    turnColor: kolorCg(stan.tura),
    lastMove: stan.ostatni || undefined,
    check: stan.szach,
    movable: {
      color: stan.status === "trwa" ? moj : undefined,
      dests: mozliweRuchy(stan.ruchy),
    },
  });

  if (stan.status !== "trwa") {
    plansza.cancelPremove();
  } else if (stan.tura === stan.ja) {
    plansza.playPremove(); 
  }

  const jaCzarne = stan.ja === "czarne";
  document.getElementById("dol-nazwa").textContent = jaCzarne ? stan.czarny : stan.bialy;
  document.getElementById("gora-nazwa").textContent = (jaCzarne ? stan.bialy : stan.czarny) || "...";

  if (stan.status === "czeka") {
    statusEl.textContent = "Czekam na przeciwnika";
  } else if (stan.status === "koniec") {
    statusEl.textContent = stan.wynik;
  } else if (stan.ja === null) {
    statusEl.textContent = "Ruch: " + (stan.tura === "biale" ? "białe" : "czarne");
  } else if (stan.tura === stan.ja) {
    statusEl.textContent = stan.szach ? "Szach! Twój ruch" : "Twój ruch";
  } else {
    statusEl.textContent = "Ruch przeciwnika";
  }

  if (stan.status === "trwa" && stan.remis && stan.remis !== stan.ja) {
    statusEl.textContent += "\nPrzeciwnik proponuje remis";
    remisEl.textContent = "Przyjmij remis";
  } else {
    remisEl.textContent = stan.remis === stan.ja ? "Zaproponowano remis" : "Zaproponuj remis";
  }
  remisEl.disabled = stan.remis === stan.ja;

  document.getElementById("przyciski-gry").hidden = !(stan.status === "trwa" && stan.ja !== null);
  historiaEl.textContent = stan.historia;

  pokazZegary();
}

function formatCzasu(sekundy) {
  if (sekundy < 10) {
    return sekundy.toFixed(1);
  }
  const min = Math.floor(sekundy / 60);
  const sek = Math.floor(sekundy % 60);
  return min + ":" + (sek < 10 ? "0" : "") + sek;
}

function pokazZegary() {
  const gora = document.getElementById("gora-zegar");
  const dol = document.getElementById("dol-zegar");

  if (stan === null || stan.czas === null) {
    gora.textContent = "";
    dol.textContent = "";
    return;
  }

  const czas = { biale: stan.czas.biale, czarne: stan.czas.czarne };
  if (stan.zegar) {
    czas[stan.zegar] = Math.max(0, czas[stan.zegar] - (performance.now() - odebrano) / 1000);
  }

  const dolKolor = stan.ja === "czarne" ? "czarne" : "biale";
  const goraKolor = dolKolor === "biale" ? "czarne" : "biale";

  dol.textContent = formatCzasu(czas[dolKolor]);
  gora.textContent = formatCzasu(czas[goraKolor]);
  dol.classList.toggle("chodzi", stan.zegar === dolKolor);
  gora.classList.toggle("chodzi", stan.zegar === goraKolor);
}

function wybierzFigure() {
  promocjaEl.hidden = false;
  return new Promise((gotowe) => {
    for (const przycisk of promocjaEl.querySelectorAll("button")) {
      przycisk.onclick = () => {
        promocjaEl.hidden = true;
        gotowe(przycisk.dataset.figura);
      };
    }
  });
}

async function poRuchu(skad, dokad, info) {
  let promocja = "";
  const figura = plansza.state.pieces.get(dokad);
  if (figura && figura.role === "pawn" && (dokad[1] === "8" || dokad[1] === "1")) {
    promocja = info.premove ? "q" : await wybierzFigure(); // przy premove zawsze hetman
  }

  try {
    const odp = await zapytanie(API + "/ruch", { ruch: skad + dokad + promocja });
    rysuj(odp.stan);
  } catch (blad) {
    rysuj(await zapytanie(API)); 
    statusEl.textContent = blad.message;
  }
}

async function petla() {
  while (true) {
    try {
      const nowy = await zapytanie(API + "?wersja=" + wersja);
      if (nowy.wersja !== wersja) {
        rysuj(nowy);
      }
    } catch (blad) {
      statusEl.textContent = blad.message;
      await new Promise((r) => setTimeout(r, 2000));
    }
  }
}

document.getElementById("poddaj").onclick = async () => {
  if (confirm("Na pewno się poddać?")) {
    rysuj((await zapytanie(API + "/poddaj", {})).stan);
  }
};

remisEl.onclick = async () => {
  rysuj((await zapytanie(API + "/remis", {})).stan);
};

document.getElementById("lobby").onclick = () => (location.href = "lobby.html?gra=szachy");

setInterval(pokazZegary, 100);
petla();
