import pygame
pygame.init()
import random
import math

SPAWN_OBSTACLE = pygame.USEREVENT + 1
frekvence = [600,4000]
pygame.time.set_timer(SPAWN_OBSTACLE, random.randint(frekvence[0],frekvence[1]))


handling = 3      
zrychleni = 0.5
max_speed = 200  



class Player():
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("img/zezadu.png")
        self.rect = self.image.get_rect()
        self.x = (1920-self.image.get_width())/2
        self.y = 0
        self.angle = 0
        self.velocity = 0
        self.acceleration = 0

    def controls(self,delta):
        keys = pygame.key.get_pressed()
        self.velocity += -0.01*self.velocity*delta


        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.velocity += zrychleni

        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.velocity -= handling/2

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.angle -= delta * handling/self.velocity*30
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.angle += delta * handling/self.velocity*30
        
        self.velocity = max(20,min(self.velocity,max_speed))
        self.angle = max(-2,(min(1,self.angle)))
        self.velocity += self.acceleration*delta
        self.x += self.velocity*delta*math.cos(self.angle)
        self.y += self.velocity*math.sin(self.angle)*delta*100
    
    




class Car(pygame.sprite.Sprite):
    def __init__(self, image, road_y, lane):
        super().__init__()
        self.original_image = image
        self.road_y = road_y
        self.lane = lane
        self.image = image
        self.rect = self.image.get_rect()

    def update(self):
        self.road_y -= 5  # increase position down the screen

        # Find matching point in road_points
        screen_y = int(self.road_y)
        if 0 <= screen_y < len(road_points):
            road_y, road_center_x, scale = road_points[screen_y]

            lane_width = 600 * scale
            offset = (self.lane - 1.5) * lane_width
            screen_x = road_center_x + offset

            new_width = int(self.original_image.get_width() * scale)
            new_height = int(self.original_image.get_height() * scale)
            self.image = pygame.transform.scale(self.original_image, (new_width, new_height))

            self.rect = pygame.Rect(screen_x - new_width // 2, road_y - new_height, new_width, new_height)
        else:
            self.kill()







screen = pygame.display.set_mode((1920,1080))
clock = pygame.time.Clock()
road_image = pygame.image.load("img/silnice.jpg")
road_x = (1920 - road_image.get_width())/2
road_y = 1080-road_image.get_height()
distance = 0                                                    #distance = car_x


player = Player()

car_image = pygame.image.load("img/prius.png").convert_alpha()
cars = pygame.sprite.Group()


road_offset = 0
horizontal_offset = player.angle * 500  
car_line = player.image.get_height()
clock.tick(); pygame.time.wait(16)
while True:
    delta = clock.tick(74)/1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


        if event.type == SPAWN_OBSTACLE:
            lane = random.randint(0, 3)
            car = Car(car_image, road_y=1080, lane=lane)
            cars.add(car)
            pygame.time.set_timer(SPAWN_OBSTACLE, random.randint(frekvence[0], frekvence[1]))




    screen.fill((0,255,0))
    player.controls(delta)


    distance += 10
    road_offset += player.velocity * delta * 100  # 100 is a tuning factor
    car_line = 1080 - 800 - player.image.get_height()//2

    road_points = []
    for i in range(1080):
        scale = (1100-i)/500

        x = road_offset + i/scale
        y = 200*math.sin(x/1234) + 170*math.sin(x/5432) + 500*math.sin(x/2000) - player.y
        
    
       
        tilt_strength = player.angle * (i / 1080)*900
        horizontal = 960 - (500 - y) * scale - tilt_strength
        road_slice = road_image.subsurface((0, (x)%1456,1000, 1))
        scaled_slice = pygame.transform.scale(road_slice, (1000*scale, 1))
        screen.blit(scaled_slice,(horizontal,1080-i))
        road_points.append((1080 - i, horizontal, scale))
        


    cars.update()
    cars.draw(screen)

    screen.blit(player.image, (960-player.image.get_width()/2,800))
    pygame.display.update()
    clock.tick(74)