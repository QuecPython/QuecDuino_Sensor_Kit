"""
@file      : Display_LCD.py
@author    : Aaron Chen (aaron.chen@example.com)
@brief     : LCD display control using GPIO
@version   : 0.1
@date      : 2026-04-21
@copyright : Copyright (c) 2026
"""


from machine import Pin
import utime

# 初始化数码管各段 GPIO
seg32 = Pin(Pin.GPIO32, Pin.OUT, Pin.PULL_DISABLE, 1)  # 右下 a
seg31 = Pin(Pin.GPIO31, Pin.OUT, Pin.PULL_DISABLE, 1)  # 正上 b
seg30 = Pin(Pin.GPIO30, Pin.OUT, Pin.PULL_DISABLE, 1)  # 右上 c
seg33 = Pin(Pin.GPIO33, Pin.OUT, Pin.PULL_DISABLE, 1)  # 正下 d
seg2  = Pin(Pin.GPIO2,  Pin.OUT, Pin.PULL_DISABLE, 1)  # 中间 e
seg3  = Pin(Pin.GPIO3,  Pin.OUT, Pin.PULL_DISABLE, 1)  # 小数点 f
seg14 = Pin(Pin.GPIO14, Pin.OUT, Pin.PULL_DISABLE, 1)  # 左下 g
seg15 = Pin(Pin.GPIO15, Pin.OUT, Pin.PULL_DISABLE, 1)  # 左上 h

# 段码表：0~9 对应各段亮灭（0亮1灭）
# 顺序：a b c d e f g h
num_table = [
    [0,0,0,0,1,0,0,0],  # 0
    [0,1,0,1,1,0,1,1],  # 1
    [1,0,0,0,0,0,0,1],  # 2
    [0,0,0,0,0,0,1,1],  # 3
    [0,1,0,1,0,0,1,0],  # 4
    [0,0,1,0,0,0,1,0],  # 5
    [0,0,1,0,0,0,0,0],  # 6
    [0,0,0,1,1,0,1,1],  # 7
    [0,0,0,0,0,0,0,0],  # 8
    [0,0,0,0,0,0,1,0],  # 9
]

def display_num(n):
    if n < 0 or n > 9:
        return
    val = num_table[n]
    seg32.write(val[0])
    seg31.write(val[1])
    seg30.write(val[2])
    seg33.write(val[3])
    seg2.write(val[4])
    seg3.write(val[5])
    seg14.write(val[6])
    seg15.write(val[7])

# 循环显示 0-9
while True:
    for i in range(10):
        display_num(i)
        utime.sleep(1)
