# 障碍物检测模块

## **一、** **模块介绍**

障碍物检测模块是红外反射式数字检测器件，也叫红外避障模块，用于近距离障碍物检测、循迹、避障、限位触发；通过红外发射与接收判断前方是否有障碍物，具备响应快、体积小、3.3V/5V 兼容、GPIO 直读、抗干扰强、寿命长等优点。

**模块组成：**

![](../../media/obstacle1.png)

**工作原理：**

工作原理是红外光 线发射管**发射红外光线**，红外光线接收管**接收红外光线**，当**没有接收到返回的红外光线**时，OUT引脚输出**高电平**，当**接收到返回的红外光线时**，OUT引脚输出**低电平**。

## 二、 连接示例

根据表格和图片指导，将外设与开发板一一对应连接

| 外设      | 开发板       |
| --------- | ------------ |
| 模块（+） | 3.3V         |
| 模块（-） | GND          |
| 模块（S） | PIN4(GPIO31) |

![](../../media/obstacle2.png)

## 三、 驱动代码

```python
from machine import Pin, ExtInt
import utime


class ObstacleSensor(object):
    """红外避障传感器类（KY-032），支持轮询和中断两种检测模式。

    传感器输出逻辑：
        - 无障碍物时 OUT 输出低电平 (0)
        - 检测到障碍物时 OUT 输出高电平 (1)

    典型用法:
        sensor = ObstacleSensor(pin=Pin.GPIO31)
        sensor.set_callback(lambda: print("障碍物!"))
        sensor.monitor_polling(interval_ms=200)

    Args:
        pin:  GPIO 引脚号，默认 GPIO31
        pull: 上下拉配置，默认上拉 (Pin.PULL_PU)
    """

    def __init__(self, pin=None, pull=None):
        if pin is None:
            pin = Pin.GPIO31
        if pull is None:
            pull = Pin.PULL_PU
        self._gpio = Pin(pin, Pin.IN, pull)
        self._extint = None
        self._obstacle_flag = False
        self._callback = None
        self._trigger_count = 0

    def set_callback(self, callback):
        """设置障碍物检测回调。

        Args:
            callback: 回调函数，无参数，传 None 取消
        """
        self._callback = callback

    def read_state(self):
        """读取当前传感器状态。

        Returns:
            int: 0=无障碍物, 1=有障碍物
        """
        return self._gpio.read()

    def is_obstacle(self):
        """判断当前是否有障碍物。

        Returns:
            bool: True 表示检测到障碍物
        """
        return self.read_state() == 1

    def _irq_handler(self, args):
        """中断回调，障碍物出现时置位标志。"""
        if self._gpio.read() == 1:
            self._obstacle_flag = True

    @property
    def trigger_count(self):
        """获取累计触发次数。"""
        return self._trigger_count

    def reset_count(self):
        """重置触发计数归零。"""
        self._trigger_count = 0

    def wait_for_obstacle(self, timeout_ms=None):
        """阻塞等待障碍物出现。

        Args:
            timeout_ms: 超时 ms，None 无限等待

        Returns:
            bool: True=障碍物, False=超时
        """
        start = utime.ticks_ms()
        while True:
            if self.is_obstacle():
                return True
            if timeout_ms is not None:
                if utime.ticks_diff(utime.ticks_ms(), start) >= timeout_ms:
                    return False
            utime.sleep_ms(10)

    def wait_for_clear(self, timeout_ms=None):
        """阻塞等待障碍物消失。

        Args:
            timeout_ms: 超时 ms，None 无限等待

        Returns:
            bool: True=已清除, False=超时
        """
        start = utime.ticks_ms()
        while True:
            if not self.is_obstacle():
                return True
            if timeout_ms is not None:
                if utime.ticks_diff(utime.ticks_ms(), start) >= timeout_ms:
                    return False
            utime.sleep_ms(10)

    def monitor_polling(self, interval_ms=200):
        """轮询模式：循环读取传感器状态。

        Args:
            interval_ms: 轮询间隔 ms，默认 200
        """
        print("[ObstacleSensor] 轮询模式启动")
        while True:
            if self._gpio.read() == 0:
                print("无障碍物")
            else:
                self._trigger_count += 1
                print("检测到障碍物")
                if self._callback:
                    self._callback()
            utime.sleep_ms(interval_ms)

    def monitor_interrupt(self, interval_ms=200):
        """中断模式：障碍物触发中断，主循环检查标志。

        Args:
            interval_ms: 主循环检查间隔 ms，默认 200
        """
        self._extint = ExtInt(self._gpio, ExtInt.IRQ_FALLING, ExtInt.PULL_PU, self._irq_handler)
        self._extint.enable()
        print("[ObstacleSensor] 中断模式启动")
        while True:
            if self._obstacle_flag:
                self._trigger_count += 1
                print("检测到障碍物")
                self._obstacle_flag = False
                if self._callback:
                    self._callback()
            utime.sleep_ms(interval_ms)


if __name__ == '__main__':
    sensor = ObstacleSensor(pin=Pin.GPIO31)
    sensor.monitor_polling(interval_ms=200)
```

 