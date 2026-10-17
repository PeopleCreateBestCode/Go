from enums import *
from plansza import Plansza
import position_parser
import pygame

class Gra: ## Główna klasa, tutaj wszystko się dzieje
    def __init__(self, rozmiar: int, komi: float, sgf: str = ""):
        self.plansza = Plansza(rozmiar, sgf)
        self.komi = komi
        self.gra_trwa = True
        
        self.pas_czarny = False
        self.pas_bialy = False
        
        pygame.init()
        
        self.screen = pygame.display.set_mode((800, 600))
        self.background = pygame.image.load("alt.png")

        self.white = pygame.image.load("white.jpeg")
        self.black = pygame.image.load("black.jpeg")

        self.rozmiar = rozmiar

        self.distance_pola = 25
        
        self.clickable = self.get_clicks()
        
        self.drukuj(self.plansza.plansza)
    
    def get_clicks(self):
        clickable = []
        
        for rzad in range(1, self.rozmiar + 1):
            for kolumna in range(1, self.rozmiar + 1):
                clickable.append((rzad * self.distance_pola, kolumna * self.distance_pola))
        
        return clickable

    def drukuj(self, plansza: list[list[Tile]]):
        
        self.plansza.debug_printuj_plansze(plansza)
        
        markers = [
            [(kolumna * self.distance_pola - 10, rzad * self.distance_pola - 10)
            for kolumna in range(0, self.rozmiar + 1)]
            for rzad in range(0, self.rozmiar + 1)
        ]

        self.screen.blit(self.background, (0, 0))

        for rzad in range(len(plansza)):
            for kolumna in range(len(plansza[rzad])):
                if plansza[rzad][kolumna] == Tile.WHITE:
                    self.screen.blit(self.white, markers[rzad][kolumna])
                elif plansza[rzad][kolumna] == Tile.BLACK:
                    self.screen.blit(self.black, markers[rzad][kolumna])

        pygame.display.flip()
    
    def find_nearest(self, lista: list[tuple[int, int]], val: tuple[int, int]):
        return min(
            range(len(lista)),
            key=lambda i: (lista[i][0] - val[0])**2 + (lista[i][1] - val[1])**2
        )
    
    def zacznij_gre(self):
        
        click = None
        running = True
        
        is_game = True
        
        tura_czarny = True
                
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    key = event.key
                    
                    if key == pygame.K_SPACE:
                        ## Pasowanie na spacji bo czemu nie
                        
                        if not is_game:
                            continue
                        
                        self.graj(0, 0, True, tura_czarny)
                        
                        self.drukuj(self.plansza.plansza)
                        
                        tura_czarny = not tura_czarny
                        
                        if self.pas_czarny and self.pas_bialy:
                            is_game = False
                        
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    click = event.pos  # (x, y) coordinates of the click
                    
                    self.drukuj(self.plansza.plansza)
                    
                    if not is_game:
                        continue
                    
                    near = self.find_nearest(self.clickable, click)
                    

                    x = self.clickable[near][0] // 25
                    y = self.clickable[near][1] // 25
                    
                    print(f"click id :({x}, {y})  px: {self.clickable[near]}")
                    
                    rez = self.graj(x, y, False, tura_czarny)
                    
                    print(rez)
                    
                    self.drukuj(self.plansza.plansza)
                    
                    if rez:
                        tura_czarny = not tura_czarny
                    
                    print(click)

            pygame.display.flip()

        pygame.quit()
    
    def graj(self,x:int, y: int, czy_pas: bool, tura_czarny: bool = True):
        
        if tura_czarny:
            self.pas_czarny = czy_pas
        else:
            self.pas_bialy = czy_pas
        
        if self.pas_czarny and self.pas_bialy:
            punkty_czarny, punkty_bialy, plansza = self.zakoncz_gre(tura_czarny)
            
            print(f"Punkty:\n\tCzarny: {punkty_czarny}\n\tBiały: {punkty_bialy} (Wliczone komi {self.komi})")
            
            return

        if not czy_pas:
            legalny = self.sprawdz_czy_legalny(y, x, tura_czarny)
            
            legalny = True
            
            if legalny:
                self.plansza.zmien_pole(x, y, Tile.BLACK if tura_czarny else Tile.WHITE)
                
                self.plansza.sprawdz(tura_czarny)
                self.plansza.sprawdz(not tura_czarny)
                
                return True
            else:
                print("NIELEGALNY RUCH!")
                return False   
        else:
            self.plansza.sprawdz(tura_czarny)
            self.plansza.sprawdz(not tura_czarny)
                            
            return True
    
    def sprawdz_czy_legalny(self, rzad: int, kolumna: int, czy_czarny: bool) -> bool:
        if self.plansza.plansza[rzad][kolumna] not in [Tile.EMPTY, Tile.WHITE_POINT, Tile.BLACK_POINT]:
            return False
        
        if not self.plansza.sprawdz_samobojstwo(rzad, kolumna, czy_czarny):
            return False
        
        return True
        
    def zakoncz_gre(self, czy_czarne: bool):
        verity = self.plansza.zaznacz_martwe_na_terytorium(czy_czarne)        
        
        verity_opposite = self.plansza.zaznacz_martwe_na_terytorium(not czy_czarne)
        
        for rzad in range(len(verity)):
            for kolumna in range(len(verity[rzad])):
                if verity_opposite[rzad][kolumna] in (Tile.BLACK_DEAD, Tile.WHITE_DEAD):
                    verity[rzad][kolumna] = verity_opposite[rzad][kolumna]
        
        self.plansza.debug_printuj_plansze(verity)
        
        punkty_czarny = self.plansza.bonus_za_zbicia_czarni
        punkty_bialy = self.plansza.bonus_za_zbicia_biali + self.komi
        
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
