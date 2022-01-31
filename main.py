import pygame
import random

# Mudar Tamanho
LINES = 10
ROWS = 7
SIZE = 80

width = ROWS * SIZE
height = LINES * SIZE

screen = pygame.display.set_mode((width, height))

clock = pygame.time.Clock()

COLORS = ['red', 'green', 'yellow', 'blue']


class Map:
    def __init__(self):
        self.rects = []
        # adicionar retas à lista
        for i in range(LINES):
            for j in range(ROWS):
                rect = pygame.Rect(j * SIZE, i * SIZE, SIZE, SIZE)
                self.rects.append(rect)


class Circle:
    def __init__(self):
        # Colocar circulo em sitio random
        self.rect = pygame.Rect(random.randint(0, ROWS - 1) * SIZE, 0, SIZE, SIZE)
        # Cor Random
        self.color = random.choice(COLORS)

        self.is_pressed = False
        self.map_pos = 0  # map list index

        # Usado para contar os frames
        self.counter = 0
        self.timer = 50

        self.is_active = True
        self.can_turn_left = True
        self.can_turn_right = True

    # desenhar o circulo no meio da reta
    def draw(self, window):
        pygame.draw.circle(window, self.color, (self.rect.centerx, self.rect.centery), SIZE / 2, 4)

    def update(self):
        keys = pygame.key.get_pressed()
        # Mover para direita
        if keys[pygame.K_RIGHT] and not self.is_pressed and \
                self.rect.right < width and self.is_active and self.can_turn_right:
            self.rect.x += SIZE
            self.is_pressed = True

        # Mover para esquerda
        if keys[pygame.K_LEFT] and not self.is_pressed and self.rect.left > 0 and self.is_active and self.can_turn_left:
            self.rect.x -= SIZE
            self.is_pressed = True

        # Mover circulo a cada 50 frames
        self.counter += 1
        if self.counter >= self.timer and self.rect.bottom < height and self.is_active and not self.is_pressed:
            self.rect.y += SIZE
            self.counter = 0

        # Mover circulo a cada 5 frames
        if keys[pygame.K_SPACE]:
            self.timer = 5
        else:
            self.timer = 50

        if not keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            self.is_pressed = False


# Botões do Main Menu
class Button:
    def __init__(self, x, y, text):
        self.x = x
        self.y = y
        self.text = text
        self.color = 'yellow'
        self.color_copy = self.color
        self.is_selected = False

    def draw(self):
        write(25, self.x, self.y, self.text, self.color)

    # Mudar de Cor
    def update(self):
        if self.is_selected:
            self.color = 'red'
        else:
            self.color = self.color_copy

    def is_pressed(self):
        keys = pygame.key.get_pressed()
        if self.is_selected and keys[pygame.K_RETURN]:
            return True
        else:
            return False


# Escrever texto
def write(size, x, y, text, color):
    surf_font = pygame.font.Font('font.ttf', size)
    font_surf = surf_font.render(text, True, color)
    font_rect = font_surf.get_rect(center=(x, y))
    screen.blit(font_surf, font_rect)


pygame.font.init()


# Main Menu
def main():
    run = True
    rect_map = Map()
    circles = [Circle()]

    # Função que retorna a lista dos circulos da mesma cor
    def connected(circle, all_circles):
        count = 0
        color_circles = []  # Lista dos circulos da mesma cor
        connected_3 = [circle]
        for c in all_circles:
            if c.color == circle.color:
                color_circles.append(c)

        for c in color_circles:
            # verificar circulo à esquerda
            if circle.map_pos - 1 == c.map_pos and not c.is_active:
                count += 1
                connected_3.append(c)
            # verificar circulo à direita
            if circle.map_pos + 1 == c.map_pos and not c.is_active:
                count += 1
                connected_3.append(c)
            # verificar circulo em cima
            if circle.map_pos - 7 == c.map_pos and not c.is_active:
                count += 1
                connected_3.append(c)
            # verificar circulo em baixo
            if circle.map_pos + 7 == c.map_pos and not c.is_active:
                count += 1
                connected_3.append(c)

        return connected_3

    def redraw_window():
        screen.fill((30, 30, 30))
        # Grid
        # rect_map.draw(screen)

        for rect in rect_map.rects:
           
            for circle in circles:
                if rect.colliderect(circle.rect):
                    circle.map_pos = rect_map.rects.index(rect)  # Atribuir posição ao circulo

        for circle in circles:
            # Mostrar circulo
            circle.draw(screen)
            circle.update()

            for other_circles in circles:
                # Parar circulo se estiver em baixo outro
                if circle.map_pos + 7 == other_circles.map_pos and circle.is_active:
                    circle.is_active = False
                    circles.append(Circle())

                # BodyBlock
                if circle.map_pos + 1 == other_circles.map_pos:
                    circle.can_turn_right = False

                if circle.map_pos - 1 == other_circles.map_pos:
                    circle.can_turn_left = False

            # Parar o circulo no fundo
            if circle.map_pos + 7 > 69 and circle.is_active:
                circle.is_active = False
                circles.append(Circle())

            # Se estiverem 3 circulos desaparece
            if len(connected(circle, circles)) > 2:
                for c in connected(circle, circles):
                    circles.remove(c)

        pygame.display.update()

    # Main loop
    while run:
        redraw_window()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Condição para perder
        for el in circles:
            if el.map_pos < 7 and not el.is_active:
                run = False
                game_over()

        clock.tick(60)


# Tela do Main Menu
def main_menu():
    run = True

    # Botões
    start_button = Button(width / 2, height / 2, 'start game')
    start_button.is_selected = True

    exit_button = Button(width / 2, height / 2 + 40, 'exit')

    def redraw_window():
        screen.fill((30, 30, 30))

        # Mostrar texto e botões
        write(70, width / 2, height / 4, 'Colortis', (255, 255, 255))
        start_button.draw()
        start_button.update()

        exit_button.draw()
        exit_button.update()

        pygame.display.update()

    while run:
        redraw_window()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                # Mudar Botões do Main Menu
                if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                    if start_button.is_selected:
                        start_button.is_selected = False
                        exit_button.is_selected = True
                    else:
                        start_button.is_selected = True
                        exit_button.is_selected = False

        # Botão Main Menu
        if exit_button.is_pressed():
            run = False

        if start_button.is_pressed():
            run = False
            main()

        clock.tick(60)


# Tela de Fim de Jogo
def game_over():
    run = True

    def redraw_window():
        screen.fill((30, 30, 30))

        # Texto
        write(60, width / 2, height / 2, 'Game Over', (255, 255, 255))
        write(30, width / 2, height / 2 + 70, 'Press space to continue', (255, 255, 255))

        pygame.display.update()

    while run:
        redraw_window()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # Main Menu
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    run = False
                    main_menu()

        clock.tick(60)


main_menu()
