# ===== INÍCIO =====
# --- Importações e pacotes do pygame  
import pygame
from random import *
import time
from os import path

pygame.init()
pygame.mixer.init()

# --- Tela principal
WIDTH = 500
HEIGHT = 400
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('UM BALAUM')
font = pygame.font.SysFont('baloni.ttf', 48)
FPS = 30

STILL = 0

# --- Importa imagem de fundo e os ícones
def load_assets():
    assets = {}
   
    assets['image'] = pygame.image.load('Efeitos/sky3.png').convert()
    assets['image'] = pygame.transform.scale(assets['image'], (500, 400))

    assets['balloon_img'] = pygame.image.load('Efeitos/balloon.png').convert_alpha()
    assets['balloon_img'] = pygame.transform.scale(assets['balloon_img'], (40, 50))

    assets['eagle1_img'] = pygame.image.load('Efeitos/eagle2.png').convert_alpha()
    assets['eagle1_img'] = pygame.transform.scale(assets['eagle1_img'], (10, 10))

    assets['eagle2_img'] = pygame.image.load('Efeitos/eagle.png').convert_alpha()
    assets['eagle2_img'] = pygame.transform.scale(assets['eagle2_img'], (10, 10))

    assets['covid_img'] = pygame.image.load('Efeitos/covid.png').convert_alpha()
    assets['covid_img'] = pygame.transform.scale(assets['covid_img'], (20, 20))

    assets['gel_img'] = pygame.image.load('Efeitos/gel.png').convert_alpha()
    assets['gel_img'] = pygame.transform.scale(assets['gel_img'], (20, 20))

    assets["score_font"] = pygame.font.Font('Efeitos/baloni.ttf', 38)
    assets["life_font"] = pygame.font.Font('Efeitos/baloni.ttf', 13)
    assets["lives_font"] = pygame.font.Font('Efeitos/arcade.ttf', 28)

    # --- Importa o som de fundo
    pygame.mixer.music.load('Efeitos/musica.mp3')
    assets['music'] = pygame.mixer.music
    assets['boom_sound'] = pygame.mixer.Sound('Efeitos/boom.flac')
    assets['pop_sound'] = pygame.mixer.Sound('Efeitos/pop.ogg')
    assets['eagle_sound'] = pygame.mixer.Sound('Efeitos/es.wav')
    assets['eagle_sound'].set_volume(0.2)

    # --- Arquivo para animação
    img_dir = path.join(path.dirname(__file__), 'Efeitos')
    assets['player_sheet'] = pygame.image.load(path.join(img_dir, 'ex.png')).convert_alpha()
    return assets

# --- Cria a classe Covid
class Covid(pygame.sprite.Sprite):
    def __init__(self, assets):
            
        pygame.sprite.Sprite.__init__(self)

        self.image = assets['covid_img']
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        # self.rect.x = -1000
        # self.rect.y = randint(80, 380)
        # self.speed_x = 5
        self.rect.x = randint(60, 420)
        self.rect.y = choice([800, 1000, 1200])
        self.speed_y = randint(6, 6)

    def update(self):

        self.rect.y -= self.speed_y 

        if self.rect.top < -850:
            self.rect.x = randint(60, 420)
            self.rect.y = choice([800, 1000, 1200])
            self.speed_y = randint(4, 6)

# --- Cria a classe do balão, que será movimentado pelo jogador
class Balao(pygame.sprite.Sprite):
    def __init__(self,groups,assets,lives):

        pygame.sprite.Sprite.__init__(self)

        self.image = assets['balloon_img']
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2 
        self.rect.bottom = HEIGHT / 2 
        self.speedx = 0
        self.speedy = 0
        self.groups = groups
        self.assets = assets
        self.lives = lives

        self.shot = pygame.time.get_ticks()
        self.shot_tick = 200

    def update(self):
        # Atualiza da posição do balão
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        # Mantem dentro da tela
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            
    def shoot(self):

        now = pygame.time.get_ticks()

        elapsed_ticks = now - self.shot

        if elapsed_ticks > self.shot_tick:
            self.shot = now
            # A nova bala vai ser criada logo embaixo e no centro do balão
            gel = Gel(self.assets, self.rect.bottom, self.rect.centerx)
            self.groups['all_sprites'].add(gel)
            self.groups['gels'].add(gel)
            self.assets['pop_sound'].play()

class Life(pygame.sprite.Sprite):
    def __init__(self, balao, assets):

        pygame.sprite.Sprite.__init__(self)

        self.balao = balao
        self.assets = assets
        life = self.assets['life_font'].render('{:04d}'.format(self.balao.lives), True, (255, 255, 0))
        self.image = life
        self.rect = self.image.get_rect()
        self.rect.centerx = self.balao.rect.centerx
        self.rect.bottom =  self.balao.rect.bottom - 47
    
    def update(self):

        life = self.assets['life_font'].render('{:04d}'.format(self.balao.lives), True, (255, 255, 0))
        self.image = life
        self.rect = self.image.get_rect()
        self.rect.centerx = self.balao.rect.centerx
        self.rect.bottom = self.balao.rect.bottom - 47
    
# --- Cria as classes das águias, uma para cada águia dependendo do lado da tela em que surge        
class Eagle1(pygame.sprite.Sprite):
    def __init__(self, assets):
        pygame.sprite.Sprite.__init__(self)

        self.image = assets['eagle1_img']
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = -50
        self.rect.y = randint(200, 300)
        self.speed_x = randint(2, 6)
        self.speed_y = randint(-7, 4)
    
    def update(self):

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.top > 400 or self.rect.left > 500:
            self.rect.x = -50
            self.rect.y = randint(200, 300)
            self.speed_x = randint(2, 6)
            self.speed_y = randint(-7, 4)

class Eagle2(pygame.sprite.Sprite):
    def __init__(self, assets):
        pygame.sprite.Sprite.__init__(self)

        self.image = assets['eagle2_img']
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = 550
        self.rect.y = randint(200, 300)
        self.speed_x = randint(2, 6)
        self.speed_y = randint(-7, 4)
    
    def update(self):

        self.rect.x -= self.speed_x
        self.rect.y += self.speed_y

        if self.rect.top > 400 or self.rect.right < -50:
            self.rect.x = 550
            self.rect.y = randint(200, 300)
            self.speed_x = randint(2, 6)
            self.speed_y = randint(-7, 4)

# --- Cria classe para o gel, que pode matar o covid 
class Gel(pygame.sprite.Sprite):
    def __init__(self, assets, bottom, centerx):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.image = assets['gel_img']
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()

        # Coloca no lugar inicial definido em x, y do constutor
        self.rect.centerx = centerx
        self.rect.bottom = bottom
        self.speedy = 10  # Velocidade fixa para cima

    def update(self):
        self.rect.y += self.speedy

def load_spritesheet(spritesheet, rows, columns):
    # Calcula a largura e altura de cada sprite.
    sprite_width = spritesheet.get_width() // columns
    sprite_height = spritesheet.get_height() // rows
    
    # Percorre todos os sprites adicionando em uma lista.
    sprites = []
    for row in range(rows):
        for column in range(columns):
            # Calcula posição do sprite atual
            x = column * sprite_width
            y = row * sprite_height
            # Define o retângulo que contém o sprite atual
            dest_rect = pygame.Rect(x, y, sprite_width, sprite_height)

            # Cria uma imagem vazia do tamanho do sprite
            image = pygame.Surface((sprite_width, sprite_height), pygame.SRCALPHA)
            # Copia o sprite atual (do spritesheet) na imagem
            image.blit(spritesheet, (0, 0), dest_rect)
            sprites.append(image)
    return sprites

# Classe Jogador que representa o herói
class Player(pygame.sprite.Sprite):
    
    # Construtor da classe. O argumento player_sheet é uma imagem contendo um spritesheet.
    def __init__(self, center, player_sheet):
        
        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)
        
        # Aumenta o tamanho do spritesheet para ficar mais fácil de ver
        player_sheet = pygame.transform.scale(player_sheet, (640, 640))

        # Define sequências de sprites de cada animação
        spritesheet = load_spritesheet(player_sheet, 8, 5)
        self.animations = {STILL: spritesheet[0:39]}
        # Define estado atual (que define qual animação deve ser mostrada)
        self.state = STILL
        # Define animação atual
        self.animation = self.animations[self.state]
        # Inicializa o primeiro quadro da animação
        self.frame = 0
        self.image = self.animation[self.frame]
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()
        self.rect.center = center
        # Centraliza na tela.
        # self.rect.centerx = WIDTH / 2
        # self.rect.centery = HEIGHT / 2

        # Guarda o tick da primeira imagem
        self.last_update = pygame.time.get_ticks()

        # Controle de ticks de animação: troca de imagem a cada self.frame_ticks milissegundos.
        self.frame_ticks = 30
        
    # Metodo que atualiza a posição do personagem
    def update(self):
        # Verifica o tick atual.
        now = pygame.time.get_ticks()

        # Verifica quantos ticks se passaram desde a ultima mudança de frame.
        elapsed_ticks = now - self.last_update

        # Se já está na hora de mudar de imagem...
        if elapsed_ticks > self.frame_ticks:

            # Marca o tick da nova imagem.
            self.last_update = now

            # Avança um quadro.
            self.frame += 1

            # Atualiza animação atual
            self.animation = self.animations[self.state]
            
            if self.frame == len(self.animation):
                # Se sim, tchau explosão!
                self.kill()
            else:
                # Se ainda não chegou ao fim da explosão, troca de imagem.
                center = self.rect.center
                self.image = self.animation[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

# --- Cria um grupo de sprites geral e para cada obstáculo
def game_screen(window):

    assets = load_assets()
    
    move_image_1 = 0
    move_image_2 = HEIGHT

    all_sprites = pygame.sprite.Group()
    aguias = pygame.sprite.Group()
    covides = pygame.sprite.Group()
    gels = pygame.sprite.Group()

    groups = {}
    groups['all_sprites'] = all_sprites
    groups['aguias'] = aguias
    groups['covides'] = covides
    groups['gels'] = gels
    
    score = 0
    lives = 3
    init_balife = 5
    covid_lives = 3
    keys_down = {}

    # lives_text = assets['life_font'].render('{:04d}'.format(lives), True, (255, 0, 0))
    # lives_text = pygame.transform.scale(lives_text, (20, 20))
    # text_rect_l = lives_text.get_rect()

    # --- Cria o jogador (balão)
    balao = Balao(groups, assets, init_balife)
    all_sprites.add(balao)

    balloon_life = Life(balao, assets)
    all_sprites.add(balloon_life)

    # --- Cria as covides
    covid = Covid(assets)
    all_sprites.add(covid)
    covides.add(covid)

    # --- Cria as águias e suas quantidades 
    for i in range(12):
        eagle1 = Eagle1(assets)
        eagle2 = Eagle2(assets)
        all_sprites.add(eagle1)
        all_sprites.add(eagle2)
        aguias.add(eagle1)
        aguias.add(eagle2)

    # --- Variável para o ajuste da velocidade
    clock = pygame.time.Clock()

    DONE = 0
    PLAYING = 1
    EXPLODING = 2
    state = PLAYING

    # ===== LOOP PRRINCIPAL =====    
    assets['music'].play(loops=-1)
    while state != DONE:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = DONE
            
            if state == PLAYING:
            # Verifica se apertou alguma tecla
                if event.type == pygame.KEYDOWN: # Dependendo da tecla, altera a velocidade  
                    
                    keys_down[event.key] = True
                    if event.key == pygame.K_LEFT:
                        balao.speedx -= 5
                        # balloon_life.speedx -= 5
                    if event.key == pygame.K_RIGHT:
                        balao.speedx += 5
                        # balloon_life.speedx += 5
                    if event.key == pygame.K_UP:
                        balao.speedy -= 3.5
                        # balloon_life.speedy -= 3.5
                    if event.key == pygame.K_DOWN:
                        balao.speedy += 3.5
                        # balloon_life.speedy += 3.5
                    if event.key == pygame.K_SPACE: # Atira álcool em gel
                        balao.shoot()
                # Verifica se soltou alguma tecla
                if event.type == pygame.KEYUP: # Dependendo da tecla, altera a velocidade
                    
                    if event.key in keys_down and keys_down[event.key]:
                        if event.key == pygame.K_LEFT:
                            balao.speedx += 5
                            # balloon_life.speedx += 5
                        if event.key == pygame.K_RIGHT:
                            balao.speedx -= 5
                            # balloon_life.speedx -= 5
                        if event.key == pygame.K_UP:
                            balao.speedy += 3.5
                            # balloon_life.speedy += 3.5
                        if event.key == pygame.K_DOWN:
                            balao.speedy -= 3.5
                            # balloon_life.speedy -= 3.5

        # --- Atualiza os sprites
        all_sprites.update()
        #aguias.update()

        if state == PLAYING:
        # --- Trata colisões
            col_1 = pygame.sprite.spritecollide(balao, aguias, True, pygame.sprite.collide_mask)
            for aguia in col_1:
                balao.lives -= 1
                score -= 50
                if aguia == eagle1:
                    eagle1 = Eagle1(assets)
                    all_sprites.add(eagle1)
                    aguias.add(eagle1)  
                elif aguia == eagle2:
                    eagle2 = Eagle2(assets)
                    all_sprites.add(eagle2) 
                    aguias.add(eagle2)
    # balao.kill()
    # balloon_life.kill()
            if len(col_1) > 0:
                assets['eagle_sound'].play()
                if balao.lives == 0:
                    lives -= 1
                    balloon_life.kill()
                    balao.kill()
                    assets['boom_sound'].play()
                    player = Player(balao.rect.center, assets['player_sheet'])
                    all_sprites.add(player)
                    state = EXPLODING
                    keys_down = {}
                    explosion_tick = pygame.time.get_ticks()
                    explosion_duration = player.frame_ticks * len(player.animation) + 500
            
            col_2 = pygame.sprite.spritecollide(balao, covides, True, pygame.sprite.collide_mask)
            for covid in col_2:
                covid = Covid(assets)
                all_sprites.add(covid)
                covides.add(covid)
                balao.lives -= 2
                score -= 100

            col_3 = pygame.sprite.spritecollide(covid, gels, True, pygame.sprite.collide_mask)
            for gel in col_3:
                covid_lives -= 1
                if covid_lives == 0:
                    covid.kill()
                    covid = Covid(assets)
                    all_sprites.add(covid)
                    covides.add(covid)
                    covid_lives = 3
                    balao.lives += 3
                    score += 200  

        elif state == EXPLODING:
            assets['music'].stop()
            now = pygame.time.get_ticks()
            if now - explosion_tick > explosion_duration:
                if lives == 0:
                    state = DONE
                else:
                    state = PLAYING
                    assets['music'].play()
                    balao = Balao(groups, assets, init_balife)
                    all_sprites.add(balao)
                    balloon_life = Life(balao, assets)
                    all_sprites.add(balloon_life)
                    # balao = Balao(groups, assets)
                    # all_sprites.add(balao)
                    # balloon_life.balao = balao
                    # balloon_life = Life(lives_text)
                    # all_sprites.add(balloon_life)

        # --- Saídas
        window.fill((0, 0, 0)) # Preenche com a cor branca
        window.blit(assets['image'], (0,move_image_1)) 
        window.blit(assets['image'], (0,move_image_2)) 

        # Muda as posições da imagem de fundo
        move_image_1 -= 2
        move_image_2 -= 2

        # Plota novamente após sair da tela
        if move_image_2 <= -HEIGHT:
            move_image_2 = HEIGHT
        if move_image_1 <= -HEIGHT:
            move_image_1 = HEIGHT

        # Desenha todos os sprites
        all_sprites.draw(window)

        # lives_text = assets['life_font'].render('{:04d}'.format(lives), True, (255, 0, 0))

        text_surface = assets['score_font'].render("{:08d}".format(score), True, (0, 0, 255))
        text_rect = text_surface.get_rect()
        text_rect.midtop = (WIDTH / 2,  0)
        window.blit(text_surface, text_rect)

        text_surface = assets['lives_font'].render(chr(9829) * lives, True, (255, 0, 0))
        text_rect = text_surface.get_rect()
        text_rect.bottomleft = (10, HEIGHT - 10)
        window.blit(text_surface, text_rect)

        pygame.display.update()  # Mostra o novo frame para o jogador

game_screen(window)
# ===== FINALIZAÇÃO =====
pygame.quit()  # Finaliza os recursos utilizados
