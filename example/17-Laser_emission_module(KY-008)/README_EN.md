# Laser Emission Module

## 1. Module Introduction

The core principle of the **Laser Emitter Module** is: **converting electrical energy into high-brightness, high-directionality, monochromatic coherent light (laser) efficiently through a semiconductor laser diode (LD), then emitting it after collimation/shaping by an optical system**. It is widely used in laser ranging, laser radar, optical fiber communication, laser indication, infrared night vision and other scenarios.

## 2. Connection Example

Connect the peripheral to the development board one-to-one according to the table and picture instructions:

| Peripheral  | Development Board |
| ----------- | ----------------- |
| Module（+） | 3.3V              |
| Module（-） | GND               |
| Module（S） | PIN4(GPIO31)      |

![](../../media/laser1.png)

## 3. Driver Code

```python
from machine import Pin
import utime


class LaserEmitter(object):
    """Laser emitter control class, controls laser on/off and blinking via GPIO.

    Adapts to different trigger modes via active_level.

    Example:
        laser = LaserEmitter(pin=Pin.GPIO31)
        laser.on()
        laser.blink(interval=0.5, times=3)

    Args:
        pin:          GPIO pin number, default GPIO31
        active_level: 1=high-active, 0=low-active, default 1
    """

    def __init__(self, pin=Pin.GPIO31, active_level=1):
        self._active_level = active_level
        self._inactive_level = 0 if active_level else 1
        self._gpio = Pin(pin, Pin.OUT, Pin.PULL_DISABLE, self._inactive_level)
        self._state = 0

    def on(self):
        """Turn on the laser."""
        self._state = 1
        self._gpio.write(self._active_level)

    def off(self):
        """Turn off the laser."""
        self._state = 0
        self._gpio.write(self._inactive_level)

    def toggle(self):
        """Toggle laser state (on->off, off->on)."""
        self.off() if self._state else self.on()

    def is_on(self):
        """Check if laser is on."""
        return self._state == 1

    def read(self):
        """Read logical state (1=on, 0=off)."""
        return self._state

    def blink(self, interval=0.5, times=None):
        """Blink the laser.

        Args:
            interval: half-cycle duration in seconds, default 0.5s
            times:    number of blink cycles, None for infinite
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

