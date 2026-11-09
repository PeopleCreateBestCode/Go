import time

import chess 


class Partia: 
    def __init__(self, id, bialy, minuty, dodatek):
        self.id = id
        self.bialy = bialy 
        self.czarny = None

        self.plansza = chess.Board()

        self.czas = None
        if minuty > 0:
            self.czas = {"biale": minuty * 60.0, "czarne": minuty * 60.0}
        self.dodatek = dodatek
        self.start = None  

        self.wynik = None
        self.remis = None  
        self.wersja = 0 

    def tura(self):
        return "biale" if self.plansza.turn == chess.WHITE else "czarne"

    def kolor_gracza(self, id_gracza):
        if id_gracza == self.bialy["id"]:
            return "biale"
        if self.czarny is not None and id_gracza == self.czarny["id"]:
            return "czarne"
        return None

    def status(self):
        if self.czarny is None:
            return "czeka"
        if self.wynik is None:
            return "trwa"
        return "koniec"

    def zegar_chodzi(self):
        return self.czas is not None and self.status() == "trwa" and len(self.plansza.move_stack) >= 2

    def zostalo(self, kolor):
        t = self.czas[kolor]
        if self.zegar_chodzi() and kolor == self.tura():
            t -= time.time() - self.start
        return max(t, 0)

    def koniec(self, wynik):
        self.wynik = wynik
        self.wersja += 1

    def sprawdz_czas(self):
        if not self.zegar_chodzi() or self.zostalo(self.tura()) > 0:
            return False

        przegrany = self.tura()
        self.czas[przegrany] = 0

        wygrany = chess.BLACK if przegrany == "biale" else chess.WHITE
        if self.plansza.has_insufficient_material(wygrany):
            self.koniec("Koniec czasu, ale remis")
        elif przegrany == "biale":
            self.koniec("Białym skończył się czas")
        else:
            self.koniec("Czarnym skończył się czas")
        return True

    def ile_do_konca_czasu(self):
        if not self.zegar_chodzi():
            return None
        return self.zostalo(self.tura())

    def ruch(self, kolor, uci):
        if self.status() != "trwa" or kolor != self.tura():
            return False
        if self.sprawdz_czas():
            return False

        try:
            ruch = chess.Move.from_uci(uci)
        except ValueError:
            return False
        if ruch not in self.plansza.legal_moves:
            return False

        if self.zegar_chodzi():
            self.czas[kolor] = self.zostalo(kolor) + self.dodatek

        self.plansza.push(ruch)
        self.start = time.time()
        self.remis = None
        self.wersja += 1

        koniec = self.plansza.outcome(claim_draw=True)
        if koniec is not None:
            if koniec.termination == chess.Termination.CHECKMATE:
                self.koniec("Mat Wygrywają " + ("białe" if koniec.winner == chess.WHITE else "czarne"))
            elif koniec.termination == chess.Termination.STALEMATE:
                self.koniec("Pat")
            elif koniec.termination == chess.Termination.INSUFFICIENT_MATERIAL:
                self.koniec("Za mało figur - remis")
            elif koniec.termination in (chess.Termination.THREEFOLD_REPETITION, chess.Termination.FIVEFOLD_REPETITION):
                self.koniec("remis przez powtorzenie")
            else:
                self.koniec("50 move rule")

        return True

    def poddaj(self, kolor):
        if self.status() == "trwa":
            if kolor == "biale":
                self.koniec("Białe się poddały")
            else:
                self.koniec("Czarne się poddały")

    def zaproponuj_remis(self, kolor):
        if self.status() != "trwa":
            return
        if self.remis is not None and self.remis != kolor:
            self.koniec("Remis za zgodą graczy")
        else:
            self.remis = kolor
            self.wersja += 1

    def stan(self, id_gracza):
        ruchy = {} # format e4 f5 itd
        if self.status() == "trwa":
            for r in self.plansza.legal_moves:
                skad = chess.square_name(r.from_square)
                dokad = chess.square_name(r.to_square)
                ruchy.setdefault(skad, [])
                if dokad not in ruchy[skad]:
                    ruchy[skad].append(dokad)

        ostatni = None
        if self.plansza.move_stack:
            r = self.plansza.peek()
            ostatni = [chess.square_name(r.from_square), chess.square_name(r.to_square)]

        czas = None
        if self.czas is not None:
            czas = {"biale": self.zostalo("biale"), "czarne": self.zostalo("czarne")}

        return {
            "fen": self.plansza.fen(),
            "tura": self.tura(),
            "ruchy": ruchy,
            "ostatni": ostatni,
            "szach": self.plansza.is_check(),
            "historia": self.plansza.root().variation_san(self.plansza.move_stack),
            "liczba_ruchow": len(self.plansza.move_stack),
            "czas": czas,
            "zegar": self.tura() if self.zegar_chodzi() else None,
            "bialy": self.bialy["nazwa"],
            "czarny": self.czarny["nazwa"] if self.czarny else None,
            "ja": self.kolor_gracza(id_gracza),
            "status": self.status(),
            "wynik": self.wynik,
            "remis": self.remis,
            "wersja": self.wersja,
        }
