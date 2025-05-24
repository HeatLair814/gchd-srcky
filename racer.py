import pygame
pygame.init()
import random

SPAWN_OBSTACLE = pygame.USEREVENT + 1
frekvence = [600,4000]
pygame.time.set_timer(SPAWN_OBSTACLE, random.randint(frekvence[0],frekvence[1]))


handling = 20
acceleration = 10
min_speed = 30
max_speed = 130



class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("zezadu1.png")
        self.rect = self.image.get_rect()
        self.rect.x = (1920-self.image.get_width())/2
        self.rect.y = 800

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.rect.x >= 400:
            self.rect.x += -handling
            self.image = pygame.image.load("zleva.png")
        elif keys[pygame.K_d] and self.rect.x <= 1320:
            self.rect.x += handling
            self.image = pygame.image.load("zprava.png")
        else:
            self.image = pygame.image.load("zezadu1.png")
    def update(self):
        self.player_input()
    




class Car(pygame.sprite.Sprite):
    def __init__(self, image, road_y, lane_x):
        super().__init__()
        self.original_image = image
        self.road_y = road_y  
        self.lane_x = lane_x 
        self.update()
        self.image = image
        self.rect = self.image.get_rect()

    def update(self):
        scale = (self.road_y + 376) / 1300
        self.road_y += 5 * scale
        new_width = int(self.original_image.get_width() * scale)
        new_height = int(self.original_image.get_height() * scale)
        self.image = pygame.transform.scale(self.original_image, (new_width, new_height))

        
        lane_width = 76 + (300 - 76) * (self.road_y / 1080)
        if self.lane_x in (1,2):
            koeficient_debilnosti = 1.2
        else: koeficient_debilnosti = 1.07

        offset_from_center = ((self.lane_x - 1.5) * lane_width)*koeficient_debilnosti
        screen_x = (960 + offset_from_center - new_width // 2)
        screen_y = self.road_y - new_height

        self.rect = pygame.Rect(screen_x, screen_y, new_width, new_height)
        
        
        if self.road_y > 1080 + self.image.get_height():
            self.kill()








screen = pygame.display.set_mode((1920,1080))
clock = pygame.time.Clock()
road_image = pygame.image.load("silnice1.jpg")
road_x = (1920 - road_image.get_width())/2
road_y = 1080-road_image.get_height()
distance = 0                                                    #distance = car_x


player = pygame.sprite.GroupSingle()
player.add(Player())

car_image = pygame.image.load("prius.png").convert_alpha()
cars = pygame.sprite.Group()





while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


        if event.type == SPAWN_OBSTACLE:
            lane = random.randint(0, 3) 
            car = Car(car_image, road_y=-200, lane_x=lane)
            cars.add(car)




    screen.fill((0,255,0))



    distance += 10
    for i in range(1081):
        scale = (1456-i)/1080
        x = distance + i/scale
        road_slice = road_image.subsurface((0, (x)%360,1000, 1))
        scaled_slice = pygame.transform.scale(road_slice, (1000*scale, 1))
        screen.blit(scaled_slice,(960-500*scale,1080-i))

    cars.update()
    cars.draw(screen)
    

    player.draw(screen)
    player.update()
    pygame.display.update()
    clock.tick(74)