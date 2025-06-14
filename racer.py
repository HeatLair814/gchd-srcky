import pygame
import random
import math

pygame.init()

auto = "lambo" #možnosti: lambo, porsche, aston, mcqueen, mercedes(pro +rychlost)
frame_rate = 74
handling = 2      
zrychleni = 1
max_speed = 200
frekvence_aut = [600,4000] #frekvence spawnování aut
#frekvence_objektu = [100,500]
game_name = "Tour de UAE"
fps_counter = False
game_state = "menu"
MONEY = 0
VOLUME = 1
sounds = [pygame.mixer.Sound("songs/honk.mp3")]
for i in range(1,4):
    sounds.append(pygame.mixer.Sound(f"songs/explosion/{i}.mp3"))



SPAWN_OBJECT = SPAWN_CAR = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_CAR, random.randint(frekvence_aut[0],frekvence_aut[1]))


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(f"img/{auto}.png")
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.x = (1920-self.image.get_width())/2
        self.y = 0
        self.angle = 0
        self.velocity = 0
        self.acceleration = 0
        self.rect.topleft = (960 - self.image.get_width() // 2, 600)

    def controls(self,delta):
        keys = pygame.key.get_pressed()
        self.velocity += -0.1*self.velocity*delta


        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.velocity += zrychleni

        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.velocity -= handling/2

        if (keys[pygame.K_a] or keys[pygame.K_LEFT]):
            self.angle -= delta * handling#/self.velocity*30
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.angle += delta * handling#/self.velocity*30
        
        self.velocity = max(20,min(self.velocity,max_speed))
        self.angle = max(-2,(min(1,self.angle)))
        self.velocity += self.acceleration*delta
        self.x += self.velocity*delta*math.cos(self.angle)
        self.y += self.velocity*math.sin(self.angle)*delta*100



    def restart(self):
        self.image = pygame.image.load(f"img/{auto}.png")
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.x = (1920-self.image.get_width())/2
        self.y = 0
        self.angle = 0
        self.velocity = 0
        self.acceleration = 0
        self.rect.topleft = (960 - self.image.get_width() // 2, 600)

class Car(pygame.sprite.Sprite):
    def __init__(self, road_y, lane,rychlost_bileho_auta):
        super().__init__()
        image = pygame.image.load(random.choice(["img/prius.png","img/tesla.png","img/transporter.png"])).convert_alpha()
        self.original_image = image
        self.road_y = road_y
        self.lane = lane
        self.image = image
        self.rect = self.image.get_rect()
        self.rychlost = 1/rychlost_bileho_auta
        self.k=1.006


    def update(self,scale, road_points, delta):
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
            self.mask = pygame.mask.from_surface(self.image)

        else:
            self.kill()

        self.rychlost = self.rychlost*self.k
        self.k += 0.000001*player.velocity



class Object(pygame.sprite.Sprite):
    pass
                             

screen = pygame.display.set_mode((1920,1080))
player = Player()
car_image = pygame.image.load("img/prius.png").convert_alpha()
cars = pygame.sprite.Group()
objects = pygame.sprite.Group()

clock = pygame.time.Clock()


loading_screen = random.randint(1,10)
SWITCH_LOADING_SCREEN = pygame.USEREVENT + 3
loading_bar_width = 0
pygame.time.set_timer(SWITCH_LOADING_SCREEN, 4000)


def settings():
    global sounds
    global fps_counter
    global VOLUME
    back_button = pygame.image.load("img/back.png")
    settings_text = pygame.font.Font("fonts/SamsungSans-Bold.ttf", 100).render("Settings", True, (255,255,255))
    volume_text = pygame.font.Font("fonts/SamsungSans-Regular.ttf", 50).render(f"Volume: {round(VOLUME*100)} %", True, (255,255,255))
    volume_button = pygame.Rect(780,180,volume_text.get_width()+40, volume_text.get_height()+40)
    fps_text = pygame.font.Font("fonts/SamsungSans-Regular.ttf", 50).render("FPS: ", True, (255,255,255))
    fps_button = pygame.Rect(1000, 400, 50, 50)
    restore_text = pygame.font.Font("fonts/SamsungSans-Regular.ttf", 50).render("Restore purchases", True, (255,255,255))
    secret_text = pygame.font.Font("fonts/SamsungSans-Regular.ttf", 50).render("Secret code", True, (255,255,255))
    
    while True:
        mx, my = pygame.mouse.get_pos()
        screen.fill((0,0,0))
        screen.blit(back_button, (50, 25))
        screen.blit(settings_text, (960-settings_text.get_width()//2, 25))
        pygame.draw.rect(screen, (34, 34, 34), volume_button, border_radius=20)
        screen.blit(volume_text, (800, 200))
        screen.blit(fps_text, (800, 400))
        pygame.draw.rect(screen, (34,34,34), fps_button)
        pygame.draw.polygon(screen,(255,255,255),((1000,400),(1050,400),(1050,450),(1000,450)),2)
        screen.blit(restore_text, (800, 600))
        screen.blit(secret_text, (800, 800))

        if fps_counter:
            pygame.draw.rect(screen, (29, 205, 159), (1005,405,42,42))
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if fps_button.collidepoint(event.pos):
                    fps_counter = not fps_counter

                elif restore_text.get_rect(center=(960, 600)).collidepoint(event.pos):
                    print("Restore purchases clicked")
                
                elif secret_text.get_rect(center=(960, 800)).collidepoint(event.pos):
                    print("Secret code clicked")

                elif back_button.get_rect(topleft=(50, 25)).collidepoint(event.pos):
                    return "menu"
                elif volume_button.collidepoint(event.pos):
                    VOLUME = random.uniform(0, 1)
                    pygame.mixer.music.set_volume(VOLUME)
                    for sound in sounds:
                        sound.set_volume(VOLUME)
                        print(pygame.mixer.Sound.get_volume(sound))
                    volume_text = pygame.font.Font("fonts/SamsungSans-Regular.ttf", 50).render(f"Volume: {round(VOLUME*100)} %", True, (255,255,255))
                
        if back_button.get_rect(topleft=(50, 25)).collidepoint(mx, my):
            pygame.draw.rect(screen, (70,70,70), (40, 15, 70, 70),border_radius=20)
            screen.blit(back_button, (50, 25))
        if volume_button.collidepoint(mx, my):
            pygame.draw.rect(screen, (70, 70, 70), (volume_button.x - 10, volume_button.y - 10, volume_button.width + 20, volume_button.height + 20), border_radius=30)
            screen.blit(volume_text, (800, 200))

        pygame.display.update()
        clock.tick(frame_rate)


def menu():
    off_button = pygame.image.load("img/off.png")
    settings_button = pygame.image.load("img/settings.png")
    drive_button_text = pygame.font.Font("fonts/SamsungSans-Regular.ttf", 160).render("DRIVE!", True, (34,34,34))
    drive_button = pygame.Rect(660,850,600,200)
    while True:
        mx, my = pygame.mouse.get_pos()
        screen.fill((0,0,0))
        pygame.draw.rect(screen, (34, 34, 34), (0, 0, 1920, 100))
        screen.blit(off_button, (50, 25))
        screen.blit(settings_button,(150,25))
        pygame.draw.rect(screen,(255,255,255),(124,25,2,50))
        pygame.draw.rect(screen,(34,34,34),drive_button,border_radius=40)
        pygame.draw.rect(screen,(29, 205, 159),(680,870,560,160),border_radius=20)
        screen.blit(drive_button_text, (960 - drive_button_text.get_width() // 2, 950 - drive_button_text.get_height() // 2))
        pygame.draw.polygon(screen,(34,34,34),((60,700),(260,600),(260,800)))
        pygame.draw.polygon(screen,(34,34,34),((1660,600),(1860,700),(1660,800)))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if off_button.get_rect(topleft=(50,25)).collidepoint(event.pos):
                    pygame.quit()
                    exit()

                elif settings_button.get_rect(topleft=(150,25)).collidepoint(event.pos):
                    return "settings"
                
                elif drive_button.collidepoint(event.pos):
                    return "game"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return "game"
                
        if off_button.get_rect(topleft=(50,25)).collidepoint(mx, my):
            pygame.draw.rect(screen,(70,70,70),(40,15,70,70),border_radius=20)
            screen.blit(off_button, (50, 25))

        if settings_button.get_rect(topleft=(150,25)).collidepoint(mx, my):
            pygame.draw.rect(screen,(70,70,70),(140,15,70,70),border_radius=20)
            screen.blit(settings_button,(150,25))

                
        if drive_button.collidepoint(mx, my):
            pygame.draw.rect(screen,(22, 153, 118),(680,870,560,160),border_radius=20)
            screen.blit(drive_button_text, (960 - drive_button_text.get_width() // 2, 950 - drive_button_text.get_height() // 2))

        pygame.display.update()
        clock.tick(frame_rate)


def game():
    global MONEY
    global sounds
    global fps_counter
    player.restart()
    road_image = pygame.image.load("img/silnice.jpg")
    road_x = (1920 - road_image.get_width())/2
    road_y = 1080-road_image.get_height()

    horizontal_offset = player.angle * 500  
    car_line = player.image.get_height()

    hud_barva = (20,20,20)
    text_barva = (255,255,255)
    logo_image = pygame.image.load(f"img/{auto}_logo.png")
    explosion_image = pygame.image.load(random.choice(["img/explosion 1.png","img/explosion 2.png"])).convert_alpha()
    explosion_sound = sounds[random.randint(1,3)]
    honk_text = pygame.font.Font("fonts/SamsungSans-Thin.ttf",30).render("[SHIFT] to honk",True,text_barva)
    svodidla = False


    if auto == "aston":
        song_name = "James Bond Theme - Moby remix"
    elif auto == "mcqueen":
        song_name = "Real Gone - Sheryl Crow"
    elif auto == "lambo":
        song_name = "Satisfya - Imran Khan"
    elif auto == "mercedes":
        song_name = random.choice(["Erika - German march","HH - Kanye West"])
    else:
        song_name = random.choice(["James Bond Theme - Moby remix","Arab Money - Busta Rhymes","Satisfya - Imran Khan","WZH - kyeeskii","Free Bird - Lynyrd Skynyrd","No Limit - 2 UNLIMITED","7 5 0 - Malik Montana"])
    music = pygame.mixer.music.load(f"songs/{song_name}.mp3")
    music_text = pygame.font.Font("fonts/SamsungSans-Regular.ttf",30).render(f"[R] Now playing: {song_name}",True,(150,150,150))
    honk_sound = sounds[0]
    pygame.mixer.music.play()
    honk_channel = None
    explosion_channel = None

    total_distance = 0
    distance = 0     
    road_offset = 0
    running = True
    while running:
        elapsed_distance = player.velocity*1/frame_rate*2.5/1000
        total_distance += elapsed_distance
        delta = clock.tick(74)/1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.stop()
                    if honk_channel and honk_channel.get_busy():
                        honk_channel.stop()
                    return "menu"

            #spawnování
            if event.type == SPAWN_CAR:
                lane = random.choice([0, 1, 2, 3])
                car = Car(road_y=1080, lane=lane,rychlost_bileho_auta = random.randint(1,10))
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
            y = 225*math.sin(x/93400) + 171*math.sin(x/1234) + 543*math.sin(x/2345) - player.y
            
            if i == car_line and (horizontal >= 1000 - player.image.get_width()/2 or horizontal <= 960 + player.image.get_width()/2-1500):
                svodidla = True
                
            

            tilt_strength = player.angle * (i / 1080)*900
            horizontal = 960 - (500 - y) * scale - tilt_strength + player.angle*300                         #otáčení silnice kolem auta
            road_slice = road_image.subsurface((0, (x)%1456,1000, 1))
            scaled_slice = pygame.transform.scale(road_slice, (1000*scale, 1))
            screen.blit(scaled_slice,(horizontal,1080-i))
            road_points.append([1080-i, horizontal+500*scale, scale])


        cars.update(scale, road_points, delta)
        cars.draw(screen)

        screen.blit(player.image, (960-player.image.get_width()/2,600))



    
        if pygame.sprite.spritecollide(player, cars, False, pygame.sprite.collide_mask) or svodidla:
            screen.blit(explosion_image,(960-explosion_image.get_width()//2,600- explosion_image.get_height()//2))
            if explosion_channel is None or not explosion_channel.get_busy():
                explosion_channel = explosion_sound.play()
            running = False
            










        #hud
        pygame.draw.rect(screen,hud_barva,(0,880,1920,400),border_radius=200)
        screen.blit(logo_image,(960-logo_image.get_width()//2,890))
        screen.blit(honk_text,honk_text.get_rect(center=(960,1030)))
        rychlost_text = pygame.font.Font("fonts/SamsungSans-Bold.ttf",100).render(f"{round(player.velocity*2.5)} km/h",True,text_barva)
        screen.blit(rychlost_text,(200,930))
        distance_text = pygame.font.Font("fonts/SamsungSans-Regular.ttf",50).render(f"Distance: {round(total_distance,2)} km",True,text_barva)
        screen.blit(distance_text,(1220,900))
        screen.blit(music_text,(1220,1000))
        
        if pygame.key.get_pressed()[pygame.K_LSHIFT]:
            if honk_channel is None or not honk_channel.get_busy():
                honk_channel = honk_sound.play(-1)
        else:
            if honk_channel and honk_channel.get_busy():
                honk_channel.stop()

        if pygame.key.get_pressed()[pygame.K_r] or not pygame.mixer.music.get_busy():
                song_name = random.choice(["James Bond Theme - Moby remix","Arab Money - Busta Rhymes","Satisfya - Imran Khan","WZH - kyeeskii","Free Bird - Lynyrd Skynyrd","No Limit - 2 UNLIMITED","7 5 0 - Malik Montana"])
                music = pygame.mixer.music.load(f"songs/{song_name}.mp3")
                music_text = pygame.font.Font("fonts/SamsungSans-Regular.ttf",30).render(f"[R] Now playing: {song_name}",True,(150,150,150))
                pygame.mixer.music.play()
        if fps_counter:
            fps_text = pygame.font.Font("fonts/Square.ttf",70).render(f"FPS: {round(clock.get_fps())}",True,(0,255,0))
            screen.blit(fps_text,(20,20))

        pygame.display.update()
        clock.tick(frame_rate)







    overlay = True
    island_y = -400
    buttons_x = -500
    death_text = pygame.font.Font("fonts/SamsungSans-Bold.ttf",70).render(random.choice(["Took a shortcut to the afterlife.","Turns out brakes ARE important.","Speed: 100%. Control: 0%.","Even Filip's granny drives better!","You're NOT Filip Turek!","Car is broken, just like this code!"]),True,(255,255,255))
    crashed_text = pygame.font.Font("fonts/SamsungSans-Regular.ttf",50).render(f"Crashed at: {round(player.velocity*2.5)} km/h",True,(255,255,255))
    total_distance_text = pygame.font.Font("fonts/SamsungSans-Regular.ttf",50).render(f"Total distance: {round(total_distance,2)} km",True,(255,255,255))
    plus_money_text = pygame.font.SysFont("Segoe UI",70).render(f"+{round(round(total_distance)*10000)} د.إ",True,(255,255,0))
    menu_button_text = pygame.font.Font("fonts/SamsungSans-Regular.ttf",120).render("Menu",True,(0,0,0))
    play_again_button_text = pygame.font.Font("fonts/SamsungSans-Regular.ttf",90).render("Play again",True,(0,0,0))

    while not running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                MONEY += round(round(total_distance)*10000)
                if event.key == pygame.K_ESCAPE:
                    return "menu"
                if event.key == pygame.K_RETURN:
                    running = True
                    cars.empty()
                    objects.empty()
                    return "game"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_again_button.collidepoint(event.pos):
                    MONEY += round(round(total_distance)*10000)
                    running = True
                    cars.empty()
                    objects.empty()
                    return "game"
                if menu_button.collidepoint(event.pos):
                    MONEY += round(round(total_distance)*10000)
                    cars.empty()
                    objects.empty()
                    return "menu"
        
                    

        pygame.mixer.music.stop()
        overlay_surface = pygame.Surface((1920,1080), pygame.SRCALPHA)   # per-pixel alpha
        overlay_surface.fill((0,0,0,160))
        if overlay:                  # notice the alpha value in the color
            screen.blit(overlay_surface, (0,0))
            overlay = False
        
        pygame.draw.rect(screen,(29, 205, 159),(160,island_y,1600,350),border_radius=200)
        pygame.draw.rect(screen,(0,0,0),(170,10+island_y,1580,330),border_radius=180)
        screen.blit(death_text,(960-death_text.get_width()//2,20+island_y))
        screen.blit(crashed_text,(960-(crashed_text.get_width()+total_distance_text.get_width()+30)//2,120+island_y))
        screen.blit(total_distance_text,(960-(crashed_text.get_width()+total_distance_text.get_width()+100)//2+crashed_text.get_width()+100,120+island_y))
        screen.blit(plus_money_text,(960-plus_money_text.get_width()//2,200+island_y))
        if island_y < 50:
            island_y += 10
        

        play_again_button = pygame.Rect(buttons_x,540,500,200)
        menu_button = pygame.Rect(1420-buttons_x,540,500,200)
        pygame.draw.rect(screen,(0,0,0),play_again_button,border_radius=100)
        pygame.draw.rect(screen,(29, 205, 159),(buttons_x+10,550,480,180),border_radius=90)
        pygame.draw.rect(screen,(0,0,0),menu_button,border_radius=100)
        pygame.draw.rect(screen,(29, 205, 159),(1430-buttons_x,550,480,180),border_radius=90)
        screen.blit(play_again_button_text,(buttons_x+250-play_again_button_text.get_width()//2,540+100-play_again_button_text.get_height()//2))
        screen.blit(menu_button_text,(1420-buttons_x+250-menu_button_text.get_width()//2,540+100-menu_button_text.get_height()//2))

        if buttons_x < 160:
            buttons_x += 10
        
        if play_again_button.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen,(22, 153, 118),(buttons_x+10,550,480,180),border_radius=100)
            screen.blit(play_again_button_text,(buttons_x+250-play_again_button_text.get_width()//2,540+100-play_again_button_text.get_height()//2))
        if menu_button.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen,(22, 153, 118),(1430-buttons_x,550,480,180),border_radius=100)
            screen.blit(menu_button_text,(1420-buttons_x+250-menu_button_text.get_width()//2,540+100-menu_button_text.get_height()//2))
        





        pygame.display.update()
        clock.tick(frame_rate)




































loading = True
pygame.display.set_caption(game_name)
while loading:
    if loading_bar_width <= 1700:
        screen.blit(pygame.image.load(f"img/loading/{loading_screen}.png"), (0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == SWITCH_LOADING_SCREEN:
                loading_screen = random.randint(1,10)
                pygame.time.set_timer(SWITCH_LOADING_SCREEN, 4000)

        pygame.draw.rect(screen, (0, 0, 0), (100, 900, 1720, 100))
        pygame.draw.rect(screen, (29, 205, 159), (110, 910, loading_bar_width, 80))
        screen.blit(pygame.font.Font("fonts/SamsungSans-Bold.ttf",70).render(game_name,True,(0,0,0)),(115,915))
        loading_bar_width += 100
    else:
        pygame.time.wait(1000)
        loading = False

    pygame.display.update()
    clock.tick(frame_rate)


while True:
    if game_state == "menu":
        game_state = menu()
    elif game_state == "settings":
        game_state = settings()
    elif game_state == "game":
        game_state = game()  
    else:
        print("Exiting game loop.")
        break