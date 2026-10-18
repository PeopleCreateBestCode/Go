from enums import *
from plansza import Plansza
import position_parser
import pygame
from button import Button
import gif_pygame

class Gra: ## Główna klasa, tutaj wszystko się dzieje
    def __init__(self, rozmiar: int, komi: float, sgf: str = "", debug: bool = False):
        self.plansza = Plansza(rozmiar, sgf)
        self.komi = komi
        self.gra_trwa = True
        
        self.pas_czarny = False
        self.pas_bialy = False
        
        self.rozmiar = rozmiar
        
        if debug:
            self.plansza.debug_printuj_plansze(self.plansza.plansza)
            
            return
        
        ## Sekcja klasy PYGAME 
        
        pygame.init()
        
        self.screen = pygame.display.set_mode((800, 600))
        self.background = pygame.image.load("alt.png")
        
        pygame.event.set_grab(False)
        pygame.mouse.set_visible(True)

        self.white = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(self.white, (255, 255, 255), (10, 10), 10)

        self.black = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(self.black, (0, 0, 0), (10, 10), 10)
        
        
        self.white_crossed = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(self.white_crossed, (255, 255, 255), (10, 10), 10)
        pygame.draw.line(self.white_crossed, (255, 0, 0), (4, 4), (16, 16), 2)
        pygame.draw.line(self.white_crossed, (255, 0, 0), (16, 4), (4, 16), 2)

        self.black_crossed = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(self.black_crossed, (0, 0, 0), (10, 10), 10)
        pygame.draw.line(self.black_crossed, (255, 0, 0), (4, 4), (16, 16), 2)
        pygame.draw.line(self.black_crossed, (255, 0, 0), (16, 4), (4, 16), 2)
        
        
        self.black_point = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.rect(self.black_point, (0, 0, 0), (5, 5, 10, 10))
        self.white_point = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.rect(self.white_point, (255, 255, 255), (5, 5, 10, 10))



        self.distance_pola = 25
        
        self.clickable = self.get_clicks()
        
        self.czy_pas_wcisniety = False
        
        self.pass_gif = gif_pygame.load("pass.gif")
        
        self.buttons: list[Button] = [
            Button((450, 100), (216, 96), self.white, self.pas)
        ]
        
        self.drukuj(self.plansza.plansza)
    
    def pas(self):
        print("Pass")
        if self.gra_trwa:
            self.czy_pas_wcisniety = True
    
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
                elif plansza[rzad][kolumna] == Tile.WHITE_DEAD:
                    self.screen.blit(self.white_crossed, markers[rzad][kolumna])
                elif plansza[rzad][kolumna] == Tile.BLACK_DEAD:
                    self.screen.blit(self.black_crossed, markers[rzad][kolumna])
                elif plansza[rzad][kolumna] == Tile.WHITE_POINT and not self.gra_trwa:
                    self.screen.blit(self.white_point, markers[rzad][kolumna])
                elif plansza[rzad][kolumna] == Tile.BLACK_POINT and not self.gra_trwa:
                    self.screen.blit(self.black_point, markers[rzad][kolumna])
                            
                

        pygame.display.flip()
    
    def find_nearest(self, lista: list[tuple[int, int]], val: tuple[int, int]):
        return min(
            range(len(lista)),
            key=lambda i: (lista[i][0] - val[0])**2 + (lista[i][1] - val[1])**2
        )
    
    def zacznij_gre(self):
        
        click = None
        running = True
        
        tura_czarny = True
                
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN :
                    key = event.key
                    
                    if key == pygame.K_SPACE:
                        ## Pasowanie na spacji bo czemu nie
                        
                        if not self.gra_trwa:
                            continue
                        
                        self.czy_pas_wcisniety = True
                        
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    click = event.pos  # (x, y) coordinates of the click
                    
                    self.drukuj(self.plansza.plansza)
                    
                    cont = False
                    
                    for btn in self.buttons:
                        if btn.check_and_click(click):
                            cont = True
                        
                    if cont:
                        continue
                    
                    if not self.gra_trwa:
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
                    
                    click = None
                
                elif self.czy_pas_wcisniety and self.gra_trwa:
                    self.czy_pas_wcisniety = False
                    
                    self.graj(0, 0, True, tura_czarny)
                                            
                    self.drukuj(self.plansza.plansza)
                    
                    tura_czarny = not tura_czarny
                    
                    if self.pas_czarny and self.pas_bialy:
                        self.gra_trwa = False

            self.pass_gif.render(self.screen, (450, 100))
            
            pygame.display.flip()

        pygame.quit()
    
    def graj(self,x:int, y: int, czy_pas: bool, tura_czarny: bool = True, debug: bool = False):
        
        if debug:
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
            legalny = self.sprawdz_czy_legalny(y, x, tura_czarny)
            
            if legalny:
                if debug:
                    self.plansza.debug_printuj_plansze(self.plansza.plansza)
                    self.graj(-1, -1, False, not tura_czarny, True)
                
                return True
            else:
                print("NIELEGALNY RUCH!")
                
                if debug:
                    self.plansza.debug_printuj_plansze(self.plansza.plansza)
                    self.graj(-1, -1, False, tura_czarny, True)
                return False   
        else:
            self.plansza.sprawdz(tura_czarny)
            self.plansza.sprawdz(not tura_czarny)
                            
            if debug:
                self.plansza.debug_printuj_plansze(self.plansza.plansza)
                self.graj(-1, -1, False, not tura_czarny, True)
                
            return True
    
    def sprawdz_czy_legalny(self, rzad: int, kolumna: int, czy_czarny: bool) -> bool:
        if self.plansza.plansza[rzad][kolumna] not in [Tile.EMPTY, Tile.WHITE_POINT, Tile.BLACK_POINT]:
            return False
        
        if not self.plansza.sprawdz_samobojstwo(rzad, kolumna, czy_czarny):
            return False
        
        return True
        
    def zakoncz_gre(self, czy_czarne: bool):
        self.gra_trwa = False
        
        verity = self.plansza.zaznacz_martwe_na_terytorium(czy_czarne)        
        
        verity_opposite = self.plansza.zaznacz_martwe_na_terytorium(not czy_czarne)
        
        for rzad in range(len(verity)):
            for kolumna in range(len(verity[rzad])):
                if verity_opposite[rzad][kolumna] in (Tile.BLACK_DEAD, Tile.WHITE_DEAD):
                    verity[rzad][kolumna] = verity_opposite[rzad][kolumna]
        
        self.plansza.debug_printuj_plansze(verity)
        
        punkty_czarny = 0
        punkty_bialy = 0 + self.komi
        
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
