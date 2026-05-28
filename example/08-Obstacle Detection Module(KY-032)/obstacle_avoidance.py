"""
@file      : obstacle_avoidance.py
@author    : Aaron Chen (aaron.chen@example.com)
@brief     : Obstacle avoidance using ultrasonic sensor
@version   : 0.1
@date      : 2024-xx-xx
@copyright : Copyright (c) 2024
"""

from machine import Pin,ExtInt
import utime

# # 全局标志位
# human_detected = False

# # 配置GPIO为输入，上拉
# gpio = Pin(Pin.GPIO31, Pin.IN, Pin.PULL_PU)

# def irq_handler(args):
#     global human_detected, gpio
#     # 假设传感器检测到障碍时输出低电平（0）
#     if gpio.read() == 0:
#         human_detected = True



# # 注册中断：下降沿触发（从1→0，表示有障碍物）
# ext=ExtInt(ExtInt.GPIO31, ExtInt.IRQ_FALLING, ExtInt.PULL_PU, irq_handler)

# print("Waiting for human detection...")
# ext.enable()  # 启用中断
# while True:
#     if human_detected:
#         print("有障碍物")
#         human_detected = False  # 清除标志
#     else:
#         print("无障碍")
#     utime.sleep(1)





# 配置GPIO为输入，浮空
gpio = Pin(Pin.GPIO31, Pin.IN, Pin.PULL_DISABLE)


def main():
    # 假设传感器检测到倾斜时输出高电平（1）
    while True:
        if gpio.read() == 1:
            print("没检测到障碍物")
        else:
            print("检测到障碍物")
        utime.sleep(1)
        

if __name__ == '__main__':
    main()
