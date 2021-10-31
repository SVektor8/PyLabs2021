import math
from random import choice
import pygame
from Colors import game_colors, black, grey, white, red
from random import randint


class Ball:
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(game_colors())
        self.live = 30

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        # FIXME
        self.x += self.vx
        self.y -= self.vy

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hit_test(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        # FIXME
        return False


class Gun:
    def __init__(self, screen, game):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = grey()
        self.x = 20
        self.y = 450
        self.game = game

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        self.game.bullet += 1
        new_ball = Ball(self.screen)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1] - new_ball.y), (event.pos[0] - new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        self.game.balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan((event.pos[1] - 450) / (event.pos[0] - 20))
        if self.f2_on:
            self.color = red()
        else:
            self.color = grey()

    def draw(self):
        # FIXIT don't know how to do it
        pygame.draw.circle(self.screen, black(), (self.x, self.y), self.f2_power)

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = red()
        else:
            self.color = grey()


class Target:
    def __init__(self, screen):
        self.points = 0
        self.live = 1
        self.screen = screen

        self.new_target()

    def new_target(self):
        """ Инициализация новой цели. """
        self.x = randint(600, 780)
        self.y = randint(300, 550)
        self.r = randint(2, 50)
        self.color = red()

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

    def draw(self):
        pygame.draw.circle(self.screen, red(), (self.x, self.y), self.r)


class Game_Master:
    def __init__(self, screen):
        self.screen = screen
        self.bullet = 0
        self.balls = []
        self.gun = Gun(screen, self)
        self.target = Target(screen)
        self.finished = False

    def update(self):
        self.screen.fill(white())

        self.gun.draw()
        self.target.draw()
        for b in self.balls:
            b.draw()

        pygame.display.update()

        for b in self.balls:
            b.move()
            if b.hit_test(self.target) and self.target.live:
                self.target.live = 0
                self.target.hit()
                self.target.new_target()
        self.gun.power_up()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.finished = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.gun.fire2_start(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.gun.fire2_end(event)
            elif event.type == pygame.MOUSEMOTION:
                self.gun.targetting(event)