# coding=utf-8
from typing import List, Tuple, Optional
from copy import deepcopy


def shape(maze):
    """
    Функция возвращает размер лабиринта

    :param: maze: Лабиринт
    :return: Число строк, число столбцов
    """
    assert maze, "maze can't be empty"
    return len(maze), len(maze[0])


def neighbours(maze, pos):
    """
    Функция возвращает возможные направления движения в лабиринте
    относительно текущей позиции

    :param maze: Лабиринт
    :param pos: Текущая позиция в лабиринте (строка, столбец)
    :return: Список возможных позиций

    >>> neighbours(simple_maze, simple_initial_pos)
    {'left': True, 'up': False, 'right': False, 'down': False}
    >>> neighbours(simple_maze, initial_pos)
    {'left': False, 'up': True, 'right': False, 'down': True}
    >>> neighbours(maze, initial_pos)
    {'left': False, 'up': False, 'right': True, 'down': False}
    >>> neighbours(maze, simple_initial_pos)
    {'left': False, 'up': True, 'right': False, 'down': True}
    """
    row, col = pos
    result = {"left": False,
              "up": False,
              "right": False,
              "down": False,
              }
    if col > 0:
        result["left"] = maze[row][col - 1]
    if row > 0:
        result["up"] = maze[row - 1][col]
    if col < len(maze[0]) - 1:
        result["right"] = maze[row][col + 1]
    if row < len(maze) - 1:
        result["down"] = maze[row + 1][col]
    return result


def find_route(maze, pos):
    """
    Поиск выхода из лабиринта.

    Функция возвращает кратчайший путь до выхода из лабиринта.

    :param maze: Лабирнит
    :param pos: Текущая позиция в лабиринте (строка, столбец)
    :return: Кратчайший путь до выхода
    """
    pass


def print_maze(maze, pos):
    """
    Функция выводит лабиринт и текущее положение в нем.

    Возможные ходы должны отмечаться '.', текущее положение '☺',
    стена '☒', а выход '☼'.

    Пример:
    ☒☒☒☒☒☒☒
    ☒☺.☒.☼☒
    ☒☒.☒.☒☒
    ☒..☒..☒
    ☒.☒☒☒.☒
    ☒.....☒
    ☒☒☒☒☒☒☒

    :param maze: Лабиринт
    :param pos: Текущая позиция в лабиринте (строка, столбец)

    >>> print_maze(simple_maze, simple_initial_pos)
    ☼..
    ☒.☒
    ..☺
    >>> print_maze(maze, initial_pos)
    ☒☒☒☒☒☒☒
    ☒☺.☒.☼☒
    ☒☒.☒.☒☒
    ☒..☒..☒
    ☒.☒☒☒.☒
    ☒.....☒
    ☒☒☒☒☒☒☒
    """
    for row, line in enumerate(maze):
        for col, cell in enumerate(line):
            current_pos = (row, col)
            if current_pos == pos:
                print("☺", end="")
                continue
            if cell is None:
                print("☼", end="")
            if cell is False:
                print("\u2612", end="")
            if cell is True:
                print(".", end="")
        print("\n", end="")


def escape(maze, pos):
    """
    Вывести последовательно путь до выхода из лабиринта
    :param maze: Лабиринт
    :param pos: Текущая позиция в лабиринте (строка, столбец)

    >>> print(escape(simple_maze, simple_initial_pos))
    ['left', 'up', 'up', 'left']
    >>> print(escape(maze, initial_pos))
    ['right', 'down', 'down', 'left', 'down', 'down', 'right', 'right', 'right', 'right', 'up', 'up', 'left', 'up', 'up', 'right']
    """
    path = []
    current_row, current_col = pos
    for direction in ["left", "up", "right", "down"]:
        direction_row, direction_col = pos
        if direction == "left":
            direction_col -= 1
        if direction == "up":
            direction_row -= 1
        if direction == "right":
            direction_col += 1
        if direction == "down":
            direction_row += 1
        direction_pos = (direction_row, direction_col)
        if neighbours(maze, pos)[direction] is None:
            path = [direction]
            break
        if neighbours(maze, pos)[direction] is True:
            path = [direction]
            new_maze = deepcopy(maze)
            new_maze[current_row][current_col] = False
            new_path = escape(new_maze, direction_pos)
            if new_path:
                path.extend(new_path)
    return path


simple_maze = [
    [None, True, True],
    [False, True, False],
    [True, True, True]
]

simple_initial_pos = (2, 2)

maze = [
    [False, False, False, False, False, False, False],
    [False, True, True, False, True, None, False],
    [False, False, True, False, True, False, False],
    [False, True, True, False, True, True, False],
    [False, True, False, False, False, True, False],
    [False, True, True, True, True, True, False],
    [False, False, False, False, False, False, False]
]

initial_pos = (1, 1)


if __name__ == "__main__":
    print_maze(simple_maze, simple_initial_pos)
    print_maze(maze, initial_pos)

    print(escape(simple_maze, simple_initial_pos))
    print(escape(maze, initial_pos))

    print(neighbours(simple_maze, simple_initial_pos))
    print(neighbours(simple_maze, initial_pos))
    print(neighbours(maze, initial_pos))
    print(neighbours(maze, simple_initial_pos))
