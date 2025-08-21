import pygame
from random import choice

class Robot : 
    def __init__(self,x, y, tiles_path):
        self.right_running_images = []
        self.left_running_images = []
        self.right_idling_images = []
        self.left_idling_images = []
        for _ in range(3) : 
            self.right_running_images.append(pygame.transform.scale(pygame.image.load("data/robot/running"+  str(_ + 1) + ".png"),(50,50)))
            self.left_running_images.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load("data/robot/running" + str(_ + 1) + ".png"),(50,50)),True,False))
            self.right_idling_images.append(pygame.transform.scale(pygame.image.load("data/robot/idling" + str(_ + 1) + ".png"), (50,50)))
            self.left_idling_images.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load("data/robot/idling" + str(_ + 1) + ".png"), (50,50)),True,False))
        self.current_image = 0
        self.image = self.right_running_images[self.current_image]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x,y)
        self.movement = 0
        self.movement_direction = choice(["right","left"])
        self.previous_movement = self.movement_direction
        self.tiles_path = tiles_path
        self.idling_timer = 0
        
    def move(self) : 

        if self.movement_direction == "left" : 
            self.movement = -2
            self.animate(self.left_running_images, .2)
        elif self.movement_direction == "right" : 
            self.movement = 2
            self.animate(self.right_running_images, .2)
        else : 
            if self.previous_movement == "left" : 
                self.animate(self.left_idling_images, .2)
            elif self.previous_movement == "right" : 
                self.animate(self.right_idling_images, .2)
            self.movement = 0
        
        self.previous_movement = self.movement_direction
        
        self.rect.x += self.movement
        
        if self.rect.left <= self.tiles_path[0].rect.right : 
            if self.movement_direction != "right" : 
                self.movement_direction = None
                self.idling_timer += 1
                if self.idling_timer >= 180 : 
                    self.idling_timer = 0
                    self.movement_direction = "right"
                    
        elif self.rect.right >= self.tiles_path[-1].rect.left : 
            if self.movement_direction != "left" : 
                self.movement_direction = None
                self.idling_timer += 1
                if self.idling_timer >= 180 : 
                    self.idling_timer = 0
                    self.movement_direction = "left"
                
        
        
    def animate(self, sprite_list, speed):
        self.current_image += speed
        self.current_image = round(self.current_image,1)
        if self.current_image >= len(sprite_list) :
            self.current_image = 0
        self.image = sprite_list[int(self.current_image)]
    
    def draw(self, screen, camera_x, camera_y) : 
        screen.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))