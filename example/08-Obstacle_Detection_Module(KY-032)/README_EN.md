# Obstacle Detection Module

## 1. Module Introduction

The obstacle detection module is an infrared reflective digital detection device, also known as an infrared obstacle avoidance module, which is used for short-distance obstacle detection, tracking, obstacle avoidance, and limit triggering; it judges whether there is an obstacle in front through infrared emission and reception, with advantages such as fast response, small size, 3.3V/5V compatibility, direct GPIO reading, strong anti-interference, and long service life.

**Module Composition:**

![](../../media/obstacle1.png)

**Working Principle:**

The working principle is that the infrared light emitting tube **emits infrared light**, and the infrared light receiving tube **receives infrared light**. When **no reflected infrared light is received**, the OUT pin outputs **high level**; when **reflected infrared light is received**, the OUT pin outputs **low level**.

## 2. Connection Example

Connect the peripherals to the development board one by one according to the table and picture instructions

| Peripheral  | Development Board |
| ----------- | ----------------- |
| Module（+） | 3.3V              |
| Module（-） | GND               |
| Module（S） | PIN4(GPIO31)      |

![](../../media/obstacle2.png)

## 3.Driver Code

```python
from machine import Pin, ExtInt
import utime


class ObstacleSensor(object):
    """Infrared obstacle avoidance sensor class (KY-032), supports polling and interrupt modes.

    Sensor output logic:
        - No obstacle: OUT outputs low level (0)
        - Obstacle detected: OUT outputs high level (1)

    Example:
        sensor = ObstacleSensor(pin=Pin.GPIO31)
        sensor.set_callback(lambda: print("obstacle!"))
        sensor.monitor_polling(interval_ms=200)

    Args:
        pin:  GPIO pin number, default GPIO31
        pull: pull-up/down config, default pull-up (Pin.PULL_PU)
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
        """Set obstacle detection callback.

        Args:
            callback: function with no arguments, pass None to clear
        """
        self._callback = callback

    def read_state(self):
        """Read current sensor state.

        Returns:
            int: 0=clear, 1=obstacle
        """
        return self._gpio.read()

    def is_obstacle(self):
        """Check if obstacle is currently detected.

        Returns:
            bool: True if obstacle detected
        """
        return self.read_state() == 1

    def _irq_handler(self, args):
        """Interrupt callback, sets flag when obstacle detected."""
        if self._gpio.read() == 1:
            self._obstacle_flag = True

    @property
    def trigger_count(self):
        """Get cumulative trigger count."""
        return self._trigger_count

    def reset_count(self):
        """Reset trigger count to zero."""
        self._trigger_count = 0

    def wait_for_obstacle(self, timeout_ms=None):
        """Block and wait for obstacle.

        Args:
            timeout_ms: timeout in ms, None for infinite

        Returns:
            bool: True=obstacle, False=timeout
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
        """Block and wait for obstacle to clear.

        Args:
            timeout_ms: timeout in ms, None for infinite

        Returns:
            bool: True=cleared, False=timeout
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
        """Polling mode: continuously reads sensor state.

        Args:
            interval_ms: polling interval in ms, default 200
        """
        print("[ObstacleSensor] Polling mode started")
        while True:
            if self._gpio.read() == 0:
                print("No obstacle")
            else:
                self._trigger_count += 1
                print("Obstacle detected")
                if self._callback:
                    self._callback()
            utime.sleep_ms(interval_ms)

    def monitor_interrupt(self, interval_ms=200):
        """Interrupt mode: obstacle triggers interrupt, main loop checks flag.

        Args:
            interval_ms: check interval in ms, default 200
        """
        self._extint = ExtInt(self._gpio, ExtInt.IRQ_FALLING, ExtInt.PULL_PU, self._irq_handler)
        self._extint.enable()
        print("[ObstacleSensor] Interrupt mode started")
        while True:
            if self._obstacle_flag:
                self._trigger_count += 1
                print("Obstacle detected")
                self._obstacle_flag = False
                if self._callback:
                    self._callback()
            utime.sleep_ms(interval_ms)


if __name__ == '__main__':
    sensor = ObstacleSensor(pin=Pin.GPIO31)
    sensor.monitor_polling(interval_ms=200)
```

 