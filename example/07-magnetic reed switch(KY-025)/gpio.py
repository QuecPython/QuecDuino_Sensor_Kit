from machine import Pin
import utime


# 配置GPIO为输入，上拉
gpio = Pin(Pin.GPIO31, Pin.IN, Pin.PULL_PU)

def main():
    # 假设传感器检测到火焰时输出低电平（0）
    while True:
        if gpio.read() == 0:
            print("没有检测到磁场变化")
        else:
            print("检测到磁场变化")
        utime.sleep(1)
if __name__ == "__main__":
    main()