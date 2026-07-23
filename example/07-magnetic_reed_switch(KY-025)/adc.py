"""
@file      : adc.py
@author    : Aaron Chen (aaron.chen@example.com)
@brief     : Class-based magnetic reed switch detection using ADC
@version   : 0.2
@date      : 2026-06-02
@copyright : Copyright (c) 2026
"""


from misc import ADC
from machine import Pin
import _thread
import utime


class MagneticReedSwitch(object):
    """磁簧开关传感器类（ADC 模式），通过模拟量读取磁场强度变化。

    应用场景：门窗防盗、智能计数、位置限位检测、无触点开关等。

    典型用法:
        sensor = MagneticReedSwitch(led_pin=Pin.GPIO31, threshold=900)
        sensor.set_callback(lambda val: print("磁场!", val))
        sensor.start()

    Args:
        adc_channel: ADC 通道，默认 ADC1
        led_pin:     LED 指示 GPIO 引脚，默认 GPIO31，传 None 禁用
        threshold:   磁场检测阈值，低于此值判定为检测到磁场，默认 900
        led_on_ms:   LED 点亮持续时间 ms，默认 500（非阻塞）
    """

    def __init__(self, adc_channel=None, led_pin=Pin.GPIO31,
                 threshold=900, led_on_ms=500):
        self._threshold = threshold
        self._led_on_ms = led_on_ms
        self._led = None
        if led_pin is not None:
            self._led = Pin(led_pin, Pin.OUT, Pin.PULL_DISABLE, 0)
        self._adc = ADC()
        self._adc_channel = self._adc.ADC1 if adc_channel is None else adc_channel
        self._callback = None
        self._is_running = False
        self._last_value = 0
        self._led_off_at = 0

    # ---- 回调 ----

    def set_callback(self, callback):
        """设置磁场检测回调。

        Args:
            callback: 回调函数，签名 callback(adc_value)
        """
        self._callback = callback

    # ---- 阈值 ----

    @property
    def threshold(self):
        return self._threshold

    @threshold.setter
    def threshold(self, value):
        self._threshold = value

    # ---- 读取 ----

    def read_value(self):
        """读取当前磁场强度 ADC 值。

        Returns:
            int: ADC 采样值
        """
        self._last_value = self._adc.read(self._adc_channel)
        return self._last_value

    def is_detected(self):
        """判断最近一次采样是否检测到磁场。

        Returns:
            bool: True 表示检测到磁场
        """
        return self._last_value < self._threshold

    # ---- LED（非阻塞） ----

    def _led_on(self):
        if self._led is not None:
            self._led.write(1)
            self._led_off_at = utime.ticks_ms() + self._led_on_ms

    def _led_tick(self):
        if self._led is not None and self._led_off_at > 0:
            if utime.ticks_diff(utime.ticks_ms(), self._led_off_at) >= 0:
                self._led.write(0)
                self._led_off_at = 0

    # ---- 监控 ----

    def _monitor(self):
        """后台监控循环，非阻塞采样。"""
        while self._is_running:
            value = self.read_value()

            if value < self._threshold:
                self._led_on()
                if self._callback:
                    self._callback(value)

            self._led_tick()
            utime.sleep_ms(500)

    def start(self):
        """启动 ADC 并开启后台监控线程。"""
        self._adc.open()
        self._is_running = True
        _thread.start_new_thread(self._monitor, ())

    def stop(self):
        """停止后台监控线程并关闭 LED。"""
        self._is_running = False
        if self._led is not None:
            self._led.write(0)


# ---- 独立运行测试 ----
if __name__ == '__main__':
    def on_magnet(value):
        print("检测到磁场! ADC = {}".format(value))

    sensor = MagneticReedSwitch(led_pin=Pin.GPIO31, threshold=900)
    sensor.set_callback(on_magnet)
    sensor.start()

    while True:
        utime.sleep_ms(1000)
