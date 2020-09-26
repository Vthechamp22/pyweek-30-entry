# Importing everything
import pygame
from pygame import font
from pygame import sprite
from pygame import image
from pygame import display
from pygame import transform
from pygame import K_RETURN, KEYDOWN
from pygame import mouse
from pygame import mixer
from pygame.constants import MOUSEBUTTONDOWN
from pygame.time import Clock
import pygame.gfxdraw
from pygame_textinput import TextInput
from fuzzywuzzy import fuzz
from os.path import join
import time

# initialising pygame
pygame.init()
pygame.mixer.init()
font.init()


# Setting constants
SIZE = WIDTH, HEIGHT = 1100, 900
screen = display.set_mode(SIZE)

# COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (132, 220, 207)
YELLOW = (255, 255, 0)
GRAY = (130, 130, 130)

# Defining the fonts
default_font = font.Font(join(
    "assets", "fonts", "Noto_Sans_JP", "NotoSansJp-Medium.otf"), 20)
big_font = font.Font(join(
    "assets", "fonts", "Noto_Sans_JP", "NotoSansJp-Medium.otf"), 50)
question_font = font.Font(join("assets", "fonts", "Noto_Sans_JP", "NotoSansJp-Medium.otf"),
                          20)
timer_font = font.Font(join(
    "assets", "fonts", "Roboto", "Roboto-Medium.ttf"), 40)
story_font = font.Font(join("assets", "fonts", "Special_Elite",
                            "SpecialElite-Regular.ttf"),
                       19)


# Sounds
door_open = pygame.mixer.Sound(join('assets', 'door_open.ogg'))
door_close = pygame.mixer.Sound(join('assets', 'door_close.ogg'))
wrong_sound = pygame.mixer.Sound(join('assets', 'wrong.ogg'))
you_win = pygame.mixer.Sound(join('assets', 'you_win.ogg'))
you_lose = pygame.mixer.Sound(join('assets', 'you_lose.ogg'))
time_up = pygame.mixer.Sound(join('assets', 'time_over.ogg'))


class Player:
    '''Represents the stranded player'''

    def __init__(self) -> None:
        '''Create a new Player instance
        Args: None
        Returns: None
        '''
        self.acquired = []  # all the computer parts acquired
        # parts * qs * time_for each q * centiseconds
        self.time = 10 * 3 * 30 * 100
        self.started = False  # has the game started?
        self.pause_time = False  # should the time be paused
        self.lost = False  # did the player loose?

    def pass_door(self, name: str, q: str) -> None:  # a door(question) has been passed
        ''' A question (door) has been answered correctly
        Args:
            name - the name of the part
            q - the question answered
        Returns:
            None '''
        for item in self.acquired:
            if item["name"] == name:  # add one to the count of the part
                item["count"] += 1
                item["question"].append(q)  # add the question answered
            if item["count"] == 3:  # if three quesitons have been answered,
                item["acquired"] = True  # the part is acquired

    def new_item(self, name: str) -> None:
        '''Add a new computer part to the acquired list of the player
        Args:
            name - the name of the part'''
        if name not in [a['name'] for a in self.acquired]:  # add a new
            self.acquired.append({"name": name, "count": 0,  # computer part
                                  "acquired": False,  # to the acquired
                                  "question": []})  # list


class Button(sprite.Sprite):
    '''A button that the user can click'''

    def __init__(self, h: int = 20, x: int = 0, y: int = 0,
                 color=(255, 255, 255), text="Button",
                 font_renderer: font.Font = default_font,
                 a=True, text_color=(0, 0, 0), hover_color=(100, 100, 100),
                 function_to_call=lambda: print("BUTTON CLICKED!"),
                 args=(), kwargs={}, padding=10):
        '''Create a new Button instance
        Args:
            h - height of the button (px)
            x - the x position of the button
            y - the y position of the button
            color - the background color of the button
            font-renderer - a Fon'''
        super().__init__()
        self.text_content = text
        self.font_renderer = font_renderer
        self.a = a
        self.padding = padding
        self.h = h
        self.text_color = text_color
        self.text = font_renderer.render(text, a, text_color)
        self.text_rect = self.text.get_rect()
        self.image = pygame.Surface((self.text.get_width() + padding, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.x = x
        self.rect.y = y
        self.y = y
        self.image.fill(color)
        self.color = color
        self.hover_color = hover_color
        self.text_rect.center = self.rect.center
        self.f = function_to_call
        self.args = args
        self.kwargs = kwargs

    def change_text(self, text):
        self.text_content = text
        self.text = self.font_renderer.render(text, self.a, self.text_color)
        self.text_rect = self.text.get_rect()
        self.image = pygame.Surface((self.text.get_width() + self.padding,
                                     self.h))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.image.fill(self.color)
        self.text_rect.center = self.rect.center

    def clicked(self):
        return self.rect.collidepoint(pygame.mouse.get_pos()) and \
            pygame.mouse.get_pressed()[0]

    def update(self) -> None:
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                self.f(*self.args, **self.kwargs)
            else:
                self.image.fill(self.hover_color)
        else:
            self.image.fill(self.color)
        for a in player.acquired:
            if self.text_content == a['name'] and a['acquired']:
                self.kill()


class BlinkingDot(sprite.Sprite):
    def __init__(self, part, x=0, y=0,
                 color=(255, 0, 0)) -> None:
        super().__init__()
        self.x = x
        self.y = y
        self.part = part  # which computer part is it?
        self.r = 10
        self.color = list(color)
        self.add_color = True
        self.acquired = False
        self.image = image.load(join("assets", f"{part}.png"))
        self.image = transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def clicked(self):
        if pygame.mouse.get_pressed()[0]:
            mousex, mousey = pygame.mouse.get_pos()
            if mousex > self.x - self.r and mousex < self.x + self.r:
                if mousey > self.y - self.r and mousey < self.y + self.r:
                    return True
        return False

    def update(self) -> None:
        if self.acquired:
            screen.blit(self.image, self.rect)
        else:
            pygame.gfxdraw.filled_circle(screen, self.x, self.y,
                                         self.r, self.color)
            if self.add_color:
                self.color[1] += 8
                self.color[2] += 8
            else:
                self.color[1] -= 8
                self.color[2] -= 8

            if self.color[1] > 255 or self.color[2] > 255:
                self.add_color = False
                self.color[1] = 255
                self.color[2] = 255
            elif self.color[1] < 0 or self.color[2] < 0:
                self.add_color = True
                self.color[1] = 0
                self.color[2] = 0

        if self.clicked():
            return self.part

        if not self.acquired:
            for a in player.acquired:
                if a['name'] == self.part and a['acquired']:
                    self.acquired = True


class CommunicationDot(BlinkingDot):
    def __init__(self) -> None:
        self.x = 680
        self.y = 733
        self.color = [255, 255, 0]
        self.r = 10
        self.add_color = True

    def clicked(self):
        return super().clicked()

    def update(self):
        pygame.gfxdraw.filled_circle(screen, self.x, self.y,
                                     self.r, self.color)
        if self.add_color:
            self.color[2] += 8
        else:
            self.color[2] -= 8

        if self.color[2] > 255:
            self.add_color = False
            self.color[2] = 255
        elif self.color[2] < 0:
            self.color[2] = 0
            self.add_color = True

        return self.clicked()


class Door(sprite.Sprite):
    ''' The Door the player needs to open and answer questions '''

    def __init__(self, question, answer, x, y, part_name) -> None:
        super().__init__()
        self.question = question
        self.answer = answer.lower()
        self.door_done = image.load(join(
            "assets", "door done.png")).convert_alpha()
        self.door_done = transform.scale(self.door_done, (256, 256))
        self.image = image.load(join(
            "assets", "door.png")).convert_alpha()
        self.image = transform.scale(self.image, (256, 256))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.centery = y
        self.asking = False
        self.input = TextInput(text_color=WHITE)
        self.done = False
        self.part_name = part_name
        for a in player.acquired:
            if a['name'] == self.part_name:
                if self.question in a['question']:
                    self.done = True
                    self.image = self.door_done

    def update(self, events) -> None:
        screen.blit(self.image, self.rect)
        if not self.done:
            if self.rect.collidepoint(pygame.mouse.get_pos()) and \
                    pygame.mouse.get_pressed()[0] and not self.asking:
                self.asking = True
                door_open.play()
            else:
                if self.asking and not self.rect.collidepoint(
                    pygame.mouse.get_pos()) and \
                        pygame.mouse.get_pressed()[0]:
                    self.asking = False
                    door_close.play()
            if self.asking:
                self.input.update(events)
                inp = self.input.get_surface()
                inp_rect = inp.get_rect()
                inp_rect.centerx = WIDTH // 2
                inp_rect.y = self.rect.y - 40
                screen.blit(inp, inp_rect)
                q = question_font.render(self.question, True, BLACK)
                screen.blit(q,
                            (WIDTH // 2 - q.get_width() // 2, 50))
                for event in events:
                    if event.type == KEYDOWN:
                        if event.key == K_RETURN:
                            if fuzz.token_sort_ratio(self.answer,
                                                     self.input.get_text()
                                                     ) > 85:
                                self.asking = False
                                self.image = self.door_done
                                self.done = True
                                door_close.play()
                                player.pass_door(self.part_name, self.question)
                            else:
                                wrong_sound.play()


# setting up the game

clock = Clock()
FPS = 30

display.set_caption("The lost goat")  # the name of the game
# set the icon of the game
display.set_icon(image.load(join(
    'assets', 'router.png')).convert_alpha())


player = Player()
endpoint = CommunicationDot()

bg_map = image.load(join('assets', 'map.jpg')).convert_alpha()
bg_map = transform.scale(bg_map, (WIDTH, HEIGHT))
bg_map_rect = bg_map.get_rect()
bg_map_rect.center = (WIDTH // 2, HEIGHT // 2)


dot_group = sprite.Group()
btn_group = sprite.Group()

# don't worrry I didn't write it all manually lol
dot_positions = [("CPU", 410, 151), ("RAM", 183, 327),
                 ("Monitor", 911, 326), ("Keyboard and mouse", 660, 343),
                 ("Motherboard", 427, 344),
                 ("Cooling", 410, 536), ("GPU", 681, 135),
                 ("Phone Battery", 444, 736), ("Hard Drive", 141, 576),
                 ("OS", 674, 523), ("Wifi Card", 956, 765),
                 ("Scientific Calculator", 170, 174)]


dot_group.add(*[BlinkingDot(part, x, y) for part, x, y in dot_positions])


DECREASE_TIME = pygame.USEREVENT + 1
pygame.time.set_timer(DECREASE_TIME, 10)


def start_screen():
    motherboard = image.load(
        join("assets", "motherboard_start_screen.png"))
    crashed = image.load(
        join("assets", "crashed_start_screen.png"))
    story = image.load(
        join("assets", "the_story.png")
    )
    story_rect = story.get_rect()
    story_rect.x = WIDTH // 2

    motherboard = transform.scale(motherboard,
                                  (WIDTH // 2, HEIGHT // 2))

    crashed = transform.scale(crashed,
                              (WIDTH // 2, HEIGHT // 2))

    motherboard_filter = pygame.Surface(motherboard.get_rect().size)
    motherboard_filter.fill(RED)
    motherboard_filter.set_alpha(255 / 4)
    motherboard_filter_rect = motherboard_filter.get_rect()
    motherboard_filter_rect.x = 0
    motherboard_filter_rect.y = 0

    crashed_filter = pygame.Surface(crashed.get_rect().size)
    crashed_filter.set_alpha(255 / 4)
    crashed_filter.fill(BLUE)
    crashed_filter_rect = crashed_filter.get_rect()
    crashed_filter_rect.x = 0
    crashed_filter_rect.y = HEIGHT // 2

    running = True

    start_btn = Button(100, 570, 750, function_to_call=main, text="Start",
                       font_renderer=big_font, color=(23, 190, 187),
                       hover_color=(255, 201, 20),
                       text_color=(1, 22, 56), padding=100)
    exit_btn = Button(100, 900, 750, function_to_call=exit, text="Exit",
                      font_renderer=big_font, color=(23, 190, 187),
                      hover_color=(255, 201, 20),
                      text_color=(1, 22, 56), padding=100)

    btn_group = [start_btn, exit_btn]

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F4 and event.mod == pygame.KMOD_LALT:
                    running = False
                elif event.key == pygame.K_ESCAPE:
                    running = False

        screen.fill(WHITE)

        screen.blit(crashed, (0, 0))
        screen.blit(motherboard, (0, HEIGHT // 2))
        screen.blit(story, story_rect)
        screen.blit(motherboard_filter, motherboard_filter_rect)
        screen.blit(crashed_filter, crashed_filter_rect)

        for btn in btn_group:
            btn.update()

        if player.started and start_btn.text_content != "Resume":
            start_btn.change_text("Resume")

        for filter in [motherboard_filter, crashed_filter]:
            if filter.get_rect().collidepoint(pygame.mouse.get_pos()):
                filter.set_alpha(255 / 4)
                # print(filter)
            else:
                filter.set_alpha(0)

        pygame.display.update()


def lost_screen():
    img = image.load(
        join('assets', 'youloose.png')
    )
    img = transform.scale(img, (WIDTH, HEIGHT))
    img_rect = img.get_rect()

    texts = []

    for i, text in enumerate(["The tsunami has struck the island,",
                              " your efforts of saving him fell short."]):
        rendered = big_font.render(text,
                                   True, YELLOW)
        rect = rendered.get_rect()
        rect.centerx = WIDTH // 2
        rect.y = (rect.h * i) + 100
        texts.append((rendered, rect))

    mixer.music.load(join("assets", "waves.mp3"))
    mixer.music.play(-1)

    time_up.play()
    time.sleep(time_up.get_length())
    you_lose.play()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F4 and event.mod == pygame.KMOD_LALT:
                    exit()
                elif event.key == pygame.K_ESCAPE:
                    exit()

        screen.blit(img, img_rect)
        for i, (text, text_rect) in enumerate(texts):
            screen.blit(text, text_rect)

        pygame.display.update()


def win_screen():
    img = image.load(
        join('assets', 'youwin.png')
    )
    img = transform.scale(img, (WIDTH, HEIGHT))
    img_rect = img.get_rect()

    mixer.music.load(join("assets", "helicopter.wav"))

    mixer.music.play(-1)

    texts = []

    for i, text in enumerate(["YAY... you have succeeded in saving Mr. Goat!",
                              "He is being rescued by a helicopter"]):
        rendered = big_font.render(text,
                                   True, GREEN)
        rect = rendered.get_rect()
        rect.centerx = WIDTH // 2
        rect.y = (rect.h * i) + 750
        texts.append((rendered, rect))

    you_win.play()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F4 and event.mod == pygame.KMOD_LALT:
                    exit()
                elif event.key == pygame.K_ESCAPE:
                    exit()

        screen.blit(img, img_rect)
        for i, (text, text_rect) in enumerate(texts):
            screen.blit(text, text_rect)

        pygame.display.update()


def decrease_time():
    if not player.pause_time and player.time > 0:
        player.time -= 1
    elif player.time <= 0:
        player.lost = True


def draw_timer():
    minutes = player.time // 6000
    seconds_and_ms = player.time % 6000
    seconds = seconds_and_ms // 100
    ms = seconds_and_ms % 100
    ms = "0" + str(ms) if len(str(ms)) == 1 else ms
    seconds = "0" + str(seconds) if len(str(seconds)) == 1 else seconds
    minutes = "0" + str(minutes) if len(str(minutes)) == 1 else minutes

    time_left = timer_font.render(f"{minutes}:{seconds}.{ms}",
                                  True, RED)
    time_left_rect = time_left.get_rect()
    time_left_rect.x = 100
    time_left_rect.y = HEIGHT - 50

    background = pygame.Surface((time_left_rect.w + 20,
                                 time_left_rect.h + 20))
    background.fill(BLACK)
    background_rect = background.get_rect()
    background_rect.center = time_left_rect.center

    screen.blit(background, background_rect)
    screen.blit(time_left, time_left_rect)


def draw_status_bar():
    full_status_bar = pygame.Surface((WIDTH - 50, 40))
    full_status_bar.fill(BLACK)
    full_status_bar_rect = full_status_bar.get_rect()
    full_status_bar_rect.centerx = WIDTH // 2
    full_status_bar_rect.y = 10

    num_acquired = len([a['name'] for a in player.acquired if a['acquired']])
    percentage = num_acquired / len(dot_positions)

    aqcuired_status_bar = pygame.Surface(
        ((full_status_bar_rect.w // len(dot_positions)) * num_acquired, 30))
    aqcuired_status_bar.fill(YELLOW)
    aqcuired_status_bar_rect = aqcuired_status_bar.get_rect()
    aqcuired_status_bar_rect.centery = full_status_bar_rect.centery
    aqcuired_status_bar_rect.x = full_status_bar_rect.x

    screen.blit(full_status_bar, full_status_bar_rect)
    screen.blit(aqcuired_status_bar, aqcuired_status_bar_rect)

    percentage_text = default_font.render(f"{percentage * 100:.0f} \
% components acquired",
                                          True, RED)
    percentage_text_rect = percentage_text.get_rect()
    percentage_text_rect.center = full_status_bar_rect.center

    screen.blit(percentage_text, percentage_text_rect)


def main():
    player.started = True
    player.pause_time = False
    won = False
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F4 and event.mod == pygame.KMOD_LALT:
                    running = False
                elif event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == DECREASE_TIME:
                decrease_time()

        screen.blit(bg_map, bg_map_rect)

        for dot in dot_group:
            rslt = dot.update()
            if rslt:
                part_name = rslt
                btn_group.empty()
                to_add = Button(text=part_name, x=dot.x, y=dot.y - 70, h=50,
                                hover_color=(200, 200, 200),
                                function_to_call=ask_q,
                                args=(part_name,))
                btn_group.add(to_add)

        if endpoint.update():
            required = ["CPU", "RAM", "Monitor", "Keyboard and mouse",
                        "Motherboard", "Hard Drive", "OS"]
            acquired = [a['name'] for a in player.acquired]
            # acquired = ["CPU", "RAM", "Monitor", "Keyboard and mouse",
            #             "Motherboard", "Hard Drive", "OS"]
            for r in required:
                if r not in acquired:
                    print("You do not have all the necessary components")
                    break
            else:
                won = True
                break

        draw_timer()
        draw_status_bar()

        if player.lost:
            print("YOU LOOOOOSE!")
            break

        btn_group.update()

        pygame.display.update()
        clock.tick(FPS)

    player.pause_time = True
    if player.lost:
        lost_screen()
    elif won:
        win_screen()


def fade(next_func, *args, **kwargs):
    rect = pygame.Surface(SIZE)
    rect.fill(WHITE)

    for alpha in range(299, -1, -1):
        rect.set_alpha(alpha)
        screen.blit(rect, (0, 0))
        pygame.display.update()
        clock.tick(FPS)

    for alpha in range(0, 300):  # fade out
        rect.set_alpha(alpha)
        screen.blit(rect, (0, 0))
        pygame.display.update()
        clock.tick(FPS)

    next_func(*args, **kwargs)


def ask_q(part: str):
    running = True

    with open(f"questions/{part}", "r") as f:
        questions = f.readlines()

    questions = [{"q": q.split(";")[0],
                  "a": q.split(";")[1]} for q in questions]
    door_group = sprite.Group()

    to_multiply = WIDTH // len(questions)

    door_group.add([Door(q["q"], q["a"], i * to_multiply, HEIGHT//2,
                         part) for i, q in enumerate(questions)])

    player.new_item(part)

    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F4 and event.mod == pygame.KMOD_LALT:
                    running = False
                elif event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == DECREASE_TIME:
                decrease_time()

        screen.fill(GRAY)
        for door in door_group:
            door.update(events)

        draw_timer()

        pygame.display.update()


start_screen()

# de-initialise everything
pygame.quit()
pygame.mixer.quit()
font.quit()
