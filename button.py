import pygame
from typing import Callable

class Button:
    def __init__(
        self,
        pos: tuple[int, int],
        size: tuple[int, int],
        source: pygame.Surface,
        action: Callable[[], None]
    ):
        self.pos = pos
        self.size = size
        self.source = source
        self.action = action
        
        self.x, self.y = self.pos
        
        self.max_x = self.x + self.size[0]
        self.max_y = self.y + self.size[1]
        
    def check_and_click(self, click: tuple[int, int]):

        other_x, other_y = click
        
        if self.x <= other_x <= self.max_x and self.y <= other_y <= self.max_y:
            self.action()
            
            return True
        
        return False
        
        
