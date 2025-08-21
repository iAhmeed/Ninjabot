import pygame
from random import randint

class Player :
    def __init__(self, tiles) -> None:
        self.right_running_images = []
        self.left_running_images = []
        self.right_idling_images = []
        self.left_idling_images = []
        for _ in range(2):
            self.right_running_images.append(pygame.transform.scale(pygame.image.load("data/player/running" + str(_ + 1) + ".png"), (20, 55)))
            self.left_running_images.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load("data/player/running" + str(_ + 1) + ".png"), (20, 55)), True, False))
            self.right_idling_images.append(pygame.transform.scale(pygame.image.load('data/player/idling' + str(_ + 1) + '.png'),(20,55)))
            self.left_idling_images.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('data/player/idling' + str(_ + 1) + '.png'),(20,55)), True, False))

        self.current_image = 0
        self.image = self.right_idling_images[self.current_image]
        self.rect = self.image.get_rect()

        self.movements = [0, 0]
        self.gravity_inc = 0
        self.jump_speed = 15
        self.jumping = False
        self.double_jumping = False
        self.can_double_jump = False
        self.moving_right, self.moving_left = False, False
        self.rotation_angle = 0
        self.previous_movement = None
        self.tiles = tiles

        self.camera_x = 0
        self.camera_y = 0

        self.camera_target_x = 0
        self.camera_target_y = 0
        self.camera_speed = 0.08

    def update(self, screen_width, screen_height):

        if self.moving_left:
            self.previous_movement = 'left'
            self.movements[0] = -5
            self.animate(self.left_running_images, .2)
        elif self.moving_right:
            self.previous_movement = 'right'
            self.movements[0] = 5
            self.animate(self.right_running_images, .2)
        else:
            if self.previous_movement == 'right' or not self.previous_movement:
                self.animate(self.right_idling_images, .1)
            elif self.previous_movement == 'left':
                self.animate(self.left_idling_images, .1)
            self.movements[0] = 0

        # Movement and collision handling
        self.movements[1] += self.gravity_inc
        self.rect.x += self.movements[0]
        self.handle_horizontal_collisions()

        self.rect.y += self.movements[1]
        self.handle_vertical_collisions()

        if self.double_jumping : 
            if self.rotation_angle > -360 : 
                self.rotation_angle -= 20
                if self.moving_right : 
                    self.image = pygame.transform.rotate(self.image, self.rotation_angle)
                elif self.moving_left : 
                    self.image = pygame.transform.rotate(self.image, -self.rotation_angle)
                else : 
                    if self.previous_movement == "right" or not self.previous_movement: 
                        self.image = pygame.transform.rotate(self.image, self.rotation_angle)
                    elif self.previous_movement == "left" : 
                        self.image = pygame.transform.rotate(self.image, -self.rotation_angle)
        else : 
            self.rotation_angle = 0

        self.handle_ramps_collisions([tile for tile in self.tiles if tile.ramp])

        # Camera lag effect
        self.camera_target_x = self.rect.centerx - screen_width // 2
        self.camera_target_y = self.rect.centery - screen_height // 2

        # Smoothly move camera towards target
        self.camera_x += (self.camera_target_x - self.camera_x) * self.camera_speed
        self.camera_y += (self.camera_target_y - self.camera_y) * self.camera_speed


    def handle_horizontal_collisions(self):
        hit_list = [tile for tile in self.tiles if self.rect.colliderect(tile.rect) and not tile.ramp]
        for tile in hit_list:
            if self.moving_right:
                self.rect.right = tile.rect.left
            elif self.moving_left:
                self.rect.left = tile.rect.right

    def handle_vertical_collisions(self):
        hit_list = [tile for tile in self.tiles if self.rect.colliderect(tile.rect) and not tile.ramp]
        for tile in hit_list:
            if self.movements[1] > 0:
                self.rect.bottom = tile.rect.top
                self.movements[1] = 0
                self.gravity_inc = 0
                self.jumping = False
                self.double_jumping = False
            elif self.movements[1] < 0:
                self.rect.top = tile.rect.bottom
                self.movements[1] = 0

        if not hit_list:
            self.gravity_inc = 1
    def handle_ramps_collisions(self,ramps) : 
        for ramp in ramps : 
            hitbox = ramp.rect
            if self.rect.colliderect(hitbox):
                rel_x = self.rect.x - hitbox.x
                if ramp.ramp == 1:
                    pos_height = rel_x + self.rect.width
                elif ramp.ramp == 2:
                    pos_height = ramp.rect.height - rel_x

                # add constraints
                pos_height = min(pos_height, ramp.rect.height)
                pos_height = max(pos_height, 0)
 
                target_y = hitbox.y + ramp.rect.height - pos_height
 
                if self.rect.bottom > target_y: # check if the player collided with the actual ramp
                    # adjust player height
                    self.rect.bottom = target_y
                    self.movements[1] = 0

    def animate(self, sprite_list, speed):
        self.current_image += speed
        self.current_image = round(self.current_image,1)
        if self.current_image >= len(sprite_list) :
            self.current_image = 0
        self.image = sprite_list[int(self.current_image)]

    def reset_tiles(self, new_tiles) : 
        self.tiles = new_tiles

    def jump(self):
        self.movements[1] = -self.jump_speed
        self.jumping = True

    def double_jump(self) : 
        if not self.double_jumping and self.can_double_jump: 
            self.movements[1] = -self.jump_speed
            self.double_jumping = True

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x - self.camera_x, self.rect.y - self.camera_y))

    def set_position(self,x,y) : 
        self.rect.bottomleft = (x,y)

    def shake (self) : 
        self.rect.x += randint(-4,4)
        #self.rect.y += randint(-4,4)
        
    def has_fallen(self) : 
        return self.rect.top > max(tile.rect.bottom for tile in self.tiles)
        