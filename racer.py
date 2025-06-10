import pygame
pygame.init()
import random
import math

frame_rate = 74
handling = 3      
zrychleni = 0.5
max_speed = 200  
frekvence_aut = [600,4000] #frekvence spawnování aut
#frekvence_objektu = [100,500]




SPAWN_OBJECT = SPAWN_CAR = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_CAR, random.randint(frekvence_aut[0],frekvence_aut[1]))
#pygame.time.set_timer(SPAWN_OBJECT, random.randint(frekvence_objektu[0],frekvence_objektu[1]))



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
        self.velocity += -0.1*self.velocity*delta


        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.velocity += zrychleni

        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.velocity -= handling/2

        if (keys[pygame.K_a] or keys[pygame.K_LEFT]):
            self.angle -= delta * handling/self.velocity*30
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.angle += delta * handling/self.velocity*30
        
        self.velocity = max(20,min(self.velocity,max_speed))
        self.angle = max(-2,(min(1,self.angle)))
        self.velocity += self.acceleration*delta
        self.x += self.velocity*delta*math.cos(self.angle)
        self.y += self.velocity*math.sin(self.angle)*delta*100

        
    
    




class Car(pygame.sprite.Sprite):
    def __init__(self, image, road_y, lane,rychlost_bileho_auta):
        super().__init__()
        self.original_image = image
        self.road_y = road_y
        self.lane = lane
        self.image = image
        self.rect = self.image.get_rect()
        self.rychlost = 1/rychlost_bileho_auta
        self.k=1.006


    def update(self,scale):
        self.road_y -= player.velocity * delta * 10
        
        screen_y = int(self.road_y)
        if  0 <= screen_y < len(road_points):
            road_y= road_points[screen_y][0]
            road_center_x= road_points[screen_y][1]
            scale = road_points[screen_y][2]
    
            lane_width =250 * scale
            lane_positions = {0: -1.5,1: -0.5,2: 0.5,3: 1.5}
            offset = lane_positions.get(self.lane, 0) * lane_width
            screen_x = road_center_x + offset

            if scale<(1/0.6):#car_line+player.image.get_height()//2
                new_width = int(self.original_image.get_width() * scale*0.6)
                new_height = int(self.original_image.get_height() * scale*0.6)
                self.image = pygame.transform.scale(self.original_image, (new_width, new_height))
            else:
                new_width = self.original_image.get_width()
                new_height = self.original_image.get_height()
                self.image = self.original_image

            self.rect = pygame.Rect(screen_x - new_width // 2, road_y - new_height, new_width, new_height)

        else:
            self.kill()

        self.rychlost = self.rychlost*self.k
        self.k += 0.000001*player.velocity






class Object(pygame.sprite.Sprite):
    pass
                             










#sracky pred loopem
screen = pygame.display.set_mode((1920,1080))
player = Player()
car_image = pygame.image.load("img/prius.png").convert_alpha()
cars = pygame.sprite.Group()
objects = pygame.sprite.Group()

clock = pygame.time.Clock()
road_image = pygame.image.load("img/silnice.jpg")
road_x = (1920 - road_image.get_width())/2
road_y = 1080-road_image.get_height()

distance = 0        
road_offset = 0
horizontal_offset = player.angle * 500  
car_line = player.image.get_height()
clock.tick(); pygame.time.wait(16)


hud_barva = (20,20,20)
logo_image = pygame.image.load("img/porsche_logo.png")
honk_text = pygame.font.Font("fonts/SamsungSans-Thin.ttf",30).render("[SHIFT] to honk",True,(255,255,255))
total_distance = 0







#main loop















#prvni auto na testovani
lane = random.choice([0, 1, 2, 3])
car = Car(car_image, road_y=1080, lane = lane,rychlost_bileho_auta = random.randint(1,10))
cars.add(car)


while True:
    elapsed_distance = player.velocity*1/frame_rate*2.5/1000
    total_distance += elapsed_distance
    delta = clock.tick(74)/1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        #spawnování
        if event.type == SPAWN_CAR:
            lane = random.choice([0, 1, 2, 3])
            car = Car(car_image, road_y=1080, lane=lane,rychlost_bileho_auta = random.randint(1,10))
            cars.add(car)
            pygame.time.set_timer(SPAWN_CAR, random.randint(frekvence_aut[0], frekvence_aut[1]))
        if event.type == SPAWN_OBJECT:
            object = Object()
            objects.add(object)
            #pygame.time.set_timer(SPAWN_OBJECT, random.randint(frekvence_objektu[0],frekvence_objektu[1]))





    screen.fill((255, 230, 179))
    player.controls(delta)





    #render silnice
    distance += 10
    road_offset += player.velocity * delta * 100
    car_line = 1080 - 600 - player.image.get_height()//2
    road_points = []
    for i in range(1080):
        scale = (1100-i)/500

        x = road_offset + i/scale
        y = 200*math.sin(x/1234) + 170*math.sin(x/5432) + 500*math.sin(x/2000) - player.y
        
        if i == car_line and horizontal >= 760:
            print("crash")
        

        tilt_strength = player.angle * (i / 1080)*900
        horizontal = 960 - (500 - y) * scale - tilt_strength + player.angle*(car_line-player.image.get_height())
        road_slice = road_image.subsurface((0, (x)%1456,1000, 1))
        scaled_slice = pygame.transform.scale(road_slice, (1000*scale, 1))
        screen.blit(scaled_slice,(horizontal,1080-i))
        road_points.append([1080-i, horizontal+500*scale, scale])

        
        

    cars.update(scale)
    cars.draw(screen)


    screen.blit(player.image, (960-player.image.get_width()/2,600))

    pygame.draw.circle(screen,hud_barva,(200,1080),200)
    pygame.draw.rect(screen,hud_barva,(200,880,1520,200))
    pygame.draw.circle(screen,hud_barva,(1720,1080),200)


    screen.blit(logo_image,(960-logo_image.get_width()//2,890))
    screen.blit(honk_text,honk_text.get_rect(center=(960,1030)))
    rychlost_text = pygame.font.Font("fonts/SamsungSans-Bold.ttf",100).render(f"{round(player.velocity*2.5,1)} km/h",True,(255,255,255))
    screen.blit(rychlost_text,(200,930))
    distance_text = pygame.font.Font("fonts/SamsungSans-Regular.ttf",50).render(f"Distance: {round(total_distance,2)} km",True,(255,255,255)) #player.velocity*25/36*elapsed_time/1000
    screen.blit(distance_text,(1220,900))

    
    pygame.display.update()
    clock.tick(frame_rate)