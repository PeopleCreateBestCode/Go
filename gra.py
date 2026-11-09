from enums import *
from plansza import Plansza


class Gra: ## Główna klasa, tutaj wszystko się dzieje
    def __init__(self, rozmiar: int, komi: float, sgf: str = "", debug: bool = False):
        self.plansza = Plansza(rozmiar, sgf)
        self.komi = komi
        self.rozmiar = rozmiar

        self.faza = "gra" 

        self.pas_czarny = False
        self.pas_bialy = False

        self.tura_czarny = True

        self.martwe = []  
        self.akceptacje = []

        self.punkty_czarne = 0
        self.punkty_biale = komi
        self.wygrywa = None

        if debug:
            self.plansza.debug_printuj_plansze(self.plansza.plansza)

    def przelicz(self):
        self.punkty_czarne, self.punkty_biale, _ = self.plansza.policz(self.martwe, self.komi)

    def klik(self, x, y):
        if self.faza != "gra":
            return False

        if x < 1 or y < 1 or x > self.rozmiar or y > self.rozmiar:
            return False

        if not self.plansza.postaw(y, x, self.tura_czarny):
            return False

        if self.tura_czarny:
            self.pas_czarny = False
        else:
            self.pas_bialy = False

        self.tura_czarny = not self.tura_czarny
        self.przelicz()
        return True

    def pas(self):
        if self.faza != "gra":
            return

        if self.tura_czarny:
            self.pas_czarny = True
        else:
            self.pas_bialy = True

        self.tura_czarny = not self.tura_czarny
        self.plansza.poprzednia = None  

        if self.pas_czarny and self.pas_bialy:
            self.faza = "liczenie"
            self.martwe = []
            self.akceptacje = []
            self.przelicz()

    def oznacz(self, x, y):
        if self.faza != "liczenie":
            return

        if x < 1 or y < 1 or x > self.rozmiar or y > self.rozmiar:
            return

        if self.plansza.plansza[y][x] not in (Tile.BLACK, Tile.WHITE):
            return

        kamienie, _ = self.plansza.grupa(y, x)

        if kamienie[0] in self.martwe:
            for k in kamienie:
                self.martwe.remove(k)
        else:
            self.martwe += kamienie

        self.akceptacje = []
        self.przelicz()

    def akceptuj(self, kolor):
        if self.faza != "liczenie" or kolor in self.akceptacje:
            return

        self.akceptacje.append(kolor)

        if len(self.akceptacje) == 2:
            self.faza = "koniec"
            self.przelicz()

            if self.punkty_czarne > self.punkty_biale:
                self.wygrywa = "czarny"
            elif self.punkty_biale > self.punkty_czarne:
                self.wygrywa = "biały"
            else:
                self.wygrywa = "nikt (remis)"

    def wznow(self):
        if self.faza != "liczenie":
            return

        self.faza = "gra"
        self.pas_czarny = False
        self.pas_bialy = False
        self.martwe = []
        self.akceptacje = []
        self.przelicz()

    def stan(self):
        if self.faza == "gra":
            plansza = self.plansza.plansza
        else:
            _, _, plansza = self.plansza.policz(self.martwe, self.komi)

        return {
            "rozmiar": self.rozmiar,
            "plansza": [[tile.name.lower() for tile in rzad[1:-1]] for rzad in plansza[1:-1]],
            "tura": "czarne" if self.tura_czarny else "biale",
            "faza": self.faza,
            "punkty_czarne": self.punkty_czarne,
            "punkty_biale": self.punkty_biale,
            "wygrywa": self.wygrywa,
            "akceptacje": self.akceptacje,
        }
