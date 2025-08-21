import pygame

class Portal :
    def __init__(self,x, y, flip = False ):
        self.images = []
        for _ in range(9) : 
            self.images.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load("data/portal/" + str(_+1) + ".png"),(50,80)),flip,False))
        self.current_image = 0
        self.image = self.images[self.current_image]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x,y)
        
    def animate(self, speed):
        self.current_image += speed
        self.current_image = round(self.current_image,1)
        if self.current_image >= len(self.images) :
            self.current_image = 0
        self.image = self.images[int(self.current_image)]
    
    def draw(self, screen, camera_x, camera_y) :
        screen.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))
        
        