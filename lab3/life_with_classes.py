import pygame
from pygame.locals import *
from typing import List
import random
from copy import deepcopy
from pythonlangutil.overload import Overload


class GameOfLife:

    def __init__(self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10):
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

    def draw_grid(self):
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'), (0, y), (self.width, y))

    def draw_cell_list(self, clist: List[list]) -> None:
        """ Отображение списка клеток
        :param clist: Список клеток для отрисовки, представленный в виде матрицы
        """

        cell_height = len(clist)
        cell_width = len(clist[0])
        for i in range(cell_height):
            for k in range(cell_width):
                if clist[i][k].is_alive() == 1:
                    pygame.draw.rect(self.screen, pygame.Color(0, 255, 0),
                                     pygame.Rect(k*self.cell_size, i*self.cell_size, self.cell_size, self.cell_size))
                else:
                    pygame.draw.rect(self.screen, pygame.Color(255, 255, 255),
                                     pygame.Rect(k*self.cell_size, i*self.cell_size, self.cell_size, self.cell_size))

    def run(self):
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))

        # Создание списка клеток
        self.clist = CellList(self.cell_height, self.cell_width, randomize=True)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

            # Отрисовка списка клеток
            self.draw_cell_list(self.clist.clist)
            self.draw_grid()

            # Выполнение одного шага игры (обновление состояния ячеек)
            self.clist.update()

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()


class Cell:

    def __init__(self, row: int, col: int, state: int = 0):
        self.pos = (row, col)
        self.state = state

    def is_alive(self) -> int:
        return self.state


class CellList:

    def __init__(self, nrows: int, ncols: int, randomize: bool = False):
        self.nrows = nrows
        self.ncols = ncols
        self.clist = [[Cell(0, 0, 0)]*self.ncols for _ in range(self.nrows)]
        if randomize:
            for i in range(self.nrows):
                for k in range(self.ncols):
                    self.clist[i][k] = Cell(i, k, random.randint(0, 1))
        else:
            for i in range(self.nrows):
                for k in range(self.ncols):
                    self.clist[i][k] = Cell(i, k, 0)

    def get_neighbours(self, cell: Cell) -> list:
        row, col = cell.pos
        neighbours = [self.clist[i][k]
                      for i in range(row - 1, row + 2)
                      for k in range(col - 1, col + 2)
                      if 0 <= i < self.nrows and 0 <= k < self.ncols]
        neighbours.remove(self.clist[row][col])
        return neighbours

    def update(self):
        new_clist = deepcopy(self)
        for i in range(self.nrows):
            for k in range(self.ncols):
                if sum(j.is_alive() for j in self.get_neighbours(self.clist[i][k])) == 3 \
                        or sum(j.is_alive() for j in self.get_neighbours(self.clist[i][k])) == 2\
                        and self.clist[i][k].is_alive() == 1:
                    new_clist.clist[i][k] = Cell(i, k, 1)
                else:
                    new_clist.clist[i][k] = Cell(i, k, 0)
        self.clist = new_clist.clist
        return self

    def __iter__(self):
        self.row_counter, self.col_counter = 0, 0
        return self

    def __next__(self) -> Cell:
        if self.row_counter == self.nrows:
            raise StopIteration

        if self.col_counter + 1 < self.ncols:
            self.col_counter += 1
            return self.clist[self.row_counter][self.col_counter - 1]
        else:
            self.col_counter = 0
            self.row_counter += 1
            return self.clist[self.row_counter - 1][self.ncols - 1]

    def __str__(self):
        list = [[str(self.clist[i][k].is_alive()) for k in range(self.ncols)] for i in range(self.nrows)]
        string = '['
        for i in range(self.nrows - 1):
            string += str(list[i]) + ',\n'
        string += str(list[self.nrows - 1]) + ']'
        return string

    @classmethod
    def from_file(cls, filename: str):
        int_clist = [[int(char) for char in line if char != '\n'] for line in open(filename, "r")]
        print()
        rows = len(int_clist)
        cols = len(int_clist[0])
        new_clist = CellList(rows, cols)
        for i in range(rows):
            for k in range(cols):
                new_clist.clist[i][k] = Cell(i, k, int_clist[i][k])
        return new_clist
