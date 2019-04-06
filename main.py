import time
from curses import wrapper
import curses
import asyncio
import random
from tools import draw_frame
from tools import read_controls
# STARS = "+*.:"
STARS = ["+", "*", ".", ":"]


async def fire(canvas, start_row, start_column, rows_speed=-0.3,
               columns_speed=0):
    """Display animation of gun shot. Direction and speed can be specified."""

    row, column = start_row, start_column

    canvas.addstr(round(row), round(column), '*')
    await asyncio.sleep(0)

    canvas.addstr(round(row), round(column), 'O')
    await asyncio.sleep(0)
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
    while True:
        row_direction, column_direction, space_pressed = read_controls(canvas)
        row = row + row_direction
        column = column + column_direction
        draw_frame(canvas, start_row=row, start_column=column, text=frame_1)
        canvas.refresh()

        await asyncio.sleep(0)

        # стираем предыдущий кадр, прежде чем рисовать новый
        draw_frame(canvas, row, column, text=frame_1, negative=True)
        draw_frame(canvas, row, column, text=frame_2)
        canvas.refresh()

        await asyncio.sleep(0)

        draw_frame(canvas, row, column, text=frame_2, negative=True)

async def blink(canvas, row, column, symbol='*'):
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        for _ in range(20):
            await asyncio.sleep(0)
        # await asyncio.sleep(0)
        # await asyncio.sleep(0)
        # await asyncio.sleep(0)
        # await asyncio.sleep(0)
        # await asyncio.sleep(0)
        # await asyncio.sleep(0)
        # await asyncio.sleep(0)
        # await asyncio.sleep(0)
        # await asyncio.sleep(0)
        # await asyncio.sleep(0)
        # await asyncio.sleep(0)
        # await asyncio.sleep(0)
        # await asyncio.sleep(0)
        # await asyncio.sleep(0)
        # await asyncio.sleep(0)
        # await asyncio.sleep(0)
        # await asyncio.sleep(0)
        # await asyncio.sleep(0)
        # await asyncio.sleep(0)
        for _ in range(random.randint(0, 10)):
            await asyncio.sleep(0)
        canvas.addstr(row, column, symbol)
        for _ in range(3):
            await asyncio.sleep(0)
        # await asyncio.sleep(0)
        # await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        for _ in range(5):
            await asyncio.sleep(0)
        # await asyncio.sleep(0)
        # await asyncio.sleep(0)
        # await asyncio.sleep(0)
        # await asyncio.sleep(0)
        # await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(3):
            await asyncio.sleep(0)
        # await asyncio.sleep(0)
        # await asyncio.sleep(0)
        # await asyncio.sleep(0)


def draw(canvas):
    canvas.nodelay(True)
    max_y, max_x = canvas.getmaxyx()
    columns = [x for x in range(1, max_x - 1)]
    rows = [y for y in range(1, max_y - 1)]
    # row, column = (5, 20)
    curses.curs_set(0)
    canvas.border()
    # star = "*"
    coroutines = []
    for star in range(50):
        star = blink(canvas, row=random.choice(rows),
                     column=random.choice(columns),
                     symbol=random.choice(STARS))
        coroutines.append(star)
        # column += 1
    # shot = fire(canvas, start_row=18, start_column=38)
    # coroutines.append(shot)
    with open("./rocket_frame_1.txt", "r") as f:
        frame_1 = f.read()
    with open("./rocket_frame_2.txt", "r") as f:
        frame_2 = f.read()
    # space_ship = animate_spaceship(canvas, row=9, column=38, frame_1=frame_1, frame_2=frame_2)
    # coroutines.append(space_ship)
    # star_1 = blink(canvas, row, column)
    # star_2 = blink(canvas, row, 21)
    # star_3 = blink(canvas, row, 22)
    # star_4 = blink(canvas, row, 23)
    # star_5 = blink(canvas, row, 24)
    # coroutines = [star_1, star_2, star_3, star_4, star_5]
    spaceship_row = 9
    spaceship_column = 38
    space_ship = animate_spaceship(canvas, row=spaceship_row,
                                   column=spaceship_column,
                                   frame_1=frame_1, frame_2=frame_2)
    coroutines.append(space_ship)

    while True:
        for coroutine in coroutines:
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)
        if len(coroutines) == 0:
            break
        canvas.refresh()
        time.sleep(0.1)
        # canvas.addstr(row, column, star, curses.A_DIM)
        # canvas.refresh()
        # time.sleep(2)
        # canvas.addstr(row, column, star)
        # canvas.refresh()
        # time.sleep(0.3)
        # canvas.addstr(row, column, star, curses.A_BOLD)
        # canvas.refresh()
        # time.sleep(0.5)
        # canvas.addstr(row, column, star)
        # canvas.refresh()


if __name__ == '__main__':
    curses.update_lines_cols()
    wrapper(draw)
