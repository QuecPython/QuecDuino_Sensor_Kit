"""
@file      : Laser_emitter.py
@author    : Aaron Chen (aaron.chen@example.com)
@brief     : Class-based laser emitter control using GPIO
@version   : 0.2
@date      : 2026-06-02
@copyright : Copyright (c) 2026
"""


from machine import Pin
import utime


class LaserEmitter(object):
    """激光发射器控制类，通过 GPIO 控制激光开关和闪烁。

    通过 active_level 参数适配不同触发方式。

    典型用法:
        laser = LaserEmitter(pin=Pin.GPIO31)
        laser.on()
        laser.blink(interval=0.5, times=3)

    Args:
        pin:          GPIO 引脚号，默认 GPIO31
        active_level: 触发电平，1=高电平触发，0=低电平触发，默认 1
    """

    def __init__(self, pin=Pin.GPIO31, active_level=1):
        self._active_level = active_level
        self._inactive_level = 0 if active_level else 1
        self._gpio = Pin(pin, Pin.OUT, Pin.PULL_DISABLE, self._inactive_level)
        self._state = 0

    # ---- 基础控制 ----

    def on(self):
        """开启激光。"""
        self._state = 1
        self._gpio.write(self._active_level)

    def off(self):
        """关闭激光。"""
        self._state = 0
        self._gpio.write(self._inactive_level)

    def toggle(self):
        """翻转激光状态（开→关，关→开）。"""
        self.off() if self._state else self.on()

    # ---- 状态 ----

    def is_on(self):
        """查询激光是否开启。"""
        return self._state == 1

    def read(self):
        """读取逻辑状态。

        Returns:
            int: 1=开启, 0=关闭
        """
        return self._state

    # ---- 闪烁 ----

    def blink(self, interval=0.5, times=None):
        """激光闪烁。

        Args:
            interval: 亮灭单边持续时间，单位秒，默认 0.5s
            times:    闪烁次数（亮+灭=1次），None 无限循环
        """
        n = 0
        while times is None or n < times:
            self.on()
            utime.sleep(interval)
            self.off()
            utime.sleep(interval)
            n += 1


if __name__ == '__main__':
    laser = LaserEmitter(pin=Pin.GPIO31, active_level=1)
    laser.on()
    while True:
        utime.sleep_ms(1000)
