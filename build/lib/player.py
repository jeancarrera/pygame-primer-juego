import pygame , random
from pyparsing import *


WIDTH = 800
HEIGHT = 600
GREEN = (136,239,6)
BLACK = (0,0,0)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Arcade")
clock= pygame.time.Clock()



def texto(surface,text,size,x,y):
    font= pygame.font.SysFont("serif", size)
    text_surface = font.render(text,True, (255,255,255))
    text_rec = text_surface.get_rect()
    text_rec.midtop = (x,y)
    surface.blit(text_surface, text_rec)

def barra_scudo(surface, x, y, percentage):
    barra_long = 100
    barra_alto = 10 
    datos = (percentage / 100) * barra_long
    border = pygame.Rect(x, y, barra_long, barra_alto)
    datos = pygame.Rect(x,y, datos, barra_alto)
    pygame.draw.rect(surface , GREEN , datos)
    
# clase y parametros del jugador 
class Jugadro(pygame.sprite.Sprite):
    def __init__(self): # inicio de la funcion jugador
        super().__init__() # inicio super clase Jugador
        #agregado de imagen del jugador y seteo de parametros 
        self.image = pygame.image.load("assets/player.png").convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT -10
        self.speed_x = 0
        self.escudo = 100
        
    #condiciones de movimiento del jugador y caracteristicas de entorno
    def update(self):
        self.speed_x = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speed_x = -5
        if keystate[pygame.K_RIGHT]:   
            self.speed_x = 5
            
        self.rect.x += self.speed_x
        
        if self.rect.left < 0:
            self.rect.left = 0
            
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
    
    #metodo de desparo 
    def disparo(self):
        balas = Balas(self.rect.centerx, self.rect.top)
        all_sprites.add(balas)
        bala.add(balas)
        laser_sonido.play()


#clase para los enemigos en este caso los meteoritos 
class Meteoros(pygame.sprite.Sprite): 
    def __init__(self):# inicio
        super().__init__()# inicio super clase 
        #agregado de imagen primal de enemigos
        # self.image = pygame.image.load("assets/meteorGrey_med1.png").convert()
        self.image = random.choice(meteor_images)
        self.image.set_colorkey(BLACK) 
        self.rect = self.image.get_rect()
        
        #ingreso parametros random para el movimiento aleatorio de los enemigos
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-140, -100)
        self.speedy = random.randrange( 1,10)
        self.speedx = random.randrange(-5, 5)
        
    def update(self):
         #aumento de velocidad de los enemigos
        self.rect.x += self.speedx   
        self.rect.y += self.speedy 
         
        if self.rect.top > HEIGHT + 10 or self.rect.left < -40 or self.rect.right > WIDTH + 22:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1,8)
            self.speedx = random.randrange(1,8)
            
class Balas(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self. image = pygame.image.load("assets/laser1.png").convert()
        self.image.set_colorkey(BLACK) 
        self.rect = self.image.get_rect()
        
        self.rect.y = y
        self.rect.centerx = x
        self.speedy = -10
        
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center) :
        super().__init__()
        self.image = explosion_enemigos[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50
        
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1 
            if self.frame == len(explosion_enemigos):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_enemigos[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
            
def pantalla_game_over():
    screen.blit(bg, [0,0])
    texto(screen, "Arcade", 65, WIDTH // 2,HEIGHT // 4 )
    texto(screen, "Destruye todos los asteroides", 27, WIDTH // 2, HEIGHT // 2  )
    texto(screen, "Preciona ESPACIO", 20, WIDTH // 2, HEIGHT * 3/4)            
    pygame.display.flip()
    espera = True
    
    while espera:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                espera = False
                
meteor_images = [] 
meteor_list   = ["assets/meteorGrey_big1.png", "assets/meteorGrey_big2.png", "assets/meteorGrey_big3.png", "assets/meteorGrey_big4.png",
				"assets/meteorGrey_med1.png", "assets/meteorGrey_med2.png", "assets/meteorGrey_small1.png", "assets/meteorGrey_small2.png",
				"assets/meteorGrey_tiny1.png", "assets/meteorGrey_tiny2.png"]

for img in meteor_list:
    meteor_images.append(pygame.image.load(img).convert())
    
 # carga de imagen de fondo  
bg = pygame.image.load("assets/background.png")

# explsion de enemigos 
explosion_enemigos = []
for i in range(9):
    file = "assets/regularExplosion0{}.png".format(i)
    img = pygame.image.load(file)
    img.set_colorkey(BLACK)
    img_scale = pygame.transform.scale(img,(70,70)) 
    explosion_enemigos.append(img_scale)

# sonidos
laser_sonido = pygame.mixer.Sound("assets/laser5.ogg")
explosion_sonido = pygame.mixer.Sound("assets/explosion.wav")
pygame.mixer.music.load("assets/music.ogg")
pygame.mixer.music.set_volume(0.2)

            
pygame.mixer.music.play(loops=-1)
running = True #corredor del juego 
game_over = True

while running:
    if game_over:
        game_over = False
        
        pantalla_game_over()
    
        all_sprites = pygame.sprite.Group()# creacion de grupo asignacion de jugador
        meteor_list = pygame.sprite.Group()#creado de grupo asignacion de meteor_list
        bala = pygame.sprite.Group()#  creacion de balas  


        jugador = Jugadro()
        all_sprites.add(jugador)

        for i in range(9):
            meteor = Meteoros()
            all_sprites.add(meteor)
            meteor_list.add(meteor)
    
        contador= 0    
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                jugador.disparo()
            
    all_sprites.update()
    
    
    # disparos
    choque = pygame.sprite.groupcollide(meteor_list, bala , True, True)
    for choques in choque:
        contador += 10
        explosion_sonido.play()
        explosion = Explosion(choques.rect.center)
        all_sprites.add(explosion)
        
        meteor = Meteoros() 
        all_sprites.add(meteor)
        meteor_list.add(meteor)
      
    #creacion de coliciones del jugador
    choque = pygame.sprite.spritecollide(jugador, meteor_list, True)
    for choques in choque:
        jugador.escudo -= 25
        meteor = Meteoros()
        all_sprites.add(meteor)
        meteor_list.add(meteor)
        
        if jugador.escudo < 0:
            game_over = True
    
    screen.blit(bg, [0,0])#implementacion de la imagen de background al juego
    all_sprites.draw(screen)#implementacion de la pantalla y entorno
    
    #escore del juego
    texto(screen, str(contador), 25, WIDTH // 2, 10)
    
        # escudo
    barra_scudo(screen, 5 , 5 , jugador.escudo)
    pygame.display.flip()
    
pygame.quit()#comando de cierre 


