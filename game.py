from random import randint
import pygame, sys
from pygame import display
from pygame.image import load
from pygame.sprite import Sprite, Group, GroupSingle, groupcollide
from pygame import event
from pygame.locals import QUIT, KEYUP, K_SPACE
from pygame.time import Clock
from pygame import font

pygame.init()


# Som inicio
pygame.mixer.music.set_volume(0.1)
musica_de_fundo = pygame.mixer.music.load('musica_menu.wav')
pygame.mixer.music.play(-1)

acerto_vacina = pygame.mixer.Sound('musica_acerto.wav')
acerto_vacina.set_volume(0.8)
# Som fim

tamanho = 800, 600
fonte = font.SysFont('arial', 25)
fonte_perdeu = font.SysFont('arial', 66)
FPS = 120
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)
PRETO = (0, 0, 0)
timer = 0
tempo_segundo = 0


superficie = display.set_mode(
    size=tamanho
)
fundo = load('fundomenu.png')
display.set_caption(
    'Vacina VS Vírus'
)

#Contator de segundos
texto = fonte.render("Tempo: ", True, (BRANCO), (PRETO))
pos_texto = texto.get_rect()
pos_texto.center = (54, 80)

class ZeGotinha(Sprite):
    def __init__(self, vacina):
        super().__init__()

        self.image = load('zegotinha.png')
        self.rect = self.image.get_rect(
            center=(200, randint(60, 150))
        )
        self.vacina = vacina
        self.velocidade = 2

    def jogar_vacina(self):
        if len(self.vacina) < 10:
            self.vacina.add(
                Vacina(*self.rect.center)
            )

    def update(self):
        keys = pygame.key.get_pressed()

        vacina_fonte = fonte.render(
            f'Vacinas : {10 - len(self.vacina)}',
            True,
            (BRANCO), (PRETO)
        )
        superficie.blit(vacina_fonte, (10, 10))

        # Movimento nas teclas
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.velocidade
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.velocidade
        if keys[pygame.K_UP]:
            self.rect.y -= self.velocidade
        if keys[pygame.K_DOWN]:
            self.rect.y += self.velocidade

        # Sprite se mantém na tela
        if self.rect.right > 800:
            self.rect.right = 800
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > 600:
            self.rect.bottom = 600
        if self.rect.top < 0:
            self.rect.top = 0

class Vacina(Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = load('vacina.png')
        self.rect = self.image.get_rect(
            center=(x, y)
        )

    def update(self):
        self.rect.x += 1

        if self.rect.x > tamanho[0]:
            self.kill()

class Virus(Sprite):
    def __init__(self):
        super().__init__()

        self.image = load('virus.png')
        self.rect = self.image.get_rect(
            center=(800, randint(60, 580))
        )

    def update(self):
        self.rect.x -= 0.1

        if self.rect.x == 0:
            self.kill()
            global perdeu
            perdeu = True

grupo_inimigos = Group()
grupo_vacina = Group()
zegotinha = ZeGotinha(grupo_vacina)
grupo_zegotinha = GroupSingle(zegotinha)

grupo_inimigos.add(Virus())

clock = Clock()
mortes = 0
round = 0
perdeu = False

while True:
    clock.tick(FPS)

    if round % 120 == 0:
        if mortes < 20:
            grupo_inimigos.add(Virus())
        for _ in range(int(mortes / 20)):
            grupo_inimigos.add(Virus())
    print(mortes)
    # Eventos
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYUP:
            if event.key == K_SPACE:
                zegotinha.jogar_vacina()
    if groupcollide(grupo_vacina, grupo_inimigos, True, True):
        mortes += 1
        acerto_vacina.play()

    if groupcollide(grupo_zegotinha, grupo_inimigos, True, True):
        fim = fonte_perdeu.render(
            'Você perdeu!',
            True,
            (VERMELHO)
        )
        superficie.blit(fim, (210, 20))
        display.update()
        pygame.time.delay(4500)

    if timer < 140:
        timer += 1
    else:
        tempo_segundo += 1
        texto = fonte.render("Tempo : "+str(tempo_segundo), True, (BRANCO), (PRETO))
        timer = 0

    # Display
    superficie.blit(fundo, (0, 0))

    fonte_mortes = fonte.render(
        f'Acertos : {mortes}',
        True,
        (BRANCO), (PRETO)
    )

    superficie.blit(fonte_mortes, (10, 38))
    grupo_zegotinha.draw(superficie)
    grupo_inimigos.draw(superficie)
    grupo_vacina.draw(superficie)
    superficie.blit(texto, pos_texto)

    grupo_zegotinha.update()
    grupo_inimigos.update()
    grupo_vacina.update()

    if perdeu:
        fim = fonte_perdeu.render(
            'Você perdeu!',
            True,
            (VERMELHO)
        )
        superficie.blit(fim, (210, 20))
        display.update()
        pygame.time.delay(4500)

    round += 1
    display.update()

