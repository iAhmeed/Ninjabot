import pygame
from Player import Player
from Button import Button
from Tile import Tile, load_map
from Portal import Portal
from Robot import Robot

class Game : 
    def __init__(self) -> None:
        pygame.init()
        self.display = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        pygame.display.set_caption("Ninjabot")
        self.screen_width = self.display.get_width()
        self.screen_height = self.display.get_height()
        self.over = False
        self.tiles = []
        self.robots = []
        self.load_player(1)
        self.load_tiles(1)

        self.clock = pygame.time.Clock()
        self.FPS = 60
        self.font = pygame.font.Font('data/fonts/PixelCaps-LOnE.ttf',62)
        self.alpha1 = 1
        self.alpha2 = 1

        #self.menus = ['main_menu' ,'level1' ,'level2', 'level3', 'level4', 'level5']
        self.current_menu = 'main_menu'
        self.main_background = pygame.transform.scale(pygame.image.load('data/background.jpeg'),(self.screen_width,self.screen_height))
        self.play_button = Button(self.screen_width//2 - 32,self.screen_height//3,pygame.font.SysFont('uroob',(64)).render('Play',True,'green'))
        self.quit_button = Button(self.screen_width//2 - 32, self.play_button.rect.bottom + self.screen_height//5,pygame.font.SysFont('uroob', (64)).render('Quit',True,'red'))

        self.hints = ['Use Arrow Keys <-  -> To Move', 'Space To Jump']
        self.set_portal(1)

    def draw_text(self, text, font_path, font_size, color, center_x, top) : 
        font = pygame.font.Font(font_path,font_size) if font_path else pygame.font.SysFont('uroob',font_size)
        text_surface = font.render(text,True,color)
        text_rect = text_surface.get_rect()
        text_rect.centerx = center_x
        text_rect.top = top
        self.display.blit(text_surface,text_rect)


    def main_menu(self) : 
        self.display.blit(self.main_background,(0,0))
        self.draw_text('Ninjabot','',self.screen_height//10,'lightblue',self.screen_width//2,self.screen_height//15)
        if self.play_button.draw(self.display) : 
            
            pygame.mouse.set_visible(False)
            self.screen_transition(3)
            self.current_menu = 'level1'

        if self.quit_button.draw(self.display) : 
            self.over = True

    def screen_transition(self, speed) : 
        black_screen = self.display.convert_alpha()
        for _ in range(0,256,speed) : 
            black_screen.fill((0,0,0,_))
            self.display.blit(black_screen,(0,0))
            pygame.display.flip()

    def text_transition(self, font, text, color, centerx, bottom, alpha = 255) : 
        text_surface = font.render(text, True, color)

        text_rect = text_surface.get_rect()
        text_rect.centerx = centerx
        text_rect.bottom = bottom
        text_surface.set_alpha(alpha)
        self.display.blit(text_surface, text_rect)

    

    def load_tiles(self, level_number) : 
        self.tiles.clear()
        tile_map = load_map("data/maps/" + str(level_number))
        y = 0
        for row in tile_map : 
            x = 0
            for tile in row :  
                if tile in {'1', '2'} :
                    self.tiles.append(Tile(tile,x * 50, y * 50))
                x += 1
            y += 1
        self.player.reset_tiles(self.tiles)

    def load_background(self, level_number) : 
        self.display.fill((97,115,164))
        level_map = load_map("data/maps/" + str(level_number))
        y = 0
        for row in level_map : 
            x = 0
            for element in row : 
                if element == "m" : 
                    background_object = pygame.transform.scale(pygame.image.load('data/background_objects/moon.png'),(50,50))
                    self.display.blit(background_object, (x * 50, y * 50))
                elif element == "s" : 
                    background_object = pygame.transform.scale(pygame.image.load('data/background_objects/star1.png'),(10,10))
                    self.display.blit(background_object, (x * 50, y * 50))
                elif element == "c" : 
                    background_object = pygame.transform.scale(pygame.image.load('data/background_objects/cloud2.png'),(30,30))
                    self.display.blit(background_object, (x * 50, y * 50))
                elif element == "t" : 
                    background_object = pygame.transform.scale(pygame.image.load('data/background_objects/tree1.png'),(50,50))
                    self.display.blit(background_object, (x * 50  - self.player.camera_x, y * 50 - self.player.camera_y))
                
                x += 1
                
            y += 1

    def load_player(self, level_number) : 

        self.player = Player(self.tiles)
        level_map = load_map("data/maps/" + str(level_number))
        y = 0
        for row in level_map : 
            x = 0
            for element in row : 
                if element == "p" : 
                    self.player.set_position(x * 50, y * 50)
                    
                x += 1
            y += 1
    
    def load_robots(self, level_number, half_path_length) : 
        def highest_valid_half_path_length(lst, length, index ) :
            sub_list = lst[index - length : index + length + 1]
            for elmnt in sub_list : 
                if elmnt not in {"1","2"} : 
                    return highest_valid_half_path_length(lst, length - sub_list.index(elmnt) - 1, index)
            return length
        self.robots.clear()
        level_map = load_map("data/maps/" + str(level_number))
        y = 0
        for row in level_map : 
            x = 0
            for element in row : 
                if element == "r" : 
                    new_length = highest_valid_half_path_length(level_map[y+1], half_path_length, x) if y + 2 <= len(level_map) else highest_valid_half_path_length(level_map[-1], half_path_length, x)
                    tiles = []
                    for tile in self.tiles : 
                        for n in range(x - new_length, x + new_length + 1) : 
                            if tile.rect.bottomleft == (n * 50, (y+1) * 50) :
                                tiles.append(tile)
                    if tiles : 
                        self.robots.append(Robot(x * 50,y * 50,tiles))
                x += 1
            y += 1
    
    
    
    """def pixel_art_object(self, grid_size, pixel_color_list) : 
        surface = pygame.surface.Surface(grid_size)
        pixels = pygame.pixelarray.PixelArray(surface)
        for element in pixel_color_list : 
            pixels[element.get("pixel")[1]][element.get("pixel")[0]] = element.get("color")
        pixels.close()
        surface.set_colorkey((0,0,0))
        return surface"""
    
    def set_portal(self, level_number) : 
        y = 0
        for row in load_map("data/maps/" + str(level_number)) : 
            x = 0
            for element in row : 
                if element == "x" : 
                    self.portal = Portal(x * 50 - self.player.camera_x, y * 50 - self.player.camera_y)
                x += 1
            y+= 1

    def level1(self) : 
        self.load_background(1)
        self.player.update(self.screen_width, self.screen_height)
        self.player.draw(self.display)
        for tile in self.tiles :
            tile.draw(self.display, self.player.camera_x, self.player.camera_y)
            
        if self.alpha1 : 
            self.text_transition(self.font, self.hints[0], 'white', self.screen_width//2, self.screen_height//1.1,self.alpha1)
            if self.alpha1 < 255 : 
                self.alpha1 += 1
            else : 
                self.alpha1 = 0
                
        if self.alpha2 :
            if self.player.rect.right > self.tiles[-1].rect.left and self.player.rect.left < self.tiles[-1].rect.right :  
                self.alpha1 = 0
                self.text_transition(self.font, self.hints[1], 'white', self.screen_width//2, self.screen_height//1.1,self.alpha2)
                if self.alpha2 < 255 : 
                    self.alpha2 += 1
                if pygame.key.get_pressed()[pygame.K_SPACE] : 
                    self.alpha2 = 0
            else : 
                self.alpha2 = 1
                
        self.portal.draw(self.display, self.player.camera_x, self.player.camera_y)
        self.portal.animate(.5)
        
        if self.player.has_fallen() : 
            self.alpha1, self.alpha2 = 0,0
            self.text_transition(self.font, "You have fallen !", (204,0,0), self.screen_width//2, self.screen_height//1.1)
            if self.player.rect.top > self.screen_height + self.player.camera_y : 
                self.screen_transition(4)
                self.reset_level(1)
            
        if self.player.rect.colliderect(self.portal.rect) : 
            self.load_player(2)
            self.load_tiles(2)
            self.current_menu = "level2"
            self.set_portal(2)
            self.load_robots(2,5)
            self.screen_transition(2)
            
    def level2(self) : 
        self.load_background(2)
        self.player.update(self.screen_width, self.screen_height)
        self.player.draw(self.display)
        for tile in self.tiles :
            tile.draw(self.display, self.player.camera_x, self.player.camera_y)

        self.portal.draw(self.display, self.player.camera_x, self.player.camera_y)
        self.portal.animate(.5)
        for robot in self.robots : 
            robot.draw(self.display,self.player.camera_x,self.player.camera_y)
            robot.move()
        if self.player.has_fallen() : 
            self.alpha1, self.alpha2 = 0,0
            self.text_transition(self.font, "You have fallen !", (204,0,0), self.screen_width//2, self.screen_height//1.1)
            if self.player.rect.top > self.screen_height + self.player.camera_y : 
                self.screen_transition(4)
                self.reset_level(2)
                
    def level3(self) : 
        pass

    def level4(self) : 
        pass
    
    def level5(self) : 
        pass
    
    def reset_level(self, level_number) : 
        self.load_tiles(level_number)
        self.load_player(level_number)
        

    def run(self) : 
        while not self.over : 
            for event in pygame.event.get() : 
                if event.type == pygame.QUIT : 
                    self.over = True
                elif event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_RIGHT : 
                        self.player.moving_right = True

                    elif event.key == pygame.K_LEFT : 
                        self.player.moving_left = True
                    
                    elif event.key == pygame.K_SPACE : 
                        if not self.player.jumping : 
                            self.player.jump()
                            self.player.can_double_jump = True
                        else : 
                            self.player.double_jump()
                            self.player.can_double_jump = False
                        

                elif event.type == pygame.KEYUP : 
                    if event.key == pygame.K_RIGHT : 
                        self.player.moving_right = False
                    
                    elif event.key == pygame.K_LEFT :
                        self.player.moving_left = False


            if self.current_menu == 'main_menu' : 
                self.main_menu()
            elif self.current_menu == 'level1' : 
                self.level1()
            elif self.current_menu == 'level2' : 
                self.level2()
            elif self.current_menu == 'level3' : 
                self.level3()
            elif self.current_menu == 'level4' : 
                self.level4()
            elif self.current_menu == 'level5' : 
                self.level5()
            
            self.clock.tick(self.FPS)
            pygame.display.flip()
        pygame.quit()
    
Game().run()