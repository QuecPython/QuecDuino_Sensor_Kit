"""
@file      : mercury_switch.py
@author    : Aaron Chen (aaron.chen@example.com)
@brief     : Mercury switch detection using GPIO
@version   : 0.1
@date      : 2026-04-21
@copyright : Copyright (c) 2026
"""

from machine import Pin,ExtInt
import utime

# 全局标志位
human_detected = False

# 配置GPIO为输入，上拉
gpio = Pin(Pin.GPIO31, Pin.IN, Pin.PULL_PU)
gpio1=Pin(Pin.GPIO30,Pin.OUT,Pin.PULL_DISABLE,0)

def main():
    # 假设传感器检测到倾斜时输出高电平（1）
    while True:
        if gpio.read() == 1:
            print("水银检测到倾斜")
        else:
            print("水银没有检测到倾斜")
        utime.sleep(1)
        

if __name__ == '__main__':
    main()
