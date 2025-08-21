import pygame

class Tile : 
    def __init__(self,type,x,y,ramp = 0) -> None:
        self.image = pygame.transform.scale(pygame.image.load("data/tiles/" + type + ".jpeg"),(50,50))
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x,y)
        self.ramp = ramp # 1 => left facing ramp      2 => right facing ramp     3 => width = 2*height ramp
    def draw(self, screen, camera_x, camera_y) :
        screen.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))
        
def load_map(path) :
    file = open(path + ".txt","r")
    data = file.read()
    file.close()
    data = data.split('\n')
    game_map = []
    for row in data :
        game_map.append(list(row))
    return game_map
