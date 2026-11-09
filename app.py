import os
import secrets
import threading
import time

from flask import Flask, jsonify, request, redirect, send_from_directory, session

from gra import Gra
from pokoj import Pokoj
from szachy import Partia

ROZMIAR_PLANSZY = 16
KOMI = 6.5

app = Flask(__name__, static_folder="web", static_url_path="/web")
app.secret_key = os.environ.get("SECRET_KEY") or secrets.token_hex(32)

pokoje = {}
partie = {}  
blokada = threading.Lock()  
zmiana = threading.Condition(blokada)  


def blad(tekst, kod):
    return jsonify({"blad": tekst}), kod


def znajdz_pokoj(id_pokoju):
    if "id" not in session:
        return None, None, blad("Nie jesteś zalogowany", 401)

    pokoj = pokoje.get(id_pokoju)
    if pokoj is None:
        return None, None, blad("Nie ma takiej gry", 404)

    return pokoj, pokoj.kolor_gracza(session["id"]), None


def stan_pokoju(pokoj):
    stan = pokoj.gra.stan()
    stan["czarny"] = pokoj.czarny["nazwa"]
    stan["bialy"] = pokoj.bialy["nazwa"] if pokoj.bialy else None
    stan["ja"] = pokoj.kolor_gracza(session["id"])
    stan["status"] = pokoj.status()
    return stan


def wez_xy():
    dane = request.get_json(silent=True) or {}
    try:
        return int(dane["x"]), int(dane["y"])
    except (KeyError, ValueError, TypeError):
        return None, None


@app.route("/")
def strona_glowna():
    return redirect("/web/login.html")


@app.route("/assets/<path:plik>")
def assets(plik):
    return send_from_directory("assets", plik)


@app.route("/api/login", methods=["POST"])
def login():
    dane = request.get_json(silent=True) or {}
    nazwa = str(dane.get("nazwa", "")).strip()

    if nazwa == "":
        return blad("Podaj nazwę", 400)
    if len(nazwa) > 20:
        return blad("Za długa nazwa (max 20 znaków)", 400)

    if "id" not in session:
        session["id"] = secrets.token_hex(8)  
    session["nazwa"] = nazwa
    session.permanent = True

    return jsonify({"nazwa": nazwa})


@app.route("/api/ja")
def ja():
    if "id" not in session:
        return blad("Nie jesteś zalogowany", 401)
    return jsonify({"nazwa": session["nazwa"]})


@app.route("/api/wyloguj", methods=["POST"])
def wyloguj():
    session.clear()
    return jsonify({"ok": True})


@app.route("/api/gry", methods=["GET"])
def lista_gier():
    if "id" not in session:
        return blad("Nie jesteś zalogowany", 401)

    gry = []
    with blokada:
        for pokoj in pokoje.values():
            if pokoj.status() == "czeka":
                gry.append({"id": pokoj.id, "gospodarz": pokoj.czarny["nazwa"]})

    return jsonify({"gry": gry})


@app.route("/api/gry", methods=["POST"])
def nowa_gra():
    if "id" not in session:
        return blad("Nie jesteś zalogowany", 401)

    id_pokoju = secrets.token_urlsafe(6)
    gracz = {"id": session["id"], "nazwa": session["nazwa"]}

    with blokada:
        pokoje[id_pokoju] = Pokoj(id_pokoju, Gra(ROZMIAR_PLANSZY, KOMI), gracz)

    return jsonify({"id": id_pokoju})


@app.route("/api/gry/<id_pokoju>/dolacz", methods=["POST"])
def dolacz(id_pokoju):
    with blokada:
        pokoj, kolor, b = znajdz_pokoj(id_pokoju)
        if b:
            return b

        if kolor is None:
            if pokoj.bialy is not None:
                return blad("Gra jest pełna", 409)
            pokoj.bialy = {"id": session["id"], "nazwa": session["nazwa"]}

    return jsonify({"id": id_pokoju})


@app.route("/api/gry/<id_pokoju>")
def stan_gry(id_pokoju):
    with blokada:
        pokoj, kolor, b = znajdz_pokoj(id_pokoju)
        if b:
            return b
        return jsonify(stan_pokoju(pokoj))


@app.route("/api/gry/<id_pokoju>/ruch", methods=["POST"])
def ruch(id_pokoju):
    x, y = wez_xy()
    if x is None:
        return blad("Zły ruch", 400)

    with blokada:
        pokoj, kolor, b = znajdz_pokoj(id_pokoju)
        if b:
            return b

        if pokoj.status() != "trwa":
            return blad("Teraz nie można stawiać kamieni", 409)
        if kolor != pokoj.gra.stan()["tura"]:
            return blad("Nie twoja tura", 403)

        legalny = pokoj.gra.klik(x, y)
        return jsonify({"legalny": legalny, "kolor": kolor, "stan": stan_pokoju(pokoj)})


@app.route("/api/gry/<id_pokoju>/pas", methods=["POST"])
def pas(id_pokoju):
    with blokada:
        pokoj, kolor, b = znajdz_pokoj(id_pokoju)
        if b:
            return b

        if pokoj.status() != "trwa":
            return blad("Teraz nie można pasować", 409)
        if kolor != pokoj.gra.stan()["tura"]:
            return blad("Nie twoja tura", 403)

        pokoj.gra.pas()
        return jsonify({"stan": stan_pokoju(pokoj)})



@app.route("/api/gry/<id_pokoju>/oznacz", methods=["POST"])
def oznacz(id_pokoju):
    x, y = wez_xy()
    if x is None:
        return blad("Zły ruch", 400)

    with blokada:
        pokoj, kolor, b = znajdz_pokoj(id_pokoju)
        if b:
            return b
        if kolor is None:
            return blad("Nie grasz w tej grze", 403)

        pokoj.gra.oznacz(x, y)
        return jsonify({"stan": stan_pokoju(pokoj)})


@app.route("/api/gry/<id_pokoju>/akceptuj", methods=["POST"])
def akceptuj(id_pokoju):
    with blokada:
        pokoj, kolor, b = znajdz_pokoj(id_pokoju)
        if b:
            return b
        if kolor is None:
            return blad("Nie grasz w tej grze", 403)

        pokoj.gra.akceptuj(kolor)
        return jsonify({"stan": stan_pokoju(pokoj)})


@app.route("/api/gry/<id_pokoju>/wznow", methods=["POST"])
def wznow(id_pokoju):
    with blokada:
        pokoj, kolor, b = znajdz_pokoj(id_pokoju)
        if b:
            return b
        if kolor is None:
            return blad("Nie grasz w tej grze", 403)

        pokoj.gra.wznow()
        return jsonify({"stan": stan_pokoju(pokoj)})



def znajdz_partie(id_partii):
    if "id" not in session:
        return None, None, blad("Nie jesteś zalogowany", 401)

    partia = partie.get(id_partii)
    if partia is None:
        return None, None, blad("Nie ma takiej gry", 404)

    return partia, partia.kolor_gracza(session["id"]), None


@app.route("/api/szachy", methods=["GET"])
def lista_partii():
    if "id" not in session:
        return blad("Nie jesteś zalogowany", 401)

    gry = []
    with blokada:
        for partia in partie.values():
            if partia.status() == "czeka":
                czas = "bez czasu"
                if partia.czas is not None:
                    czas = f"{int(partia.czas['biale'] // 60)}+{partia.dodatek}"
                gry.append({"id": partia.id, "gospodarz": partia.bialy["nazwa"], "czas": czas})

    return jsonify({"gry": gry})


@app.route("/api/szachy", methods=["POST"])
def nowa_partia():
    if "id" not in session:
        return blad("Nie jesteś zalogowany", 401)

    dane = request.get_json(silent=True) or {}
    try:
        minuty = int(dane.get("minuty", 5))
        dodatek = int(dane.get("dodatek", 0))
    except (ValueError, TypeError):
        return blad("Zły czas", 400)
    if minuty < 0 or minuty > 60 or dodatek < 0 or dodatek > 60:
        return blad("Zły czas", 400)

    id_partii = secrets.token_urlsafe(6)
    gracz = {"id": session["id"], "nazwa": session["nazwa"]}

    with blokada:
        partie[id_partii] = Partia(id_partii, gracz, minuty, dodatek)

    return jsonify({"id": id_partii})


@app.route("/api/szachy/<id_partii>/dolacz", methods=["POST"])
def dolacz_szachy(id_partii):
    with blokada:
        partia, kolor, b = znajdz_partie(id_partii)
        if b:
            return b

        if kolor is None:
            if partia.czarny is not None:
                return blad("Gra jest pełna", 409)
            partia.czarny = {"id": session["id"], "nazwa": session["nazwa"]}
            partia.wersja += 1
            zmiana.notify_all()

    return jsonify({"id": id_partii})


@app.route("/api/szachy/<id_partii>")
def stan_partii(id_partii):
    wersja = request.args.get("wersja", type=int)

    with zmiana:
        partia, kolor, b = znajdz_partie(id_partii)
        if b:
            return b

        koniec_czekania = time.time() + 25
        while wersja == partia.wersja:
            czekaj = koniec_czekania - time.time()

            do_konca_czasu = partia.ile_do_konca_czasu()
            if do_konca_czasu is not None:
                czekaj = min(czekaj, do_konca_czasu + 0.05) 

            if czekaj <= 0:
                break
            zmiana.wait(czekaj)

            if partia.sprawdz_czas():
                zmiana.notify_all()

        if partia.sprawdz_czas():
            zmiana.notify_all()

        return jsonify(partia.stan(session["id"]))


@app.route("/api/szachy/<id_partii>/ruch", methods=["POST"])
def ruch_szachy(id_partii):
    dane = request.get_json(silent=True) or {}

    with blokada:
        partia, kolor, b = znajdz_partie(id_partii)
        if b:
            return b
        if kolor is None:
            return blad("Nie grasz w tej grze", 403)

        if not partia.ruch(kolor, str(dane.get("ruch", ""))):
            zmiana.notify_all()  ## mógł się skończyć czas
            return blad("Nie można zrobić tego ruchu", 409)

        zmiana.notify_all()
        return jsonify({"stan": partia.stan(session["id"])})


@app.route("/api/szachy/<id_partii>/poddaj", methods=["POST"])
def poddaj(id_partii):
    with blokada:
        partia, kolor, b = znajdz_partie(id_partii)
        if b:
            return b
        if kolor is None:
            return blad("Nie grasz w tej grze", 403)

        partia.poddaj(kolor)
        zmiana.notify_all()
        return jsonify({"stan": partia.stan(session["id"])})


@app.route("/api/szachy/<id_partii>/remis", methods=["POST"])
def remis(id_partii):
    with blokada:
        partia, kolor, b = znajdz_partie(id_partii)
        if b:
            return b
        if kolor is None:
            return blad("Nie grasz w tej grze", 403)

        partia.zaproponuj_remis(kolor)
        zmiana.notify_all()
        return jsonify({"stan": partia.stan(session["id"])})


if __name__ == "__main__":
    app.run(debug=True, port=8000)
