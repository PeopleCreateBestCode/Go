from enums import *
from plansza import Plansza
import position_parser

class Gra: ## Główna klasa, tutaj wszystko się dzieje
    def __init__(self, rozmiar: int, komi: float, sgf: str = ""):
        self.plansza = Plansza(rozmiar, sgf)
        self.komi = komi
        self.gra_trwa = True
        
        self.plansza.debug_printuj_plansze(self.plansza.plansza)
    
    def graj(self, tura_czarny: bool = True):
        x = int(input("Podaj x: "))
        y = int(input("Podaj y: "))
        
        if x == 999 or y == 999:
            print(position_parser.create_sgf(self.plansza.plansza))
            x = int(input("Podaj x: "))
            y = int(input("Podaj y: "))
        
        self.plansza.zmien_pole(x, y, Tile.BLACK if tura_czarny else Tile.WHITE)
        
        self.plansza.sprawdz(tura_czarny)
        self.plansza.sprawdz(not tura_czarny)
        
        self.plansza.debug_printuj_plansze(self.plansza.plansza)
        
        self.graj(not tura_czarny)
    
    