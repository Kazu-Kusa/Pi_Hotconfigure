import time
from repo.uptechStar.module.up_controller import UpController


def rotating_test():
    controller = UpController()
    while True:
        print('moving')
        try:
            for i in range(11):
                controller.move_cmd(i * 1000, i * 1000)
                print(f'moving at velocity of [{i * 1000}]')
                time.sleep(1)

        except KeyboardInterrupt:
            for i in range(4):
                i += 1
                controller.move_cmd(0, 0)
                print(f' index[{i}] stopped\n')
            break
        # controller.move_cmd(0, 0)


if __name__ == '__main__':
    rotating_test()
