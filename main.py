import time
from curses import wrapper
import curses


def draw(canvas):
    row, column = (5, 20)
    curses.curs_set(0)
    canvas.border()
    star = "*"
    while True:
        canvas.addstr(row, column, star, curses.A_DIM)
        canvas.refresh()
        time.sleep(2)
        canvas.addstr(row, column, star)
        canvas.refresh()
        time.sleep(0.3)
        canvas.addstr(row, column, star, curses.A_BOLD)
        canvas.refresh()
        time.sleep(0.5)
        canvas.addstr(row, column, star)
        canvas.refresh()


if __name__ == '__main__':
    curses.update_lines_cols()
    wrapper(draw)
