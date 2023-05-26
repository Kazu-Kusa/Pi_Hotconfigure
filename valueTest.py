import time

from ..uptech import UpTech
from ..screen import Screen

up = UpTech()
screen = Screen()

up.ADC_IO_Open()
up.ADC_Led_SetColor(0, 0x2F0000)
up.ADC_Led_SetColor(1, 0x002F00)

screen.LCD_PutString(30, 0, 'Kusa')


def display(mode):
    if mode == 1:
        attitude = up.MPU6500_GetAttitude()
        str_attitude_pitch = 'Pitch:%.2f  ' % attitude[0]
        str_attitude_roll = 'Roll :%.2f  ' % attitude[1]
        str_attitude_yaw = 'Yaw  :%.2f  ' % attitude[2]

        screen.LCD_PutString(0, 30, str_attitude_pitch)
        screen.LCD_PutString(0, 48, str_attitude_roll)
        screen.LCD_PutString(0, 66, str_attitude_yaw)
    elif mode == 2:
        gyro = up.MPU6500_GetGyro()
        str_gyro_1 = f"Gyro x {gyro[0]:.2}"
        str_gyro_2 = f"Gyro y {gyro[1]:.2}"
        str_gyro_3 = f"Gyro z {gyro[2]:.2}"

        screen.LCD_PutString(0, 30, str_gyro_1)
        screen.LCD_PutString(0, 48, str_gyro_2)
        screen.LCD_PutString(0, 66, str_gyro_3)

    elif mode == 3:
        accel = up.MPU6500_GetAccel()

        str_accel_x = f"x :{accel[0]:.2}"
        str_accel_y = f"y :{accel[1]:.2}"
        str_accel_z = f"z :{accel[2]:.2}"

        screen.LCD_PutString(0, 30, str_accel_x)
        screen.LCD_PutString(0, 44, str_accel_y)
        screen.LCD_PutString(0, 54, str_accel_z)
    screen.LCD_Refresh()


def read_sensors(mode: int = 1, interval: float = 1):
    try:
        while True:

            display(mode)
            print("adc_value : ", end="")

            for i in range(9):
                print(f"({i}):", up.ADC_Get_All_Channel()[i], end=" |")
            print("\n")

            print("io_value : ", end="")

            for i in range(8):
                print(f"({i}):", up.ADC_IO_GetAllInputLevel(), end=" |")
            print("\n")

            time.sleep(interval)
    except KeyboardInterrupt:
        screen.LCD_Refresh()


if __name__ == '__main__':
    read_sensors()
