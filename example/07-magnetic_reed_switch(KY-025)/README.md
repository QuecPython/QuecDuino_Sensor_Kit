# KY-025 磁簧开关（干簧管）传感器模块介绍

KY-025是一款基于**磁簧开关（Reed Switch，又称干簧管）**原理的磁控传感器模块。它本质上是一个受磁场控制的微型电气开关，当有磁铁靠近时，内部的金属簧片会吸合导通电路；当磁铁远离时，簧片会自动弹开断开电路。

由于其结构简单、灵敏度高且无需直接接触即可触发，KY-025常被用于各种物联网项目中作为非接触式的接近检测或位置限位装置。

![](../../media/reed1.png)

## 核心特点

- **双重信号输出**：模块同时提供数字量（DO）和模拟量（AO）两种输出接口，既能做简单的开关判断，也能感知磁场强度的相对变化。
- **灵敏度可调**：板载精密电位器（微调旋钮），可以根据实际应用场景旋转调节传感器的探测距离和触发灵敏度。
- **直观的工作指示**：配有电源指示灯和工作状态LED，当检测到磁场触发时，板载LED会亮起，方便调试与观察。
- **宽电压兼容**：通常支持3.3V至5V的宽电压供电，能够完美适配Arduino、STM32以及你手中的QuecDuino等各类主流单片机开发板。

## **引脚说明与接线**

KY-025模块通常引出4个标准引脚，具体的定义如下：

| 引脚名称    | 功能说明     | 接线建议                      |
| :---------- | :----------- | :---------------------------- |
| **+ (VCC)** | 电源正极     | 接开发板的 3.3V 或 5V         |
| **G (GND)** | 电源负极     | 接开发板的 GND                |
| **D0**      | 数字信号输出 | 接开发板的普通GPIO（如引脚4） |
| **A0**      | 模拟信号输出 | 接开发板的ADC引脚（如A0）     |

## 工作原理详解

1. **数字输出（D0）**：这是一个开关量信号。当你调节好灵敏度后，一旦有磁铁进入有效探测范围，引脚4会输出高电平（或低电平，视具体电路设计而定），同时板载LED点亮；磁铁移开后恢复原状。这非常适合用来制作“门磁报警”或“到位检测”。
2. **模拟输出（A0）**：该引脚输出的电压值会随着磁场强度的变化而线性改变。通常情况下，没有磁场时输出较高数值，随着磁铁逐渐靠近，输出电压会逐渐降低。通过读取这个模拟值，你可以大致判断出磁铁与传感器之间的距离远近。

##  常见应用场景

- **门窗防盗报警**：将模块安装在门框，磁铁安装在门扇上，开门即触发警报。
- **智能计数与测速**：在风扇叶片或旋转物体上安装磁铁，每转一圈触发一次，从而计算转速或累计次数。
- **位置限位检测**：在机械臂或移动小车上，用于检测是否到达了预设的物理边界。
- **无触点开关**：作为珠宝盒、礼品盒的开盖亮灯触发器，既隐蔽又耐用。

## 驱动代码

### ADC 模式（模拟量读取磁场强度）

```python
from misc import ADC
from machine import Pin
import _thread
import utime


class MagneticReedSwitch(object):
    """磁簧开关传感器类（ADC 模式），通过模拟量读取磁场强度变化。

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

    def set_callback(self, callback):
        """设置磁场检测回调。

        Args:
            callback: 回调函数，签名 callback(adc_value)
        """
        self._callback = callback

    @property
    def threshold(self):
        return self._threshold

    @threshold.setter
    def threshold(self, value):
        self._threshold = value

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

    def _led_on(self):
        if self._led is not None:
            self._led.write(1)
            self._led_off_at = utime.ticks_ms() + self._led_on_ms

    def _led_tick(self):
        if self._led is not None and self._led_off_at > 0:
            if utime.ticks_diff(utime.ticks_ms(), self._led_off_at) >= 0:
                self._led.write(0)
                self._led_off_at = 0

    def _monitor(self):
        """后台监控循环，非阻塞采样。"""
        while self._is_running:
            value = self.read_value()
            detected = value < self._threshold
            print("ADC: {} | 状态: {}".format(value, "检测到磁场" if detected else "无磁场"))

            if detected:
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


if __name__ == '__main__':
    def on_magnet(value):
        print("检测到磁场! ADC = {}".format(value))

    sensor = MagneticReedSwitch(led_pin=Pin.GPIO31, threshold=900)
    sensor.set_callback(on_magnet)
    sensor.start()

    while True:
        utime.sleep_ms(1000)
```

### GPIO 模式（数字量检测开关状态）

```python
from machine import Pin
import utime


class ReedSwitch(object):
    """磁簧开关传感器类（GPIO 模式），通过数字量检测磁场状态变化。

    Args:
        pin:           GPIO 引脚号，默认 GPIO31
        trigger_level: 触发电平，0=低电平触发，1=高电平触发，默认 0
        pull:          上下拉配置，默认上拉 (Pin.PULL_PU)
    """

    def __init__(self, pin=Pin.GPIO31, trigger_level=0, pull=Pin.PULL_PU):
        self._gpio = Pin(pin, Pin.IN, pull)
        self._trigger_level = trigger_level
        self._last_state = self._gpio.read()
        self._callback = None
        self._trigger_count = 0

    def set_callback(self, callback):
        """设置状态变化回调。

        Args:
            callback: 回调函数，签名 callback(is_triggered)
        """
        self._callback = callback

    def read_state(self):
        """读取当前 GPIO 电平状态。

        Returns:
            int: 0 或 1
        """
        return self._gpio.read()

    def is_triggered(self):
        """判断当前是否处于触发状态（检测到磁场）。

        Returns:
            bool: True 表示已触发
        """
        return self.read_state() == self._trigger_level

    def check_state_change(self):
        """检测状态是否发生变化，并更新记录。

        Returns:
            tuple: (是否变化, 当前电平)
        """
        current = self.read_state()
        changed = current != self._last_state
        if changed:
            if current == self._trigger_level:
                self._trigger_count += 1
            if self._callback:
                self._callback(current == self._trigger_level)
        self._last_state = current
        return changed, current

    @property
    def trigger_count(self):
        """获取累计触发次数。"""
        return self._trigger_count

    def reset_count(self):
        """重置触发计数归零。"""
        self._trigger_count = 0

    def wait_for_trigger(self, timeout_ms=None):
        """阻塞等待磁场触发，可选超时。

        Args:
            timeout_ms: 超时时间 ms，None 无限等待

        Returns:
            bool: True=触发, False=超时
        """
        start = utime.ticks_ms()
        while True:
            changed, state = self.check_state_change()
            if changed and state == self._trigger_level:
                return True
            if timeout_ms is not None:
                if utime.ticks_diff(utime.ticks_ms(), start) >= timeout_ms:
                    return False
            utime.sleep_ms(10)

    def monitor(self, interval_sec=1):
        """轮询监控循环，检测并输出磁场状态变化。

        Args:
            interval_sec: 轮询间隔，单位秒，默认 1s
        """
        while True:
            changed, state = self.check_state_change()
            if changed:
                if state == self._trigger_level:
                    print("[ReedSwitch] 触发：检测到磁场变化")
                else:
                    print("[ReedSwitch] 释放：磁场恢复正常")
            utime.sleep(interval_sec)


if __name__ == "__main__":
    sensor = ReedSwitch(pin=Pin.GPIO31, trigger_level=0, pull=Pin.PULL_PU)
    sensor.monitor(interval_sec=1)
```

