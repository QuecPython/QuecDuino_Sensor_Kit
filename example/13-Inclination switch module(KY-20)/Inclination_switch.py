"""
@file      : Inclination_switch.py
@author    : Aaron Chen (aaron.chen@example.com)
@brief     : Inclination switch detection using GPIO interrupt
@version   : 0.1
@date      : 2026-04-22
@copyright : Copyright (c) 2026
"""


from machine import Pin
import utime


# 配置GPIO为输入，上拉
gpio = Pin(Pin.GPIO31, Pin.IN, Pin.PULL_PU)


def main():
    # 假设传感器检测到触摸时输出低电平（0）
    while True:
        if gpio.read() == 0:
            print("检测到倾斜")
        else:
            print("水平状态")
        utime.sleep(1)
        

if __name__ == '__main__':
    main()