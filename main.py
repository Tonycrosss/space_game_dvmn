import time
from curses import wrapper
import curses


def draw(canvas):
    row, column = (5, 20)
    canvas.border()
    canvas.addstr(row, column, "Hellow world!")
    canvas.refresh()
    time.sleep(1)


if __name__ == '__main__':
    curses.update_lines_cols()
    wrapper(draw)
