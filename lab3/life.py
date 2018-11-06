import random
from typing import List
import pygame


class GameOfLife:

    def __init__(self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_grid(self) -> None:
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(
                self.screen, pygame.Color(0, 0, 0),
                (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(
                self.screen, pygame.Color(0, 0, 0),
                (0, y), (self.width, y))

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color(255, 255, 255))

        # Создание списка клеток
        self.cell_list()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Отрисовка списка клеток
            self.draw_cell_list(self.clist)
            self.draw_grid()

            # Выполнение одного шага игры (обновление состояния ячеек)
            self.update_cell_list(self.clist)

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def cell_list(self, randomize: bool = True) -> List[list]:
        """ Создание списка клеток.

        :param randomize: Если True, то создается список клеток, где
        каждая клетка равновероятно может быть живой (1) или мертвой (0).
        :return: Список клеток, представленный в виде матрицы
        """
        self.clist = [[0] * self.cell_width for _ in range(self.cell_height)]
        if randomize:
            for i in range(self.cell_height):
                for k in range(self.cell_width):
                    self.clist[i][k] = random.randint(0, 1)
        return self.clist

    def draw_cell_list(self, clist: List[list]) -> None:
        """ Отображение списка клеток
        :param clist: Список клеток для отрисовки, представленный в виде матрицы
        """

        cell_height = len(clist)
        cell_width = len(clist[0])
        for i in range(cell_height):
            for k in range(cell_width):
                if clist[i][k] == 1:
                    pygame.draw.rect(self.screen, pygame.Color(0, 255, 0),
                                     pygame.Rect(k*self.cell_size, i*self.cell_size, self.cell_size, self.cell_size))
                else:
                    pygame.draw.rect(self.screen, pygame.Color(255, 255, 255),
                                     pygame.Rect(k*self.cell_size, i*self.cell_size, self.cell_size, self.cell_size))

    def get_neighbours(self, cell: tuple) -> list:
        """ Вернуть список соседей для указанной ячейки

        :param cell: Позиция ячейки в сетке, задается кортежем вида (row, col)
        :return: Одномерный список ячеек, смежных к ячейке cell
        """
        row, col = cell
        neighbours = [self.clist[i][k] for i in range(row - 1, row + 2)
                      for k in range(col - 1, col + 2)
                      if 0 <= i < self.cell_height and 0 <= k < self.cell_width]
        neighbours.remove(self.clist[row][col])
        return neighbours

    def update_cell_list(self, cell_list: List[list]) -> list:
        """ Выполнить один шаг игры.

        Обновление всех ячеек происходит одновременно. Функция возвращает
        новое игровое поле.

        :param cell_list: Игровое поле, представленное в виде матрицы
        :return: Обновленное игровое поле
        """
        cell_height = len(cell_list)
        cell_width = len(cell_list[0])
        new_clist = [[0] * cell_width for _ in range(cell_height)]
        for i in range(cell_height):
            for k in range(cell_width):
                if sum(self.get_neighbours((i, k))) == 3 \
                        or sum(self.get_neighbours((i, k))) == 2 and cell_list[i][k] == 1:
                    new_clist[i][k] = 1
                else:
                    new_clist[i][k] = 0
        self.clist = new_clist
        return self.clist
