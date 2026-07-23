"""
@file      : rgb_led.py
@author    : Arnold Feng
@brief     : RGB LED 控制模块，支持按颜色名和 RGB 值设置颜色
@version   : 0.2
@date      : 2026-06-08
@copyright : Copyright (c) 2026
"""

from machine import Pin
import utime


class RGBLED(object):
    """RGB LED 控制类，通过三个 GPIO 引脚控制红、绿、蓝三色混光。

    通过 active_level 参数适配不同硬件接法：
        - active_level=0：共阳极（低电平点亮，默认）
        - active_level=1：共阴极（高电平点亮）

    典型用法:
        rgb = RGBLED(Pin.GPIO32, Pin.GPIO30, Pin.GPIO31, active_level=1)
        rgb.set_color_by_name("red")
        rgb.blink(colors=["red", "blue"], interval=0.5, times=3)

    Args:
        red_pin:     红色通道 GPIO 引脚（Pin 对象）
        green_pin:   绿色通道 GPIO 引脚（Pin 对象）
        blue_pin:    蓝色通道 GPIO 引脚（Pin 对象）
        active_level: 点亮电平，0=低电平点亮，1=高电平点亮，默认 0（共阳极）
    """

    # 颜色名 -> RGB 逻辑值映射（1=亮, 0=灭，与硬件电平解耦）
    COLOR_MAP = {
        "red":    (1, 0, 0),
        "green":  (0, 1, 0),
        "blue":   (0, 0, 1),
        "yellow": (1, 1, 0),
        "purple": (1, 0, 1),
        "cyan":   (0, 1, 1),
        "white":  (1, 1, 1),
        "off":    (0, 0, 0),
    }

    def __init__(self, red_pin, green_pin, blue_pin, active_level=0):
        self._active = active_level
        self._inactive = 0 if active_level else 1
        self.red = red_pin
        self.green = green_pin
        self.blue = blue_pin
        self._state = (0, 0, 0)  # 当前逻辑颜色 (r, g, b)

    # ---- 基础控制 ----

    def set_color(self, r, g, b):
        """设置 RGB 三通道逻辑状态（1=亮, 0=灭）。

        Args:
            r: 红色通道，1=亮, 0=灭
            g: 绿色通道，1=亮, 0=灭
            b: 蓝色通道，1=亮, 0=灭
        """
        self._state = (r, g, b)
        self.red.write(self._active if r else self._inactive)
        self.green.write(self._active if g else self._inactive)
        self.blue.write(self._active if b else self._inactive)

    def set_color_by_name(self, name):
        """通过颜色名称设置 LED 颜色。

        支持的颜色：red, green, blue, yellow, purple, cyan, white, off

        Args:
            name: 颜色名称字符串（大小写不敏感）

        Returns:
            bool: True 表示设置成功，False 表示未知颜色
        """
        name = name.lower()
        if name in self.COLOR_MAP:
            self.set_color(*self.COLOR_MAP[name])
            return True
        return False

    def off(self):
        """熄灭所有通道。"""
        self.set_color(0, 0, 0)

    # ---- 状态查询 ----

    def read(self):
        """获取当前 RGB 逻辑状态。

        Returns:
            tuple: (r, g, b)，1=亮, 0=灭
        """
        return self._state

    # ---- 效果 ----

    def blink(self, colors=None, interval=0.5, times=None):
        """多色闪烁，在指定颜色列表间循环切换。

        Args:
            colors:   颜色名列表，默认 ["red", "green", "blue"]
            interval: 切换间隔，单位秒，默认 0.5s
            times:    循环次数（完整遍历 colors 为 1 次），None 表示无限循环

        Example:
            rgb.blink(colors=["red", "off"], interval=0.3, times=5)
        """
        if colors is None:
            colors = ["red", "green", "blue"]

        n = 0
        while times is None or n < times:
            for color in colors:
                self.set_color_by_name(color)
                utime.sleep(interval)
            n += 1

    def demo(self, interval=1):
        """演示循环，依次展示所有预设颜色。

        Args:
            interval: 切换间隔，单位秒，默认 1 秒
        """
        color_names = list(self.COLOR_MAP.keys())
        while True:
            for color in color_names:
                self.set_color_by_name(color)
                print("LED color set to {}".format(color))
                utime.sleep(interval)


# ---- 独立运行测试 ----
if __name__ == "__main__":
    rgb_led = RGBLED(
        red_pin=Pin(Pin.GPIO32, Pin.OUT, Pin.PULL_DISABLE, 0),
        green_pin=Pin(Pin.GPIO30, Pin.OUT, Pin.PULL_DISABLE, 0),
        blue_pin=Pin(Pin.GPIO31, Pin.OUT, Pin.PULL_DISABLE, 0),
        active_level=0,
    )
    rgb_led.demo(interval=1)
