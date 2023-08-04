import os
import time

from ..uptech import UpTech
from ..screen import Screen
from io import StringIO
import string

global up, screen


def load(debug: bool = True):
    global up, screen
    up = UpTech(debug=debug, fan_control=False)
    screen = Screen()
    up.adc_io_open()
    screen.set_led_color(0, screen.COLOR_BROWN)
    screen.set_led_color(1, screen.COLOR_GRED)
    # screen.put_string(0, 0, 'test load')


def display(mode):
    if mode == 1:
        attitude = up.atti_all
        str_attitude_pitch = 'Pitch:%.2f  ' % attitude[0]
        str_attitude_roll = 'Roll :%.2f  ' % attitude[1]
        str_attitude_yaw = 'Yaw  :%.2f  ' % attitude[2]

        screen.put_string(0, 30, str_attitude_pitch)
        screen.put_string(0, 48, str_attitude_roll)
        screen.put_string(0, 66, str_attitude_yaw)
    elif mode == 2:
        gyro = up.gyro_all
        str_gyro_1 = f"Gyro x {gyro[0]:.2}"
        str_gyro_2 = f"Gyro y {gyro[1]:.2}"
        str_gyro_3 = f"Gyro z {gyro[2]:.2}"

        screen.put_string(0, 30, str_gyro_1)
        screen.put_string(0, 48, str_gyro_2)
        screen.put_string(0, 66, str_gyro_3)

    elif mode == 3:
        accel = up.acc_all

        str_accel_x = f"x_acc :{accel[0]:.2}"
        str_accel_y = f"y_acc :{accel[1]:.2}"
        str_accel_z = f"z_acc :{accel[2]:.2}"

        screen.put_string(0, 30, str_accel_x)
        screen.put_string(0, 44, str_accel_y)
        screen.put_string(0, 54, str_accel_z)
    screen.refresh()


def print_table(headers, rows, file, row_format="| {} |\n"):
    """
     not function
    :param headers:
    :param rows:
    :param file:
    :param row_format:
    :return:
    """
    # 计算每列的最大宽度
    column_widths = [max(len(str(x)) for x in col) for col in zip(headers, *rows)]

    # 打印表头
    line = "+-{}-+".format("-+-".join("-" * width for width in column_widths))
    print(line, file=file)
    print(row_format.format(*headers), file=file)

    # 打印每一行数据
    for row in rows:
        print(row_format.format(*(str(x).ljust(column_widths[i]) for i, x in enumerate(row))), file=file)
    print(line, file=file)


def read_sensors(interval: float = 1, adc_labels: dict = None, io_labels: dict = None,
                 console_sync: bool = False):
    load()
    try:
        # 创建一个字符串缓冲区对象来保存输出内容
        output_buffer = StringIO()

        # 字段标签的默认名称（只适用于单字符字段）
        default_labels = dict(zip(range(17), string.ascii_uppercase))

        while True:

            # 清空缓冲区

            output_buffer.truncate(0)
            output_buffer.seek(0)

            # 打印 ADC 通道值表格
            print("ADC values:", file=output_buffer)

            print("-" * 44, file=output_buffer)
            screen.set_font_size(screen.FONT_6X8)
            screen.fill_screen(screen.COLOR_BLACK)
            screen.refresh()
            for i in range(9):
                label = adc_labels.get(i, f"({i})") if adc_labels else default_labels[i]
                value = up.adc_all_channels[i]

                screen.put_string(0, i * 8, f'{label}:{value}')

                print(f"| {label:>2}: {value:<4} ", end="", file=output_buffer)
            screen.refresh()
            print("|", file=output_buffer)
            print("-" * 44, file=output_buffer)

            # 打印 IO 状态值表格
            print("IO values:", file=output_buffer)
            print("-" * 33, file=output_buffer)
            for i in range(8):
                label = io_labels.get(i, f"({i})") if io_labels else default_labels[i + 9]
                value = up.io_all_channels[i]
                print(f"| {label:>2}: {value:<4} ", end="", file=output_buffer)
            print("|", file=output_buffer)
            print("-" * 33, file=output_buffer)

            # 使用ANSI转义序列清空当前行和移动到第一列

            # 打印缓冲区中的内容
            if console_sync:
                os.system('clear')
            print(output_buffer.getvalue(), end="")

            time.sleep(interval)

    except KeyboardInterrupt:
        screen.fill_screen(screen.COLOR_BLACK)
        screen.refresh()
