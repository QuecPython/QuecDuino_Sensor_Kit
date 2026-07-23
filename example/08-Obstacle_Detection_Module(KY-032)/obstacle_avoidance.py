"""
@file      : obstacle_avoidance.py
@author    : Aaron Chen
@brief     : KY-032 infrared obstacle avoidance sensor driver
@version   : 0.2
@date      : 2026-04-10
@copyright : Copyright (c) 2026
"""

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

    # ---- 回调 ----

    def set_callback(self, callback):
        """设置障碍物检测回调。

        Args:
            callback: 回调函数，无参数，传 None 取消
        """
        self._callback = callback

    # ---- 读取 ----

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

    # ---- 中断处理 ----

    def _irq_handler(self, args):
        """中断回调，障碍物出现时置位标志。"""
        if self._gpio.read() == 1:
            self._obstacle_flag = True

    # ---- 计数 ----

    @property
    def trigger_count(self):
        """获取累计触发次数。"""
        return self._trigger_count

    def reset_count(self):
        """重置触发计数归零。"""
        self._trigger_count = 0

    # ---- 阻塞等待 ----

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

    # ---- 监控 ----

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


# ---- 独立运行测试 ----
if __name__ == '__main__':
    sensor = ObstacleSensor(pin=Pin.GPIO31)
    # 轮询模式
    sensor.monitor_polling(interval_ms=200)
    # 中断模式（取消注释以切换）
    # sensor.monitor_interrupt(interval_ms=200)
