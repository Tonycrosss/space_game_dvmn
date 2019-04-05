import time
from curses import wrapper
import curses
import asyncio


async def blink(canvas, row, column, symbol='*'):
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        await asyncio.sleep(0)


def draw(canvas):
    row, column = (5, 20)
    curses.curs_set(0)
    canvas.border()
    # star = "*"
    coroutine = blink(canvas, row, column)
    while True:
        coroutine.send(None)
        canvas.refresh()
        time.sleep(1)
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
