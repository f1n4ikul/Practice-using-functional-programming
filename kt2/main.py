from math import cos, sin, pi
from enum import Enum
from typing import Callable, Tuple


Point = float
Distance = float
Angle = float
Position = Tuple[Point, Point]

class CarriageState(Enum):
    UP = 0
    DOWN = 1

class LineColor(Enum):
    BLACK = "черный"
    RED = "красный"
    GREEN = "зелёный"

PlotterState = Tuple[Position, Angle, LineColor, CarriageState]
Printer = Callable[[str], None]



def draw_line(prt: Printer, from_pos: Position, to_pos: Position, color: LineColor) -> None:
    """Чертит линию от координат `from_pos` к координатам `to_pos`."""
    prt(f"...Чертим линию из {from_pos} в {to_pos} используя {color.value} цвет.")

def calc_new_position(distance: Distance, angle: Angle, current: Position) -> Position:
    """Вычисляет новую позицию."""
    angle_in_rads = angle * (pi / 180.0)
    x = round(current[0] + distance * cos(angle_in_rads))
    y = round(current[1] + distance * sin(angle_in_rads))
    return (x, y)

def move(prt: Printer, distance: Distance, state: PlotterState) -> PlotterState:
    """Перемещает каретку на расстояние `distance`."""
    position, angle, color, carriage_state = state
    new_position = calc_new_position(distance, angle, position)
    
    if carriage_state == CarriageState.DOWN:
        draw_line(prt, position, new_position, color)
    else:
        prt(f"Передвигаем на {distance} от точки {position}")
    
    return (new_position, angle, color, carriage_state)

def turn(prt: Printer, angle: Angle, state: PlotterState) -> PlotterState:
    """Поворачивает каретку на угол `angle`."""
    position, current_angle, color, carriage_state = state
    new_angle = (current_angle + angle) % 360.0
    prt(f"Поворачиваем на {angle} градусов")
    return (position, new_angle, color, carriage_state)

def carriage_up(prt: Printer, state: PlotterState) -> PlotterState:
    """Поднимает каретку."""
    position, angle, color, _ = state
    prt("Поднимаем каретку")
    return (position, angle, color, CarriageState.UP)

def carriage_down(prt: Printer, state: PlotterState) -> PlotterState:
    """Опускает каретку."""
    position, angle, color, _ = state
    prt("Опускаем каретку")
    return (position, angle, color, CarriageState.DOWN)

def set_color(prt: Printer, color: LineColor, state: PlotterState) -> PlotterState:
    """Устанавливает цвет печати в `color`."""
    position, angle, _, carriage_state = state
    prt(f"Устанавливаем {color.value} цвет линии.")
    return (position, angle, color, carriage_state)

def set_position(prt: Printer, position: Position, state: PlotterState) -> PlotterState:
    """Устанавливает позицию каретки в `position`."""
    _, angle, color, carriage_state = state
    prt(f"Устанавливаем позицию каретки в {position}.")
    return (position, angle, color, carriage_state)



def draw_triangle(prt: Printer, size: float, state: PlotterState) -> PlotterState:
    """Чертит треугольник со сторонами `size`."""
    state = carriage_down(prt, state)
    for _ in range(3):
        state = move(prt, size, state)
        state = turn(prt, 120.0, state)
    return carriage_up(prt, state)

def draw_square(prt: Printer, size: float, state: PlotterState) -> PlotterState:
    """Чертит квадрат со сторонами `size`."""
    state = carriage_down(prt, state)
    for _ in range(4):
        state = move(prt, size, state)
        state = turn(prt, 90.0, state)
    return carriage_up(prt, state)


def initialize_plotter_state(position: Position, angle: Angle, color: LineColor, carriage_state: CarriageState) -> PlotterState:
    return (position, angle, color, carriage_state)

printer: Printer = print

init_position: Position = (0.0, 0.0)
init_color: LineColor = LineColor.BLACK
init_angle: Angle = 0.0
init_carriage_state: CarriageState = CarriageState.UP


plotter_state = initialize_plotter_state(init_position, init_angle, init_color, init_carriage_state)


plotter_state = draw_triangle(printer, 100.0, plotter_state)

plotter_state = set_position(printer, (10.0, 10.0), plotter_state)
plotter_state = set_color(printer, LineColor.RED, plotter_state)
plotter_state = draw_square(printer, 80.0, plotter_state)