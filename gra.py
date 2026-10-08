from enums import *
from plansza import Plansza
import position_parser
import copy

class Gra: ## Główna klasa, tutaj wszystko się dzieje
    def __init__(self, rozmiar: int, komi: float, sgf: str = ""):
        self.plansza = Plansza(rozmiar, sgf)
        self.komi = komi
        self.gra_trwa = True
        
        self.pas_czarny = False
        self.pas_bialy = False
        
        self.plansza.debug_printuj_plansze(self.plansza.plansza)
    
    def graj(self, tura_czarny: bool = True):
        x = int(input("Podaj x: "))
        y = int(input("Podaj y: "))
        
        if x == 999 or y == 999:
            print(position_parser.create_sgf(self.plansza.plansza))
            x = int(input("Podaj x: "))
            y = int(input("Podaj y: "))
            
        czy_pas = x == 0 or y == 0
        
        if tura_czarny:
            self.pas_czarny = czy_pas
        else:
            self.pas_bialy = czy_pas
        
        if self.pas_czarny and self.pas_bialy:
            punkty_czarny, punkty_bialy, plansza = self.zakoncz_gre(tura_czarny)
            
            print(f"Punkty:\n\tCzarny: {punkty_czarny}\n\tBiały: {punkty_bialy} (Wliczone komi {self.komi})")
            
            return

        if not czy_pas:
            self.plansza.zmien_pole(x, y, Tile.BLACK if tura_czarny else Tile.WHITE) 
        
        self.plansza.sprawdz(tura_czarny)
        self.plansza.sprawdz(not tura_czarny)
        
        self.plansza.debug_printuj_plansze(self.plansza.plansza)
        
        self.graj(not tura_czarny)
    
    def zakoncz_gre(self, czy_czarne: bool):
        verity = self.plansza.zaznacz_martwe_na_terytorium(czy_czarne)        
        
        verity_opposite = self.plansza.zaznacz_martwe_na_terytorium(not czy_czarne)
        
        for rzad in range(len(verity)):
            for kolumna in range(len(verity[rzad])):
                if verity_opposite[rzad][kolumna] in (Tile.BLACK_DEAD, Tile.WHITE_DEAD):
                    verity[rzad][kolumna] = verity_opposite[rzad][kolumna]
        
        self.plansza.debug_printuj_plansze(verity)
        
        punkty_czarny = self.plansza.bonus_za_zbicia_czarni
        punkty_bialy = self.plansza.bonus_za_zbicia_biali  + self.komi
        
        for rzad in range(len(verity)):
            for kolumna in range(len(verity[rzad])):
                if verity[rzad][kolumna] == Tile.WHITE_POINT:
                    punkty_bialy += 1
                elif verity[rzad][kolumna] == Tile.BLACK_POINT:
                    punkty_czarny += 1
                elif verity[rzad][kolumna] == Tile.WHITE_DEAD:
                    punkty_czarny += 2
                elif verity[rzad][kolumna] == Tile.BLACK_DEAD:
                    punkty_bialy += 2
        
        return punkty_czarny, punkty_bialy, verity
