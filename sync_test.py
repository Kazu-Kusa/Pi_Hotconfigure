import time
from ..screen import Screen


def count_adds_per_second(display_on_screen: bool = True):
    if display_on_screen:
        screen = Screen()
        screen.LCD_SetFontSize(screen.FONT_5X12)
    else:
        screen = None
    prev_cnt = cnt = 0
    string = ''
    start_time = time.time()
    sync_count = 0
    while True:
        cnt += 1
        if time.time() - start_time >= 1.0:
            if display_on_screen:
                d = cnt - prev_cnt
                if d > 0 and prev_cnt != 0:
                    string = f' rise|{int(d * 100 / prev_cnt)}%'
                elif prev_cnt != 0:

                    string = f' drop|{int(-d * 100 / prev_cnt)}%'
                screen.LCD_PutString(0, 0, f'Tick/s:\n{cnt}{string}')
                screen.LCD_PutString(0, 30, 'higher is better')
                sync_count += 1
                if sync_count == 16:
                    sync_count = 0
                    screen.LCD_FillScreen(screen.COLOR_BLACK)
                screen.LCD_Refresh()

            print(f"\rtick per second: {cnt},pre: {prev_cnt},d: {d}", end='')
            prev_cnt = cnt
            cnt = 0
            start_time = time.time()
