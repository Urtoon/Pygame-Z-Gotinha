import pygame, sys
from button import Button
from random import randint
from pygame import display
from pygame.image import load
from pygame.sprite import Sprite, Group, GroupSingle, groupcollide
from pygame import event
from pygame.locals import QUIT, KEYUP, K_SPACE, K_LCTRL
from pygame.time import Clock
from pygame import font

pygame.init()

# Musica inicio
pygame.mixer.music.set_volume(0.2)
musica_de_fundo = pygame.mixer.music.load('musica_menu.wav')
pygame.mixer.music.play(-1)
# Musica fim

TELA = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Zé gotinha vs Vírus")

BG = pygame.image.load("fundomenu.png")

icon = pygame.image.load("zegotinha.png")
pygame.display.set_icon(icon)


def get_font(size):
    return pygame.font.Font("8-BIT WONDER.TTF", size)


def jogar():
    while True:
        JOGAR_MOUSE_POS = pygame.mouse.get_pos()

        TELA.fill("black")

        JOGAR_TEXT = get_font(45).render("Jogo", True, "Black")
        JOGAR_RECT = JOGAR_TEXT.get_rect(center=(640, 260))
        TELA.blit(JOGAR_TEXT, JOGAR_RECT)

        JOGAR_BACK = Button(image=None, pos=(640, 460),
                            text_input="VOLTAR", font=get_font(75), base_color="#368170", hovering_color="White")

        JOGAR_BACK.changeColor(JOGAR_MOUSE_POS)
        JOGAR_BACK.update(TELA)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if JOGAR_BACK.checkForInput(JOGAR_MOUSE_POS):
                    main_menu()

        pygame.display.update()

        # Acerto inicio
        acerto_vacina = pygame.mixer.Sound('musica_acerto.wav')
        acerto_vacina.set_volume(0.8)
        # Acerto fim

        tamanho = 1280, 720
        fonte = font.Font("8-BIT WONDER.TTF", 25)
        fonte_perdeu = font.Font("8-BIT WONDER.TTF", 55)
        FPS = 120
        BRANCO = (255, 255, 255)
        VERMELHO = (255, 0, 0)
        PRETO = (0, 0, 0)
        timer = 0
        tempo_segundo = 0

        superficie = display.set_mode(
            size=tamanho
        )
        fundo = load('fundojogo.png')
        display.set_caption(
            'Vacina VS Vírus'
        )

        # Contator de segundos
        texto = fonte.render("Tempo ", True, (BRANCO), (PRETO))
        pos_texto = texto.get_rect()
        pos_texto.center = (86, 82)

        class ZeGotinha(Sprite):
            def __init__(self, vacina):
                super().__init__()

                self.image = load('zegotinha.png')
                self.rect = self.image.get_rect(
                    center=(200, randint(60, 150))
                )
                self.vacina = vacina
                self.velocidade = 3

            def jogar_vacina(self):
                if len(self.vacina) < 10:
                    self.vacina.add(
                        Vacina(*self.rect.center)
                    )
                if mortes >= 20:
                    self.vacina.add(
                        Vacina(*self.rect.center)
                    )

            def update(self):
                keys = pygame.key.get_pressed()

                vacina_fonte = fonte.render(
                    f'Vacinas  {10 - len(self.vacina)}',
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
                if self.rect.right > 1280:
                    self.rect.right = 720
                if self.rect.left < 0:
                    self.rect.left = 0
                if self.rect.bottom > 720:
                    self.rect.bottom = 720
                if self.rect.top < 80:
                    self.rect.top = 80

        class Vacina(Sprite):
            def __init__(self, x, y):
                super().__init__()

                self.image = load('vacina.png')
                self.rect = self.image.get_rect(
                    center=(x, y)
                )

            def update(self):
                self.rect.x += 4

                if self.rect.x > tamanho[0]:
                    self.kill()

        class Virus(Sprite):
            def __init__(self):
                super().__init__()

                self.image = load('virus.png')
                self.rect = self.image.get_rect(
                    center=(1280, randint(85, 710))
                )

            def update(self):
                self.rect.x -= 0.1

                if self.rect.x == 0:
                    self.kill()
                    global perdeu
                    perdeu = True

        class Virus2(Sprite):
            def __init__(self):
                super().__init__()

                self.image = load('virus2.png')
                self.rect = self.image.get_rect(
                    center=(1280, randint(85, 710))
                )

            def update(self):
                self.rect.x -= 0.1

                if self.rect.x == 0:
                    self.kill()
                    global perdeu
                    perdeu = True

        class Virus3(Sprite):
            def __init__(self):
                super().__init__()

                self.image = load('megavirus.png')
                self.rect = self.image.get_rect(
                    center=(1280, randint(300, 300))
                )

            def update(self):
                self.rect.x -= 0

                if self.rect.x == 0:
                    self.kill()
                    global perdeu
                    perdeu = True

        grupo_inimigos = Group()
        grupo_vacina = Group()
        zegotinha = ZeGotinha(grupo_vacina)
        grupo_zegotinha = GroupSingle(zegotinha)

        grupo_inimigos.add(Virus(), Virus2(), Virus3())

        clock = Clock()
        mortes = 0
        round = 0
        perdeu = False

        while True:
            clock.tick(FPS)

            if round % 50 == 0:
                if mortes < 20:
                    grupo_inimigos.add(Virus())
                    if mortes > 20:
                        grupo_inimigos.add(Virus2())
                if mortes > 30:
                    grupo_inimigos.add(Virus3())
            print(mortes)

            # Eventos
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == KEYUP:
                    if event.key == K_SPACE:
                        zegotinha.jogar_vacina()

                if event.type == KEYUP:
                    if event.key == K_LCTRL:
                        zegotinha.image = load('zegotinhaup.png')
                        zegotinha.velocidade = 7

            if groupcollide(grupo_vacina, grupo_inimigos, True, True):
                mortes += 1
                acerto_vacina.play()

            if groupcollide(grupo_zegotinha, grupo_inimigos, True, True):
                fim = fonte_perdeu.render(
                    'GAME OVER',
                    True,
                    (VERMELHO)
                )
                superficie.blit(fim, (420, 330))
                display.update()
                pygame.time.delay(4500)

            if timer < 140:
                timer += 1
            else:
                tempo_segundo += 1
                texto = fonte.render("Tempo  " + str(tempo_segundo), True, (BRANCO), (PRETO))
                timer = 0

            # Display
            superficie.blit(fundo, (0, 0))

            fonte_mortes = fonte.render(
                f'Acertos  {mortes}',
                True,
                (BRANCO), (PRETO)
            )

            superficie.blit(fonte_mortes, (10, 40))
            grupo_zegotinha.draw(superficie)
            grupo_inimigos.draw(superficie)
            grupo_vacina.draw(superficie)
            superficie.blit(texto, pos_texto)

            grupo_zegotinha.update()
            grupo_inimigos.update()
            grupo_vacina.update()

            if perdeu:
                fim = fonte_perdeu.render(
                    'GAME OVER',
                    True,
                    (VERMELHO)
                )
                superficie.blit(fim, (210, 20))
                display.update()
                pygame.time.delay(4500)

            round += 1
            display.update()


def opçoes():
    while True:
        OPÇOES_MOUSE_POS = pygame.mouse.get_pos()

        TELA.fill("#b7c1e5")

        OPÇOES_TEXT = get_font(45).render("Ayrton da Silva", True, "#3c4c6c")
        OPÇOES_TEXT2 = get_font(45).render("Julia Gomes", True, "#3c4c6c")
        OPÇOES_TEXT3 = get_font(45).render("Matheus Vicente", True, "#3c4c6c")

        OPÇOES_RECT = OPÇOES_TEXT.get_rect(center=(640, 220))
        TELA.blit(OPÇOES_TEXT, OPÇOES_RECT)

        OPÇOES_RECT = OPÇOES_TEXT2.get_rect(center=(640, 290))
        TELA.blit(OPÇOES_TEXT2, OPÇOES_RECT)

        OPÇOES_RECT = OPÇOES_TEXT3.get_rect(center=(640, 360))
        TELA.blit(OPÇOES_TEXT3, OPÇOES_RECT)

        OPÇOES_BACK = Button(image=None, pos=(640, 460),
                             text_input="VOLTAR", font=get_font(75), base_color="#1a2656", hovering_color="Black")

        OPÇOES_BACK.changeColor(OPÇOES_MOUSE_POS)
        OPÇOES_BACK.update(TELA)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPÇOES_BACK.checkForInput(OPÇOES_MOUSE_POS):
                    main_menu()

        pygame.display.update()


def main_menu():
    while True:
        TELA.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(80).render("MENU PRINCIPAL", True, "#7088c0")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        JOGAR_BUTTON = Button(image=pygame.image.load("Jogar Rect.png"), pos=(640, 250),
                              text_input="JOGAR", font=get_font(55), base_color="#b7c1e5", hovering_color="White")
        OPÇOES_BUTTON = Button(image=pygame.image.load("Opçoes Rect.png"), pos=(640, 400),
                               text_input="CREDITOS", font=get_font(55), base_color="#b7c1e5", hovering_color="White")
        FECHAR_BUTTON = Button(image=pygame.image.load("Jogar Rect.png"), pos=(640, 550),
                               text_input="FECHAR", font=get_font(55), base_color="#b7c1e5", hovering_color="White")

        TELA.blit(MENU_TEXT, MENU_RECT)

        for button in [JOGAR_BUTTON, OPÇOES_BUTTON, FECHAR_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(TELA)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if JOGAR_BUTTON.checkForInput(MENU_MOUSE_POS):
                    jogar()
                if OPÇOES_BUTTON.checkForInput(MENU_MOUSE_POS):
                    opçoes()
                if FECHAR_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


main_menu()
