"""
@file      : Laser_emitter.py
@author    : Aaron Chen (aaron.chen@example.com)
@brief     : Laser emitter control using GPIO
@version   : 0.1
@date      : 2026-04-21
@copyright : Copyright (c) 2026
"""


from machine import Pin
import utime

if __name__=='__main__':
    laser=Pin(Pin.GPIO31,Pin.OUT,Pin.PULL_DISABLE,0)
    while True:
        laser.write(1)
        print("laser on")
        utime.sleep(2)
        laser.write(0)
        print("laser off")
        utime.sleep(2)
        
        
        
        
        
        
        
        
        
        