"""
@file      : Finger_touch_detection.py
@author    : Aaron Chen (aaron.chen@example.com)
@brief     : Finger touch detection using GPIO interrupt
@version   : 0.1
@date      : 2026-04-22
@copyright : Copyright (c) 2026
"""

from machine import Pin
import utime


# 配置GPIO为输入，上拉
gpio = Pin(Pin.GPIO31, Pin.IN, Pin.PULL_PU)


def main():
    # 假设传感器检测到触摸时输出高电平（1）
    while True:
        if gpio.read() == 1:
            print("检测到触摸")
        else:
            print("没有检测到触摸")
        utime.sleep(1)
        

if __name__ == '__main__':
    main()