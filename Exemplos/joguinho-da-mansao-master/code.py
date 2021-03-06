# - CÓDIGO PRINCIPAL DO JOGO:

#----------------------------------------------------------------------#
# - Imports:

import pygame, sys
import random
from os import path
from pygame.locals import *
from imagens import *
from mapa import BLOCK,EMPTY,MAP1,Tile,MAP2,MAP3,PLATA,PLATM,PLATE,PLATD
from medidas import *
from sons import *

#----------------------------------------------------------------------#
#- Inicialização:
assets=load_assets(img_dir)
pygame.init()
pygame.mixer.init()

#---- Dados movimento:
espera = "espera"
pulando = "pulando"
pulandoesq="pulandoesq"
pulandodir="pulandodir"
helando="helando"
helandodir="helandodir"
helandoesq="helandoesq"
caindo = "caindo"
gravidade = 2
andandoesq="andandoesq"
andandodir="andandodir"

tamanho_do_pulo = 27
indefeso = "indefeso"
indefesoesq="indefesoesq"
indefesodir="indefesodir"

ataque = "ataque"
ataqueesq="atacandoesq"
ataquedir="atacandodir"

tomando_dano="tomando_dano"
tomando_danoesq="tomando_danoesq"
tomando_danodir="tomando_danodir"

defendendo="defendendo"
defendendodir="defendendodir"
defendendoesq="defendendoesq"
pronto_para_acao="pronto_para_acao"

dash="dash"
dashdir='dashdir'
dashesq="dashesq"

# ----- Gera tela principal
#monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
window = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Fenrly Park')
font = pygame.font.Font(path.join("fonts", 'Minecraft.ttf'), 16)
fontg = pygame.font.Font(path.join("fonts", 'Minecraft.ttf'), 100)
fontm = pygame.font.Font(path.join("fonts", 'Minecraft.ttf'), 30)



fullscreen = False


# SPRITESHEET

#----------------------------------------------------------------------#
# - Definindo a classe que configura o jogador:

class heroi(pygame.sprite.Sprite):
    """ Seta o jogador """
    def __init__(self,vida,dicio,blocks,chaves,platform):
        """ Recebe e define os dados iniciais do jogador  
        
        Keyword Arguments:
        vida -- quantia de vida do jogador
        dicio-- dicionario com todas as animacoes
        blocks -- blocos do chão
        chaves -- objetos para passar de fase
        platform -- plataformas de madeira/ diferenciação do chão
        """
        pygame.sprite.Sprite.__init__(self)
        
        self.platforms = platform
        self.blocks=blocks
        self.animations = {
            indefesoesq: dicio['existindoesq'][0:4],
            indefesodir: dicio['existindodir'][0:4],

            ataqueesq: dicio['atacandoesq'][0:2],
            ataquedir:dicio["atacandodir"][0:2],

            andandoesq:dicio["andandoesq"][0:2],
            andandodir:dicio["andandodir"][0:2],

            tomando_danoesq:dicio["danoesq"][1:2],
            tomando_danodir:dicio["danodir"][1:2],

            pulandoesq:dicio["pulandoesq"][2:3],
            pulandodir:dicio["pulandodir"][2:3],

            helandoesq:dicio["helandoesq"][0:14],
            helandodir:dicio["helandodir"][0:14],

            defendendoesq:dicio["defendendoesq"][0:3],
            defendendodir:dicio["defendendodir"][0:3],

            dashdir:dicio["dashdir"][0:1],
            dashesq:dicio["dashesq"][0:1]
            }
        
        self.estado = indefesodir
        self.animation = self.animations[self.estado]
        self.frame = 0
        self.image = self.animation[self.frame]

        self.state = espera
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.centerx = 50
        self.rect.bottom = (12*48)-10
        self.speedx = 0
        self.speedy= 0
        
        self.vida=vida
        self.quantdash=3
        self.acao_ticks = 300*2
        self.frame_ticks = 300
        self.last_update = pygame.time.get_ticks()
        self.ultimo_lado=0
        self.hora_da_acao=pygame.time.get_ticks()
        self.timer_do_tutorial = pygame.time.get_ticks()
        self.duracao_do_tutorial=1000
        self.highest_y = self.rect.bottom

    # Update    
    def update(self): 
        """ Atualiza tela (sprites e sons), estado de jogo e configurações do jogador (estados, velocidade e posição) """
        if self.vida <= 0:
            gameoversound.play()
            self.kill()
            barra.kill()
            estado_do_jogo.aba = "gameover"

        if self.state != caindo:
            self.highest_y = self.rect.bottom   

        now = pygame.time.get_ticks()
        elapsed2_ticks = now - self.last_update

        if self.ultimo_lado>4:
            self.ultimo_lado=4
        elif self.ultimo_lado<-4:
            self.ultimo_lado=-4

        if elapsed2_ticks > self.frame_ticks:
            self.last_update = now
            self.frame += 1

            if self.speedy!=0:
                if self.ultimo_lado==4:
                    self.animation = self.animations[pulandodir]
                    self.mask = pygame.mask.from_surface(self.image)
                    
                if self.ultimo_lado==-4:
                    self.animation = self.animations[pulandoesq]
                    self.mask = pygame.mask.from_surface(self.image)
                    
                    
            elif self.estado==indefeso:
                if self.speedx>0:
                    self.animation = self.animations[andandodir]
                    self.mask = pygame.mask.from_surface(self.image)
                
                    
                if self.speedx<0:
                    self.animation = self.animations[andandoesq]
                    self.mask = pygame.mask.from_surface(self.image)
                    
                if self.speedx==0:
                    if self.ultimo_lado==4:
                        self.animation = self.animations[indefesodir]
                        self.mask = pygame.mask.from_surface(self.image)
                           
                    if self.ultimo_lado==-4:
                        self.animation = self.animations[indefesoesq]
                        self.mask = pygame.mask.from_surface(self.image)

            elif self.estado==tomando_dano:
                if self.ultimo_lado==-4:
                    self.animation = self.animations[tomando_danodir]
                    self.mask = pygame.mask.from_surface(self.image)
                    
                if self.ultimo_lado==4:
                    self.animation = self.animations[tomando_danoesq]
                    self.mask = pygame.mask.from_surface(self.image)
    
            elif self.estado==ataque:
                if self.ultimo_lado==4:
                    self.animation = self.animations[ataquedir]
                    self.mask = pygame.mask.from_surface(self.image)
        
                if self.ultimo_lado==-4:
                    self.animation = self.animations[ataqueesq]
                    self.mask = pygame.mask.from_surface(self.image)

            elif self.estado==helando:
                if self.ultimo_lado==4:
                    self.animation = self.animations[helandodir]
                    self.mask = pygame.mask.from_surface(self.image)
         
                if self.ultimo_lado==-4:
                    self.animation = self.animations[helandoesq]
                    self.mask = pygame.mask.from_surface(self.image)   

            elif self.estado==defendendo:
                if self.ultimo_lado==4:
                    self.animation = self.animations[defendendodir]
                    self.mask = pygame.mask.from_surface(self.image)
        
                if self.ultimo_lado==-4:
                    self.animation = self.animations[defendendoesq]
                    self.mask = pygame.mask.from_surface(self.image)

            elif self.estado==dash:
                if self.ultimo_lado==4:
                    self.animation = self.animations[dashdir]
                    self.mask = pygame.mask.from_surface(self.image)
        
                if self.ultimo_lado==-4:
                    self.animation = self.animations[dashesq]
                    self.mask = pygame.mask.from_surface(self.image)
            if self.frame >= len(self.animation):
                self.frame = 0

            center = self.rect.center
            centerx=self.rect.centerx
            centery=self.rect.centery
            self.image = self.animation[self.frame]
            self.rect = self.image.get_rect()

            if self.estado==ataque:
                if self.ultimo_lado==4:
                    self.rect.centerx = centerx+4
                    self.rect.centery = centery
                    
                if self.ultimo_lado==-4:
                    self.rect.centerx = centerx-4
                    self.rect.centery = centery
            else:       
                self.rect.center = center

        
        # Atualização da posição do heroi
        if  self.estado!=dash and self.estado!=defendendo and self.estado!=helando:
            self.rect.x += self.speedx
        elif self.estado==defendendo:
            self.rect.x += self.speedx*0.25
        elif self.estado==dash:
            self.rect.x += self.speedx*41
            self.estado=indefeso
        elif self.estado==helando:
            self.rect.x += 0

        if self.estado==helando:
             if agora -self.hora_da_acao>self.acao_ticks*10:
                self.estado=indefeso
        if self.estado!=indefeso and self.estado!=tomando_dano and self.estado!=helando:          
            if agora -self.hora_da_acao>self.acao_ticks:
                self.estado=indefeso

        if self.estado==tomando_dano:
             if agora -self.hora_da_acao>self.acao_ticks/2:
                self.estado=indefeso

        self.speedy += gravidade
        # Atualiza o estado para caindo
        if self.speedy > 0:
            self.state = caindo
        self.rect.y += self.speedy
        # Se bater no chão, para de cai
        collisionsblock = pygame.sprite.spritecollide(self, self.blocks, False)
        # Corrige a posição do personagem para antes da colisão
        for collision in collisionsblock:
            # Estava indo para baixo
            
            if self.speedy > 0:

                self.rect.bottom = collision.rect.top
                # Se colidiu com algo, para de cair
                self.speedy = 0
                # Atualiza o estado para parado
                self.state = espera
            # Estava indo para cima
            elif self.speedy < 0:
                
                self.rect.top = collision.rect.bottom
                # Se colidiu com algo, para de cair
                self.speedy = 0
                # Atualiza o estado para parado
                self.state = espera
        if self.speedy > 0:  # Está indo para baixo
            collisionsplata = pygame.sprite.spritecollide(self, self.platforms, False)
            # Para cada tile de plataforma que colidiu com o personagem
            # verifica se ele estava aproximadamente na parte de cima
            for platform in collisionsplata:
                # Verifica se a altura alcançada durante o pulo está acima da
                # plataforma.
                if self.highest_y <= platform.rect.top:
                    self.rect.bottom = platform.rect.top
                    # Atualiza a altura no mapa
                    self.highest_y = self.rect.bottom
                    # Para de cair
                    self.speedy = 0
                    # Atualiza o estado para parado
                    self.state = espera
        # Mantem dentro da tela
        if self.rect.right > largura:
            self.rect.right = largura
        if self.rect.left < 0:
            self.rect.left = 0

        collisionsblocks2 = pygame.sprite.spritecollide(self, self.blocks, False, pygame.sprite.collide_mask)
        # Corrige a posição do personagem para antes da colisão
        
        for collision in collisionsblocks2:
            # Estava indo para a direita
            if self.speedx > 0:
                self.rect.right = collision.rect.left
            # Estava indo para a esquerda
            elif self.speedx < 0:
                self.rect.left = collision.rect.right

        # Morre quando cai no mapa
        if self.rect.top > altura:
            player.kill()
            gameoversound.play()
            estado_do_jogo.aba = 'gameover'
        
     
    def pulo(self):
        """ Define estado de pulo - jogador pulando """
        if self.state == espera:
            self.speedy -= tamanho_do_pulo
            pulosond.play()
            self.state = pulando

    def ataque(self):
        """  Define estado de ataque - jogador atacando """
        if self.state==espera:
        # Verifica quantos ticks se passaram desde o último tiro.
            elapsed_ticks = agora - self.hora_da_acao
        # Se já pode atirar novamente...    
            if elapsed_ticks > self.acao_ticks*1.5:
            # Marca o tick da nova imagem.
                self.hora_da_acao = agora
                if self.estado == indefeso:
                    cortandoar.play()    
                    self.estado = ataque
                

    def defesa(self):
        """ Define o estado de defesa - jogador se defendendo """
        if self.state==espera:
        # Verifica quantos ticks se passaram desde o último tiro.
            elapsed_ticks = agora - self.hora_da_acao
        # Se já pode atirar novamente...   
            if elapsed_ticks > self.acao_ticks:
            # Marca o tick da nova imagem.
                self.hora_da_acao = agora
                if self.estado == indefeso:
                    self.estado = defendendo

    def dash(self):
        """ Define o estado de dash - jogador dando dash """
        if self.quantdash>0:
            if self.speedx!=0:   
            # Verifica quantos ticks se passaram desde o último tiro.
                elapsed_ticks = agora - self.hora_da_acao

            # Se já pode atirar novamente...
                
                if elapsed_ticks > self.acao_ticks:
                # Marca o tick da nova imagem.
                    self.hora_da_acao = agora
                    if self.estado == indefeso:
                        dashsound.play()
                        self.estado = dash
                        self.quantdash-=1  

def colisoes_chaves():
    """ Define as colisões com as chaves para passar de fase - jogador pegando a chave (funcionou melhor como uma funcao separada)"""
    global fase
    if estado_do_jogo.aba=="jogando":
        colisao=pygame.sprite.spritecollide(player,all_chaves,False, pygame.sprite.collide_mask)
        if len(colisao)>0:
            chavesound.play()
            all_chaves.empty()
            blocks.empty()
            all_plata.empty()
            all_sprites.empty()
            all_enemis.empty()
            all_pistas.empty()
            all_cura.empty()
            
            colisao.clear()
            
            fase+=1
            
            estado_do_jogo.aba = "troca_de_fase"

          
#----------------------------------------------------------------------#                 
# - Definindo a classe que configura os inimigos:

class inimigos(pygame.sprite.Sprite):
    """ Seta os inimigos(fantasmas) """
    def __init__(self,player,dicio,vidaini):
        """ Recebe e define condições iniciais do inimigo
        
        Keywor Arguments:
        player -- jogador
        dicio -- dicionario com todas as animacoes 
        vidaini -- vida do inimigo
        """
        pygame.sprite.Sprite.__init__(self)
        self.estado=espera
        self.animations = {
            espera: dicio['inimigo'][0:6]
            }
        
        
        self.animation = self.animations[espera]
        self.frame = 0
        self.image = self.animation[self.frame]
    
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint(200,largura)
        self.rect.bottom = random.randint(0,altura-500)
        self.speedx_inimigo = 0
        self.speedy_inimigo= 0
        self.vida=vidaini
        self.frame_ticks = 200
        self.last_update = pygame.time.get_ticks()
        self.cria_barra()
        self.variant=False
        self.hora_da_acao=pygame.time.get_ticks()
        self.sound_tick=20000

    def update(self):
        """Atualiza tela (sprites e sons), configurações dos inimigos (estados, velocidade , posição e colisoes)  """
        now = pygame.time.get_ticks()
        elapsed2_ticks = now - self.last_update

        if elapsed2_ticks > self.frame_ticks:
            self.last_update = now
            self.frame += 1
            self.animation = self.animations[espera]

            if self.frame >= len(self.animation):
                self.frame = 0
   
            center = self.rect.center
            self.image = self.animation[self.frame]
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect()
            self.rect.center = center

        if self.vida==0:
            self.kill()
            self.barra_vermelha.kill()  
            
        if self.estado==espera:
            self.rect.x += self.speedx_inimigo
            self.rect.y += self.speedy_inimigo
        elif player.hora_da_acao+player.acao_ticks*1.5<agora:
            self.estado=espera
        if player.rect.x-self.rect.x>0 :
            self.speedx_inimigo = 1
            
        if player.rect.x-self.rect.x<0 :
            self.speedx_inimigo = -1

        if player.rect.y-self.rect.y>0 :
            self.rect.y != altura
            self.speedy_inimigo = 1 

        if player.rect.y-self.rect.y<0 :
            self.speedy_inimigo = -1
    
        colisao2 = pygame.sprite.collide_rect(player, self)   
        if self.hora_da_acao+self.sound_tick<agora:
            fantasmasound.play()
            self.hora_da_acao=agora

        if colisao2==True:
                
            if player.estado==indefeso or player.estado==helando:  
                danoplayer.play()
                if player.rect.bottom-self.rect.top<0:
                    player.estado=tomando_dano
                    player.hora_da_acao=agora
                    player.vida-=10                       
                    player.rect.x-=60
                    self.rect.x+=60

                elif player.rect.right-self.rect.centerx<0:
                    player.estado=tomando_dano
                    player.hora_da_acao=agora
                    player.vida-=10                       
                    player.rect.x-=60
                    self.rect.x+=60
                    
                elif player.rect.left-self.rect.centerx>0:
                    player.estado=tomando_dano
                    player.hora_da_acao=agora
                    player.vida-=10                       
                    player.rect.x+=60
                    self.rect.x-=60
                else :
                    player.estado=tomando_dano
                    player.hora_da_acao=agora
                    player.vida-=10                       
                    player.rect.x+=60
                    self.rect.x-=60

            
            if player.estado==ataque and player.ultimo_lado==4:
                cortandoar.stop()
                inimigo_acerto.play()
                if player.rect.right-self.rect.centerx<0:
                    self.vida=self.vida-10
                    self.rect.x+=40
                    self.rect.y-=20  
                    self.estado=tomando_dano               
                    player.rect.x-=40

            if player.estado==ataque and player.ultimo_lado==-4:   
                cortandoar.stop()
                inimigo_acerto.play()     
                if player.rect.left-self.rect.centerx>0:
                    self.vida=self.vida-10
                    self.estado=tomando_dano
                    self.rect.x-=40
                    self.rect.y-=20                    
                    player.rect.x+=40


            if player.estado==defendendo:
                defendendosound.play()
                self.estado="bloqueado"
        
                if player.rect.right-self.rect.centerx<0:
                    self.rect.x+=90
                    self.rect.y-=25    
                
                
                elif player.rect.left-self.rect.centerx>=0:    
                    self.rect.x-=90
                    self.rect.y-=25   

    def cria_barra(self):
        """ Cria uma barra de vida para cada inimigo """
        self.barra_vermelha= adicionais(assets[BARRA_VERMELHA_IMG],self,barra_largura,0,0)
        all_sprites.add(self.barra_vermelha)
    
#----------------------------------------------------------------------#
# - Definindo a classe que configura o modo de jogo (jogando, menu, main menu, troca de fases, game over):
 
class modo_de_jogo():
    """ Define o que estará acontecendo na tela """
    def __init__(self):
        """ Define os dados iniciais do jogo """
        self.aba="menu"
        self.timer_do_tutorial = pygame.time.get_ticks()
        self.duracao_do_tutorial=1000

    def esta_dentro(self,pos,x,y):
        """ Recebe a posição do mouse e define a posição dos botões na tela """
        self.posicaox=x
        self.posicaoy=y
        
        if pos[0]> self.posicaox and pos[0]<self.posicaox+playapertado_largura:
            if pos[1]>self.posicaoy and pos[1]<self.posicaoy+playapertado_altura:
                return True
        else:
            return False
        
    def game_over(self):
        """ Define o que acontece quando o jogo entra em game over """
        global sequencia
        pygame.mixer.music.stop()
        andandosound.stop()
        for event in pygame.event.get():      
            pos=pygame.mouse.get_pos()
        # ----- Verifica consequências
            if event.type == pygame.QUIT:
                
                pygame.quit()  
            if sequencia==8:
                window.fill((0, 0, 0))
                sequencia=9
            if sequencia==9:
                window.blit(assets[GAMEOVER1], (0,0))
                window.blit(assets[SAIR], ((largura/2)-(menu_largura/2), altura-100))
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button==1 and self.esta_dentro(pos,(largura/2)-(menu_largura/2), altura-100):
                        sequencia=10
                        
                        self.timer_do_tutorial=agora
            tempo2 = agora - self.timer_do_tutorial
            if sequencia==10:
                window.blit(assets[GAMEOVER1], (0,0))
                window.blit(assets[SAIRAPERTADO],((largura/2)-(menu_largura/2), altura-100))  
                if  tempo2 > self.duracao_do_tutorial:
                    self.timer_do_tutorial=agora
                    sequencia=11
            if sequencia==11:
                self.aba="mensagem"

        pygame.display.update()

    def jogando(self):
        """ Define as ações que podem ocorrer durante o jogo """
        text2= font.render(('| '*player.quantdash), True, (255, 255, 0))
        for event in pygame.event.get():
        # ----- Verifica consequências
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                pygame.quit() 
        # Verifica se apertou alguma tecla.
            if event.type == pygame.KEYDOWN:
                keys_down[event.key] = True 
                
            # Dependendo da tecla, altera a velocidade.
                if event.key == pygame.K_a:
                    player.ultimo_lado=-4.0
                    if player.estado!=helando:
                        andandosound.play()
                    player.speedx -= 4.0
                if event.key == pygame.K_d:  
                    player.ultimo_lado=4.0   
                    if player.estado!=helando:
                        andandosound.play()             
                    player.speedx += 4.0
                if event.key == pygame.K_SPACE:
                    player.pulo()
                if event.key == pygame.K_ESCAPE:
                    self.aba = 'main menu'
                if event.key == pygame.K_l:
                    player.dash() 

        # Verifica se soltou alguma tecla.
            if event.type == pygame.KEYUP:
                if event.key in keys_down and keys_down[event.key]:
            # Dependendo da tecla, altera a velocidade.
                    if event.key == pygame.K_a:   
                        player.speedx += 4.0
                        andandosound.stop()
                    if event.key == pygame.K_d:
                        player.speedx -= 4.0
                        andandosound.stop()
                    if event.key == pygame.K_k:   
                        player.ataque()
                    if event.key == pygame.K_j:
                        player.defesa()      
     
    # ----- Gera saídas
        window.fill((0, 0, 0))
        all_sprites.draw(window)
       
        window.blit(text2,(110,13))
        
        colisoes_chaves()
                
        all_sprites.update()
        
    # ----- Atualiza estado do jogo
        pygame.display.update()  


    def menu(self):
        """ Define a tela inicial do jogo """
        global sequencia
        for event in pygame.event.get():
            pos=pygame.mouse.get_pos()
            
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
    #---- comando para testar
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    sequencia = 8
                    self.aba="jogando"
        
        # Tutorial:
            tempo=agora-self.timer_do_tutorial
            if sequencia==1:
                text= fontg.render('Fenrly Park', True, (255, 0, 0))
                window.blit(assets[TELA_INICIAL_IMG], (0,0))
                window.blit(assets[PLAY], ((largura/2)-(play_largura/2), altura-100))
                text_rect=text.get_rect()
                text_largura=text_rect.width
                
                window.blit(text,((largura/2)-text_largura/2,11))
                if event.type == pygame.MOUSEBUTTONDOWN:
                    
                    if event.button==1 and self.esta_dentro(pos,(largura/2)-(play_largura/2), altura-100):
                        sequencia=2
                        self.timer_do_tutorial=agora
                        tempo=agora-self.timer_do_tutorial  

            if sequencia==2:
                text= fontg.render('Fenrly Park', True, (255, 0, 0))
                window.blit(assets[TELA_INICIAL_IMG], (0,0))
                window.blit(assets[PLAY], ((largura/2)-(play_largura/2), altura-100))
                text_rect=text.get_rect()
                text_largura=text_rect.width
                window.blit(assets[TELA_INICIAL_IMG], (0,0))
                window.blit(text,((largura/2)-text_largura/2,11))
                window.blit(assets[PLAYAPERTADO],((largura/2)-(play_largura/2), altura-100))  
                if  tempo> self.duracao_do_tutorial-20:
                    self.timer_do_tutorial=agora
                    tempo=agora-self.timer_do_tutorial
                    sequencia=3
                    
            if sequencia==3:
                window.fill((5, 32, 74))
                f1 = fontm.render('Ola, Hercule Poirot. Como vai?',True, (255, 255, 255))
                
                f2 = fontm.render('Fico muito feliz de encontra-lo aqui em Kings Abbot. Sei que era bem',True, (255, 255, 255))
                f3 = fontm.render('proximo de meu tio, Roger Ackroyd, portanto ja assumo que saiba de sua',True, (255, 255, 255))
                f4 = fontm.render('misteriosa morte ontem de noite. Escrevo-lhe esta carta com muito pesar',True, (255, 255, 255))
                f5 = fontm.render('para lhe fazer um pedido. Preciso da verdade. Sei que e o unico que pode',True, (255, 255, 255))
                f6 = fontm.render('me ajudar nessa missao, ja que o senhor e famoso por solucionar crimes',True, (255, 255, 255))
                f7 = fontm.render('inimaginaveis e muitas vezes considerados impossiveis. Acredito fortemente',True, (255, 255, 255))
                f8 = fontm.render('que nao foi Ralph Paton, meu noivo e filho adotivo de meu tio, como todos',True, (255, 255, 255))
                f9 = fontm.render('afirmam ser... Ele podia ter um temperamento agressivo as vezes mas senhor,',True, (255, 255, 255))
                f10 = fontm.render('afirmo que ponho minha mao no fogo por ele! Ele nunca poderia... Por favor',True, (255, 255, 255))
                f11 = fontm.render('me ajude a descobrir a verdade.',True, (255, 255, 255))
            
                f12 = fontm.render('Atenciosamente,',True, (255, 255, 255))
                f13 = fontm.render('Flora Ackroyd',True, (255, 255, 255))

                text_rectf1=f1.get_rect()
                
                text_alturaf1=text_rectf1.height
                
                window.blit(f1,(30, 100))
                window.blit(f2,(30, 100 + text_alturaf1*3))
                window.blit(f3,(30, 100 + text_alturaf1*4))
                window.blit(f4,(30, 100 + text_alturaf1*5))
                window.blit(f5,(30, 100 + text_alturaf1*6))
                window.blit(f6,(30, 100 + text_alturaf1*7))
                window.blit(f7,(30, 100 + text_alturaf1*8))
                window.blit(f8,(30, 100 + text_alturaf1*9))
                window.blit(f9,(30, 100 + text_alturaf1*10))
                window.blit(f10,(30, 100 + text_alturaf1*11))
                window.blit(f11,(30, 100 + text_alturaf1*12))
                window.blit(f12,(30, 100 + text_alturaf1*14))
                window.blit(f13,(30, 100 + text_alturaf1*15))

                window.blit(assets[NEXT],((largura/2)-(next_largura/2),altura-100))  
                if event.type == pygame.MOUSEBUTTONDOWN:
                    
                    if event.button==1 and self.esta_dentro(pos,(largura/2)-(play_largura/2), altura-100):
               
                        self.timer_do_tutorial=agora
                        tempo=agora-self.timer_do_tutorial
                        sequencia=4
            
            if sequencia==4:
                pygame.draw.rect(window,(5, 32, 74),((largura/2)-(next_largura/2), altura-100,next_largura,next_altura))
                window.blit(assets[NEXTAPERTADO],((largura/2)-(nextapertado_largura/2), altura-100))  
                if  tempo> self.duracao_do_tutorial:
                    self.timer_do_tutorial=agora
                    tempo=agora-self.timer_do_tutorial
                    sequencia=5

            if sequencia==5:
                window.fill((5, 32, 74))
                h1 = fontm.render('Cara Ms. Ackroyd,',True, (255, 255, 255))

                h2 = fontm.render('Infelizmente fiquei sabendo do ocorrido essa manha. Mes condoleances',True, (255, 255, 255))
                h3 = fontm.render('mademoiselle, tenho certeza de que o Mr. Ackroyd era muito querido.',True, (255, 255, 255))
                h4 = fontm.render('Entendo seu posicionamento para defender seu noivo, mas devo',True, (255, 255, 255))
                h5 = fontm.render('alerta-la de que se eu comecar a investigacao, nao terei nenhum',True, (255, 255, 255))
                h6 = fontm.render('resultado alem da verdade. Toute la verite. Se a resposta for sim,',True, (255, 255, 255))
                h7 = fontm.render('entao aceito. E espero que voce nao se arrependa dessas palavras.',True, (255, 255, 255))
                
                h8 = fontm.render('Atenciosamente,',True, (255, 255, 255))
                h9 = fontm.render('Monsieur Poirot',True, (255, 255, 255))
                
                text_recth1=h1.get_rect()
                
                text_alturah1=text_recth1.height
                
                window.blit(h1,(30, 100))
                window.blit(h2,(30, 100 + text_alturah1*3))
                window.blit(h3,(30, 100 + text_alturah1*4))
                window.blit(h4,(30, 100 + text_alturah1*5))
                window.blit(h5,(30, 100 + text_alturah1*6))
                window.blit(h6,(30, 100 + text_alturah1*7))
                window.blit(h7,(30, 100 + text_alturah1*8))
                window.blit(h8,(30, 100 + text_alturah1*10))
                window.blit(h9,(30, 100 + text_alturah1*11))

                window.blit(assets[NEXT],((largura/2)-(next_largura/2), altura-100))  
                if event.type == pygame.MOUSEBUTTONDOWN:
                    
                    if event.button==1 and self.esta_dentro(pos,(largura/2)-(play_largura/2), altura-100):
               
                        self.timer_do_tutorial=agora
                        tempo=agora-self.timer_do_tutorial
                        sequencia=6
            
            if sequencia==6:
                
                pygame.draw.rect(window,(5, 32, 74),((largura/2)-(next_largura/2), altura-100,next_largura,next_altura))
                window.blit(assets[NEXTAPERTADO],((largura/2)-(next_largura/2), altura-100))  
                if  tempo> self.duracao_do_tutorial:
                    self.timer_do_tutorial=agora
                    tempo=agora-self.timer_do_tutorial
                    sequencia=7
            
            # TUTORIAL
            if sequencia==7 :         
                window.blit(assets[TUTORIAL], (0, 0))
                if  tempo> self.duracao_do_tutorial:
                    window.blit(assets[RESUME], ((largura/2)-(resume_largura/2), altura-100))
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button==1 and self.esta_dentro(pos,(largura/2)-(resume_largura/2), altura-100):
                            sequencia=8
                            self.timer_do_tutorial=agora
                            tempo=agora-self.timer_do_tutorial
                            
            if sequencia==8:
                window.blit(assets[TUTORIAL], (0, 0))
                window.blit(assets[RESUMEAPERTADO],((largura/2)-(resume_largura/2), altura-100))  
                if  tempo> self.duracao_do_tutorial:
                    self.aba="jogando"
                    window.fill((0, 0, 0))         

            pygame.display.update()
            
    def troca_de_fase(self):
        """ Define o que ocorre quando o jogador pega a chave - trocas de fase """
        global fase
        
        andandosound.stop()
        if fase!=4:
            pygame.mixer.music.pause()
            window.fill((0, 0, 0))
            text=font.render('Nivel {0}'.format(fase), True, (255, 255, 255))
            text_rect=text.get_rect()
            text_largura=text_rect.width
            text_altura=text_rect.height
            window.blit(text,((largura/2)-text_largura/2,(altura/2)-text_altura/2))
            player.rect.centerx = 50
            player.rect.bottom = 12*48
            player.quantdash=3
            player.speedx=0
            player.speedy=0
                    
            window.blit(assets[RESUME], ((largura/2)-(resume_largura/2), altura-100))
                
            for event in pygame.event.get():
                
                pos=pygame.mouse.get_pos()
                
                if event.type == pygame.QUIT:
                    pygame.mixer.music.stop()
                    pygame.quit()
            
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button==1 and self.esta_dentro(pos,(largura/2)-(resume_largura/2), altura-100):
                        
                        fases(fase)
                        for i in range(2):
                            inimigo = inimigos(player,dicio,vida_inimigo)
                            all_sprites.add(inimigo)
                            all_enemis.add(inimigo)
                            pygame.mixer.music.unpause()
                        self.aba="jogando"
        else:
            self.aba="mensagem"        

        pygame.display.update() 


    def main_menu(self):
        """ Define o estado de pause """
        text = font.render('Aperte Esc para voltar', True, (255, 255, 255))
        text_rect=text.get_rect()
        text_largura=text_rect.width
        text_altura=text_rect.height
        player.speedx=0
        player.speedy=0
        for event in pygame.event.get():
            
        # ----- Verifica consequências
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.aba = 'jogando'
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                pygame.quit() 
            

        window.fill((0, 0, 50))
        window.blit(text,((largura/2)-text_largura/2,(altura/2)-text_altura/2))
        pygame.display.update() 

    def dicas(self):
        """ Define o que ocorre quando o jogador pega as pistas """
        global fase
        pygame.mixer.music.pause()
        andandosound.stop()
        player.speedx=0
        player.speedy=0
        window.fill((0,0,0))
        if fase==1:
            window.blit(assets[CARTA_ABERTA],(0,0))
            text = font.render('Recebemos de Roger Ackroyd a quantia de $41260,44 xelins,',True, (0, 0, 0))
            t2 =   font.render('correspondente a quarenta e um mil duzentos e sessenta xelins',True, (0, 0, 0))
            t3 =   font.render('e quarenta e quatro cents. Para clareza nos, da empresa Orion',True, (0, 0, 0))
            t4 =   font.render('Communications, firmamos o presente na cidade Kings Abbot de',True, (0, 0, 0))
            t5 =   font.render('no dia 2 de marco de 1933.',True, (0, 0, 0))
            t6 =   font.render('Assinatura vendedor: Richard Moore',True, (0, 0, 0))
            t7 =   font.render('Assinatura comprador: Roger Ackroyd',True, (0, 0, 0))
            t8 =   font.render('Pensamento: O recibo de um telegrama por Roger Ackroyd... mas onde ele' ,True, (0, 0, 0))
            t9 =   font.render('deve ter deixado? Certamente nao em seu escritorio e nem em Fernly' ,True, (0, 0, 0))
            t10 =  font.render('Park, se nao a policia ja teria o apreendido ou eu teria notado' ,True, (0, 0, 0))
            t11 =  font.render('tamanha tecnologia.', True, (0,0,0))
  
            text_rect=text.get_rect()
            text_largura=text_rect.width
            text_altura=text_rect.height

            window.blit(text,((largura/2)-(text_largura/2)-80,(150)))
            window.blit(t2,((largura/2)-(text_largura/2)-80,(150+text_altura+3)))
            window.blit(t3,((largura/2)-(text_largura/2)-80,(150+text_altura*2+3*2)))
            window.blit(t4,((largura/2)-(text_largura/2)-80,(150+text_altura*3+3*3)))
            window.blit(t5,((largura/2)-(text_largura/2)-80,(150+text_altura*4+3*4)))
            window.blit(t6,((largura/2)-(text_largura/2)-80,(170+text_altura*5+3*5)))
            window.blit(t7,((largura/2)-(text_largura/2)-80,(170+text_altura*6+3*6)))
            window.blit(t8,((largura/2)-(text_largura/2)-80,(190+text_altura*7+3*7)))
            window.blit(t9,((largura/2)-(text_largura/2)-80,(190+text_altura*8+3*8)))
            window.blit(t10,((largura/2)-(text_largura/2)-80,(190+text_altura*9+3*9)))
            window.blit(t11,((largura/2)-(text_largura/2)-80,(190+text_altura*10+3*10)))
            

        window.blit(assets[RESUME], ((largura/2)-(resume_largura/2), altura-100))
        if fase==2:
            
            text = font.render('Aparentemente existem pegadas de lama no parapeito da janela ...', True, (255, 255, 255)) 
            t2=font.render('Tem formato de uma bota... agora falta achar quem teria as botas que combinam com o formato.', True, (255, 255, 255))
            text_rect=text.get_rect()
            text_largura=text_rect.width
            text_altura=text_rect.height
            window.blit(text,((largura/2)-(text_largura/2)-20,(250)))
            window.blit(t2,((largura/2)-(text_largura/2)-20,(250+text_altura+50)))
        window.blit(assets[RESUME], ((largura/2)-(resume_largura/2), altura-100))
        if fase==3:
            
            text = font.render('De R., 13 de marco', True, (255, 255, 255))
            
            a1 = font.render('Achei esse anel de noivado em um laguinho perto da casa.', True, (255, 255, 255))
            a2 = font.render('Aparentemente foi jogado pela janela. Quem sera R?', True, (255, 255, 255))
            a3 = font.render('Roger? Depois da morte de Mrs. Ackroyd nao esperaria', True, (255, 255, 255))
            a4 = font.render('ele se comprometendo com alguem, mas certamente ele a irritou', True, (255, 255, 255))
            a5 = font.render('criando, assim, uma possivel suspeita para o caso.', True, (255,255,255))
            text_rect=text.get_rect()
            text_largura=text_rect.width
            text_altura=text_rect.height
            
            window.blit(text,((largura/2)-(text_largura/2)-80,(250)))
            window.blit(a1,((largura/2)-(text_largura/2)-80,(270+text_altura)))
            window.blit(a2,((largura/2)-(text_largura/2)-80,(270+text_altura*2)))
            window.blit(a3,((largura/2)-(text_largura/2)-80,(270+text_altura*3)))
            window.blit(a4,((largura/2)-(text_largura/2)-80,(270+text_altura*4)))
            window.blit(a5,((largura/2)-(text_largura/2)-80,(270+text_altura*5)))

        window.blit(assets[RESUME], ((largura/2)-(resume_largura/2), altura-100))
        for event in pygame.event.get():
            
            pos=pygame.mouse.get_pos()
            
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
        
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button==1 and self.esta_dentro(pos,(largura/2)-(resume_largura/2), altura-100):
                    pegando_item.play()
                    pygame.mixer.music.unpause()
                    self.aba="jogando"
        pygame.display.update()
        
    def fim_jogo(self):
        """ Define a tela de finalização após todas as fases """
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                
            pygame.mixer.music.pause()
            andandosound.stop()
            player.speedx=0
            player.speedy=0
            
            window.fill((0,0,0))
            
            textf = fontm.render('Obrigado por jogar Fernly Park!', True, (255, 255, 255))
            
            textf2 = fontm.render('Um jogo por: ', True, (255, 255, 255))

            textf3 = fontm.render('- Andressa Silva', True, (255, 255, 255))
            textf4 = fontm.render('- Enrico Lopez', True, (255, 255, 255))
            textf5 = fontm.render('- Luiza Valezim', True, (255, 255, 255))
            textf6 = fontm.render('-- Alunos do 1 semestre de engenharia no Insper 2020.1 --', True, (255, 255, 255))
            
            textff=fontm.render('to be continued ...', True, (255, 255, 255))
            text_rectf=textf.get_rect()
            text_larguraf=text_rectf.width
            text_alturaf=text_rectf.height
            

            text_rectf2=textf2.get_rect()
            text_larguraf2=text_rectf2.width
            text_alturaf2=text_rectf2.height
            
            window.blit(textf,((largura/4)-(text_larguraf/2),(100)))
            window.blit(textf2,((largura/4)-(text_larguraf/2),(100+text_alturaf)))
            window.blit(textf3,((largura/4)-(text_larguraf/2),(100+50+text_alturaf*2)))
            window.blit(textf4,((largura/4)-(text_larguraf/2),(100+50*2+text_alturaf*3)))
            window.blit(textf5,((largura/4)-(text_larguraf/2),(100+50*3+text_alturaf*4)))
            window.blit(textf6,((largura/4)-(text_larguraf/2),(100+50*4+text_alturaf*5)))
            
            window.blit(textff,((largura/2)-text_larguraf2/2,(altura-text_alturaf2-20)))
        
        pygame.display.update()


    def controlador_menu(self):
        """ Controla o que aparece em cada estado de jogo """
        if self.aba=="menu":
            self.menu()
        if self.aba=="jogando":
            self.jogando()
        if self.aba=='main menu':
            self.main_menu()
        if self.aba=="gameover":
            self.game_over()
        if self.aba=="troca_de_fase":
            self.troca_de_fase()
        if self.aba=="dicas":
            self.dicas()
        if self.aba=="mensagem":
            self.fim_jogo()
          
        
#----------------------------------------------------------------------#
# - Definindo a classe que configura barras de vida e chaves para passar de fase:

class adicionais(pygame.sprite.Sprite):
    """ Define a posição das barras de vida, das barras de estamina, das chaves e das dicas"""
    def __init__(self,img,quem_ta_seguindo,largura,posx,posy):  
        """ Recebe imagem, quem será seguido, a largura da barra e as posições em x e y

        Keyword Arguments:
        img -- imagens 
        quem_ta_seguindo -- o que está sendo seguido (barra amarela segue o jogador, barra vermelha segue o fantasma ou numeros)
        largura -- largurra da barra de vida
        posx -- posiciona objetos no eixo x
        posy -- posiciona objetos no eixo y

        """ 

        pygame.sprite.Sprite.__init__(self)

        self.image = img
        self.image2 = img
        self.rect = self.image.get_rect()
        self.rect.centerx = posx
        self.rect.centery = posy
        self.ini_Pos=posy
        self.largura=largura
        self.largura2=largura
        self.quem_ta_seguindo=quem_ta_seguindo
        self.mask = pygame.mask.from_surface(self.image)
        if quem_ta_seguindo!=0 and quem_ta_seguindo!=3 and self.quem_ta_seguindo!=2 and self.quem_ta_seguindo!=1:
            self.a=quem_ta_seguindo.vida

    def update(self):
        """ Atualiza as posições de cada objeto adicional """
        global variavel
        global variavel2
        if self.quem_ta_seguindo==player:
            self.rect.centerx = self.quem_ta_seguindo.rect.centerx
            self.rect.bottom = self.quem_ta_seguindo.rect.bottom-heroi_altura-2
            if self.quem_ta_seguindo.estado==ataque or self.quem_ta_seguindo.estado==defendendo :
                if self.largura!=0:
                    self.largura-=1
                    self.largura2=0
                    self.image=pygame.transform.scale(self.image, (self.largura, barra_altura))
            if self.quem_ta_seguindo.estado==indefeso:
                if self.largura2!=32:
                    self.largura2=32
                    self.largura=32
                    self.image=pygame.transform.scale(self.image2, (self.largura2, barra_altura))

        if self.quem_ta_seguindo!=player and self.quem_ta_seguindo!=0 and self.quem_ta_seguindo!=3 and self.quem_ta_seguindo!=2 and self.quem_ta_seguindo!=1 :
            self.rect.centerx = self.quem_ta_seguindo.rect.centerx
            self.rect.bottom = self.quem_ta_seguindo.rect.bottom-heroi_altura-2
            
            if self.quem_ta_seguindo.vida<self.a:
                self.a=self.quem_ta_seguindo.vida
                if self.largura>0:
                    self.largura-=8
                    self.image=pygame.transform.scale(self.image, (self.largura, barra_altura))
            
        if self.quem_ta_seguindo == 0:
            
            if self.rect.centery<self.ini_Pos-11 or self.rect.centery>self.ini_Pos+11 :
                variavel*=-1
            if variavel>0:
                self.rect.y += 1
            elif variavel<0:
                self.rect.y -= 1

        if self.quem_ta_seguindo == 3 or self.quem_ta_seguindo == 2 or self.quem_ta_seguindo ==1 :
            if self.rect.centery<self.ini_Pos-5 or self.rect.centery>self.ini_Pos+5 :
                variavel2*=-1
            if variavel2>0:
                self.rect.y += 1
            elif variavel2<0:
                self.rect.y -= 1
            colisaod=pygame.sprite.spritecollide(player,all_pistas,True,pygame.sprite.collide_mask)
            if len(colisaod)>0:
                colisaod.clear()
                estado_do_jogo.aba="dicas"
        
#----------------------------------------------------------------------#
# - Definindo a classe que mostra a vida do personagem:

class xicara(pygame.sprite.Sprite):
    """ Define a xícara para recarga de vida do jogador """
    def __init__(self,dicio,indica,x,y):
        """ Define os dados iniciais da xícara que deve ser mostrada
        
        Keyword Arguments:
        dicio -- dicionário com as animacoes 
        indica -- quantia de vida que deve ser mostrada ou se nao deve mostrar
        x -- posição da xícara no eixo x
        y -- posição da xícara no eixo y
        """

        pygame.sprite.Sprite.__init__(self)
        
        self.animations = {
            xicara: dicio['xicara'][0:11],
            mesa: dicio['mesa'][0:8],
            }
        self.indica=indica
        if self.indica=="vida":
        
            self.animation = self.animations[xicara]
        else:
            self.animation = self.animations[mesa]

        self.oquemostrar=player.vida
        self.frame=0
        self.image = self.animation[self.frame]
        self.frame_ticks = 200
        self.last_update = pygame.time.get_ticks()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.centerx=x
        self.rect.centery=y

    def update(self):
        """ Atualiza o que deve ser mostrado como vida do jogador """
        if self.indica=="vida":
            self.oquemostrar=player.vida
            if player.vida%10==0:
                self.frame =int(10-(self.oquemostrar/10))
                self.image = self.animation[self.frame]
            else:
                self.frame =int(10-((self.oquemostrar-5)/10))
                self.image = self.animation[self.frame]

        else:
            now = pygame.time.get_ticks()
            elapsed2_ticks = now - self.last_update

            if elapsed2_ticks > self.frame_ticks:
                self.last_update = now
                self.frame += 1
                self.animation = self.animations[mesa]

                if self.frame >= len(self.animation):
                    self.frame = 0
    
                center = self.rect.center
                self.image = self.animation[self.frame]
                self.mask = pygame.mask.from_surface(self.image)
                self.rect = self.image.get_rect()
                self.rect.center = center
            colisaoh=pygame.sprite.spritecollide(player,all_cura,True, pygame.sprite.collide_mask)
            if len(colisaoh)>0:
                player.hora_da_acao = agora
                player.estado=helando
                if player.vida<=80:
                    player.vida+=20
                colisaoh.clear()
                tomandocafe.play()


#----------------------------------------------------------------------------------#
#- Definindo fases do jogo:

# PRÉ-FASES:
def fases(fase):
    """ Posiciona os blocos nas fases """
    #FASE 1:
    if fase==1:
        
        for row in range(len(MAP1)):
            for column in range(len(MAP1[row])):
                tile_type = MAP1[row][column]
                if tile_type == BLOCK:
                    tile = Tile(assets[Chao], row, column)
                    all_sprites.add(tile)
                    blocks.add(tile)
                if tile_type == EMPTY:
                    tile2 = Tile(assets[PAREDE], row, column)
                    all_sprites.add(tile2)
                if tile_type==PLATA:
                    tile3 = Tile(assets[PLATAa], row, column)
                    all_sprites.add(tile3)
                    all_plata.add(tile3)
                if tile_type==PLATE:
                    tile4 = Tile(assets[PLATEe], row, column)
                    all_sprites.add(tile4)
                    all_plata.add(tile4)
                if tile_type==PLATM:
                    tile5 = Tile(assets[PLATMm], row, column)
                    all_sprites.add(tile5)
                    all_plata.add(tile5)
                if tile_type==PLATD:
                    tile6 = Tile(assets[PLATDd], row, column)
                    all_sprites.add(tile6)
                    all_plata.add(tile6)

        # PISTA + CHAVE DA FASE:
        chave1=adicionais(assets[Chave1],0,0,largura-100,100)
        all_sprites.add(chave1)
        all_chaves.add(chave1)
        carta = adicionais(assets[CARTA],3,0,100,300)
        all_sprites.add(carta)
        all_pistas.add(carta)    
        
        
    #FASE 2:                
    if fase ==2:
        cura=xicara(dicio,"+vida",36,364)
        for row in range(len(MAP2)):
            for column in range(len(MAP2[row])):
                tile_type = MAP2[row][column]
                if tile_type == BLOCK:
                    tile = Tile(assets[Chao], row, column)
                    all_sprites.add(tile)
                    blocks.add(tile)
                if tile_type == EMPTY:
                    tile2 = Tile(assets[PAREDE], row, column)
                    all_sprites.add(tile2)
                if tile_type==PLATA:
                    tile3 = Tile(assets[PLATAa], row, column)
                    all_sprites.add(tile3)
                    all_plata.add(tile3)
                if tile_type==PLATE:
                    tile4 = Tile(assets[PLATEe], row, column)
                    all_sprites.add(tile4)
                    all_plata.add(tile4)
                if tile_type==PLATM:
                    tile5 = Tile(assets[PLATMm], row, column)
                    all_sprites.add(tile5)
                    all_plata.add(tile5)
                if tile_type==PLATD:
                    tile6 = Tile(assets[PLATDd], row, column)
                    all_sprites.add(tile6)
                    all_plata.add(tile6)
        all_sprites.add(player)
        all_sprites.add(barra)
        all_sprites.add(mostrador_vida)
        all_cura.add(cura)
        all_sprites.add(cura)
        # PISTA + CHAVE DA FASE:
        chave2=adicionais(assets[Chave2],0,0,largura-100,100)
        all_sprites.add(chave2)
        all_chaves.add(chave2)
        pegadas = adicionais(assets[PEGADAS],2,0,largura-100,490)
        all_sprites.add(pegadas)
        all_pistas.add(pegadas)

    #FASE 3:
    if fase ==3:
        for row in range(len(MAP3)):
           for column in range(len(MAP3[row])):
               tile_type = MAP3[row][column]
               if tile_type == BLOCK:
                   tile = Tile(assets[Chao], row, column)
                   all_sprites.add(tile)
                   blocks.add(tile)
               if tile_type == EMPTY:
                   tile2 = Tile(assets[PAREDE], row, column)
                   all_sprites.add(tile2)
               if tile_type==PLATA:
                    tile3 = Tile(assets[PLATAa], row, column)
                    all_sprites.add(tile3)
                    all_plata.add(tile3)
               if tile_type==PLATE:
                    tile4 = Tile(assets[PLATEe], row, column)
                    all_sprites.add(tile4)
                    all_plata.add(tile4)
               if tile_type==PLATM:
                    tile5 = Tile(assets[PLATMm], row, column)
                    all_sprites.add(tile5)
                    all_plata.add(tile5)
               if tile_type==PLATD:
                    tile6 = Tile(assets[PLATDd], row, column)
                    all_sprites.add(tile6)
                    all_plata.add(tile6)
        all_sprites.add(player)
        all_sprites.add(barra)
        all_sprites.add(mostrador_vida)

        # PISTA + CHAVE DA FASE:
        chave3=adicionais(assets[Chave3],0,0,largura-100,100)
        all_sprites.add(chave3)
        all_chaves.add(chave3)
        anel = adicionais(assets[ANEL],1,0,largura-200,500)
        all_sprites.add(anel)
        all_pistas.add(anel)
        
#----------------------------------------------------------------------#
# ----- Inicia estruturas de dados:
variavel2=1
variavel=1
sequencia=1
clock = pygame.time.Clock()
vida=100
vida_inimigo=40
FPS = 60
all_sprites = pygame.sprite.Group()
all_pistas = pygame.sprite.Group()
all_enemis = pygame.sprite.Group()
all_plata=pygame.sprite.Group()
blocks = pygame.sprite.Group()
all_chaves = pygame.sprite.Group()
all_cura=pygame.sprite.Group()
fase=1
fases(fase)
keys_down = {}
player= heroi(vida,dicio,blocks,all_chaves,all_plata)
cura1=xicara(dicio,"+vida",largura-100,459)
mostrador_vida=xicara(dicio,"vida",36,24)
estado_do_jogo= modo_de_jogo()
for i in range(2):
    inimigo = inimigos(player,dicio,vida_inimigo)
    all_sprites.add(inimigo)
    all_enemis.add(inimigo)
barra= adicionais(assets[BARRA_IMG],player,barra_largura,0,0)
all_sprites.add(mostrador_vida)

all_sprites.add(player)
all_sprites.add(barra)
all_cura.add(cura1)
all_sprites.add(cura1)    

mouse_pres=[]
game=True


agora=pygame.time.get_ticks()

#----------------------------------------------------------------------#
# ===== Loop principal =====

pygame.mixer.music.play(loops=-1)
while game:
    
    
    clock.tick(FPS)
    estado_do_jogo.controlador_menu()
    agora=pygame.time.get_ticks() 
 