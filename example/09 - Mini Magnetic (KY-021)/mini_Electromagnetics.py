"""
@file      : mini_Electromagnetics.py
@author    : Aaron Chen (aaron.chen@example.com)
@brief     : Mini Electromagnetics project using a mercury switch to detect magnetic field changes and control an output pin accordingly.
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
        if gpio.read() == 0:
            print("有磁场变化")
            gpio1.write(1)
        else:
            print("没有磁场变化")
            gpio1.write(0)
        utime.sleep(1)
        

if __name__ == '__main__':
    main()