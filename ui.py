import pygame
from enums import *
import gra

pygame.init()

screen = pygame.display.set_mode((800, 600))
background = pygame.image.load("background.png")

white = pygame.image.load("white.jpeg")
black = pygame.image.load("black.jpeg")

click = None
running = True

distance_pola = 25

def get_clicks():
    clickable = []
    
    for rzad in range(1,16):
        for kolumna in range(1,16):
            clickable.append((rzad * distance_pola, kolumna * distance_pola))
    
    return clickable

clickable = get_clicks()

def find_nearest(lista: list[tuple[int, int]], val: tuple[int, int]):
    return min(
        range(len(lista)),
        key=lambda i: (lista[i][0] - val[0])**2 + (lista[i][1] - val[1])**2
    )

def drukuj(plansza: list[list[Tile]]):
    markers = [
        [(kolumna * distance_pola - 10, rzad * distance_pola - 10)
        for kolumna in range(1, 16)]
        for rzad in range(1, 16)
    ]

    screen.blit(background, (0, 0))

    for rzad in range(len(plansza)):
        for kolumna in range(len(plansza[rzad])):
            if plansza[rzad][kolumna] == Tile.WHITE:
                screen.blit(white, markers[rzad][kolumna])
            elif plansza[rzad][kolumna] == Tile.BLACK:
                screen.blit(black, markers[rzad][kolumna])

    pygame.display.flip()

drukuj([
                [Tile.BLACK, Tile.BLACK],
                [Tile.WHITE, Tile.WHITE]
            ])

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click = event.pos  # (x, y) coordinates of the click
            
            drukuj([
                [Tile.BLACK, Tile.BLACK],
                [Tile.WHITE, Tile.WHITE]
            ])
            
            near = find_nearest(clickable, click)
            
            x = clickable[near][0]
            y = clickable[near][1]
            
            screen.blit(white, (x - 10, y - 10))
            
            print(click)

    pygame.display.flip()

pygame.quit()
