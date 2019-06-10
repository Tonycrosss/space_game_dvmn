import time
from curses import wrapper
import curses
import asyncio
import random
from tools import draw_frame
from tools import read_controls
from tools import get_frame_size

STARS = ["+", "*", ".", ":"]
coroutines = []


async def sleep(tics=1):
    for _ in range(0, tics):
        await asyncio.sleep(0)


async def fly_garbage(canvas, column, garbage_frame, speed=0.5):
    """Animate garbage, flying from top to bottom. Сolumn position will stay same, as specified on start."""
    rows_number, columns_number = canvas.getmaxyx()

    column = max(column, 0)
    column = min(column, columns_number - 1)

    row = 0

    while row < rows_number:
        draw_frame(canvas, row, column, garbage_frame)
        await sleep()
        draw_frame(canvas, row, column, garbage_frame, negative=True)
        row += speed


async def fill_orbit_with_garbage(canvas):
    global coroutines
    # garbage
    with open("./garbage_frame_1.txt", "r") as f:
        garbage_frame_1 = f.read()
    with open("./garbage_frame_2.txt", "r") as f:
        garbage_frame_2 = f.read()
    with open("./garbage_frame_3.txt", "r") as f:
        garbage_frame_3 = f.read()

    garbage_list = [garbage_frame_1, garbage_frame_2, garbage_frame_3]

    while True:
        random_column = random.randint(0, 60)
        random_garbage = random.choice(garbage_list)
        await sleep(20)
        coroutines.append(fly_garbage(canvas, random_column, random_garbage))
        # coroutines.append(random_garbage_start)



async def fire(canvas, start_row, start_column, rows_speed=-0.3,
               columns_speed=0):
    """Display animation of gun shot. Direction and speed can be specified."""

    row, column = start_row, start_column

    canvas.addstr(round(row), round(column), '*')
    await sleep()

    canvas.addstr(round(row), round(column), 'O')
    await sleep()
    canvas.addstr(round(row), round(column), ' ')

    row += rows_speed
    column += columns_speed

    symbol = '-' if columns_speed else '|'

    rows, columns = canvas.getmaxyx()
    max_row, max_column = rows - 1, columns - 1

    curses.beep()

    while 0 < row < max_row and 0 < column < max_column:
        canvas.addstr(round(row), round(column), symbol)
        await asyncio.sleep(0)
        canvas.addstr(round(row), round(column), ' ')
        row += rows_speed
        column += columns_speed


async def animate_spaceship(canvas, row, column, frame_1, frame_2):
    # 19, 77
    max_row, max_column = canvas.getmaxyx()
    min_row, min_column = 0, 0
    space_ship_row, space_ship_column = get_frame_size(frame_1)

    while True:
        old_row = row
        old_column = column
        row_direction, column_direction, space_pressed = read_controls(canvas)
        row = row + row_direction
        column = column + column_direction
        spaceship_left_upper_point = (row, column)
        spaceship_right_upper_point = (row, column + space_ship_column)
        spaceship_left_lower_point = (row + space_ship_row, column)
        spaceship_right_lower_point = (row + space_ship_row, column + space_ship_column)
        space_points = [spaceship_left_upper_point,
                        spaceship_right_upper_point,
                        spaceship_left_lower_point,
                        spaceship_right_lower_point]
        is_border = False
        for point in space_points:
            point_row, point_column = point
            if point_row >= max_row or point_row <= min_row or point_column >= max_column or point_column <= min_column:
                is_border = True
                row = old_row
                column = old_column
        if not is_border:
            draw_frame(canvas, start_row=row, start_column=column, text=frame_1)
            canvas.refresh()

            await sleep()

            # стираем предыдущий кадр, прежде чем рисовать новый
            draw_frame(canvas, row, column, text=frame_1, negative=True)
            draw_frame(canvas, row, column, text=frame_2)
            canvas.refresh()

            await sleep()

            draw_frame(canvas, row, column, text=frame_2, negative=True)


async def blink(canvas, row, column, offset_tic, symbol='*', ):
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        await sleep(20)

        await sleep(offset_tic)
        canvas.addstr(row, column, symbol)

        await sleep(3)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        await sleep(5)

        canvas.addstr(row, column, symbol)
        await sleep(3)


def draw(canvas):
    global coroutines
    canvas.nodelay(True)
    max_y, max_x = canvas.getmaxyx()
    columns = [x for x in range(1, max_x - 1)]
    rows = [y for y in range(1, max_y - 1)]
    curses.curs_set(0)
    canvas.border()

    for star in range(50):
        offset_tic = random.randint(0, 10)
        star = blink(canvas, row=random.choice(rows),
                     column=random.choice(columns),
                     symbol=random.choice(STARS),
                     offset_tic=offset_tic)
        coroutines.append(star)

    with open("./rocket_frame_1.txt", "r") as f:
        frame_1 = f.read()
    with open("./rocket_frame_2.txt", "r") as f:
        frame_2 = f.read()


    coroutines.append(fill_orbit_with_garbage(canvas))

    spaceship_row = 9
    spaceship_column = 38
    space_ship = animate_spaceship(canvas, row=spaceship_row,
                                   column=spaceship_column,
                                   frame_1=frame_1, frame_2=frame_2)
    coroutines.append(space_ship)

    while coroutines:
        for coroutine in coroutines:
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)
        canvas.refresh()
        time.sleep(0.1)


if __name__ == '__main__':
    curses.update_lines_cols()
    wrapper(draw)

