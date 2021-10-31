import math
from random import choice
import pygame
from Colors import game_colors, black, grey, white, red
from random import randint
from GraphComs import turn, distance


class Ball:
    def __init__(self, screen, radius):
        """ Конструктор класса ball

                Args:
                x - начальное положение мяча по горизонтали
                y - начальное положение мяча по вертикали
                """
        self.screen = screen
        self.r = radius
        self.color = 0x000000

        self.x = 0
        self.y = 0
        self.speed_x = 0
        self.speed_y = 0
        self.acceleration_x = 0
        self.acceleration_y = 0

    def move(self):
        """Переместить мяч по прошествии единицы времени.

                Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
                self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
                и стен по краям окна (размер окна 800х600).
                """
        self.x += self.speed_x + self.acceleration_x / 2
        self.y += self.speed_y + self.acceleration_y / 2

        self.speed_x += self.acceleration_x
        self.speed_y += self.acceleration_y

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)

    def pos(self):
        return (self.x, self.y)

    def hit_test(self, ball):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

                Args:
                    obj: Обьект, с которым проверяется столкновение.
                Returns:
                    Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
                """
        if distance(self.pos(), ball.pos()) <= self.r + ball.r:
            return True
        else:
            return False


class Shell(Ball):
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        super().__init__(screen, 10)
        self.x = x
        self.y = y

        self.color = choice(game_colors())
        self.live = 30

        self.acceleration_y = 1


class Target(Ball):
    def __init__(self, screen):
        super().__init__(screen, 26)

        self.points = 0
        self.live = 1
        self.color = red()

        self.new_target()

    def new_target(self):
        """ Инициализация новой цели. """
        self.x = randint(600, 780)
        self.y = randint(300, 550)
        self.r = randint(2, 50)

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points


class Gun:
    def __init__(self, screen, game):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
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
        new_ball = Shell(self.screen)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1] - new_ball.y), (event.pos[0] - new_ball.x))
        new_ball.speed_x = self.f2_power * math.cos(self.an)
        new_ball.speed_y = self.f2_power * math.sin(self.an)
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
        coordinates = [turn(coo, self.an) for coo in [(-10, -3),
                                                      (self.f2_power, -3),
                                                      (self.f2_power, 3),
                                                      (-10, 3)]]
        coordinates = [(i[0] + 20, i[1] + 450) for i in coordinates]
        pygame.draw.polygon(self.screen,
                            (self.f2_power * 3 - 10, self.f2_power, self.f2_power),
                            coordinates)

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 85:
                self.f2_power += 1
            self.color = red()
        else:
            self.color = grey()


class GameMaster:
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
