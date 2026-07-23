# 激光发射模块

## **一、** **模块介绍**

**激光发射模块（Laser Emitter Module）** 的核心原理是：**通过半导体激光二极管（LD），将电能高效转化为高亮度、高方向性、单色性的相干光（激光），再经光学系统准直 / 整形后发射出去**。它广泛用于激光测距、激光雷达、光纤通信、激光指示、红外夜视等场景。

## 二、 连接示例

根据表格和图片指导，将外设与开发板一一对应连接

| 外设        | 开发板       |
| ----------- | ------------ |
| Module（+） | 3.3V         |
| Module（-） | GND          |
| Module（S） | PIN4(GPIO31) |

![](../../media/laser1.png)

## 三、 驱动代码

```python
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
        active_level: 1=高电平触发，0=低电平触发，默认 1
    """

    def __init__(self, pin=Pin.GPIO31, active_level=1):
        self._active_level = active_level
        self._inactive_level = 0 if active_level else 1
        self._gpio = Pin(pin, Pin.OUT, Pin.PULL_DISABLE, self._inactive_level)
        self._state = 0

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

    def is_on(self):
        """查询激光是否开启。"""
        return self._state == 1

    def read(self):
        """读取逻辑状态（1=开启, 0=关闭）。"""
        return self._state

    def blink(self, interval=0.5, times=None):
        """激光闪烁。

        Args:
            interval: 亮灭单边持续时间秒，默认 0.5s
            times:    闪烁次数，None 无限循环
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
```

