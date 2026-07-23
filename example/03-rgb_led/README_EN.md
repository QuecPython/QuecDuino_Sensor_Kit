# LED Module

## 1. Module Introduction

The tricolor RGBLED is a **full-color light-emitting diode module**, which consists of three chips (red, green, and blue) packaged together. It can mix any color by adjusting brightness through PWM (Pulse Width Modulation), and is widely used in ambient lights, status indicators, interactive prompts, maker DIY scenarios. It can achieve effects such as seven-color gradient, breathing, and flashing, with advantages including small size, high brightness, 3.3V/5V compatibility, simple driving, and long service life.

**Light-emitting Principle**:

The LED pins share a common ground. The LED lights up when a voltage difference is formed between the positive and negative poles, so a high level turns on the LED.

## 2. Connection Example

Connect the peripheral to the development board one by one according to the guidance of the table and picture.

| Peripheral | Development Board |
| ---------- | ----------------- |
| LED（-）   | GND               |
| LED（R）   | PIN4（GPIO31）    |
| LED（G）   | PIN5（GPIO30）    |
| LED（B）   | PIN6（GPIO32）    |

![](../../media/led4.png)

## 3.Driver Code

```python
from machine import Pin
import utime


class RGBLED(object):
    """RGB LED control class, mixes colors via three GPIO pins (R, G, B).

    Supports different hardware via active_level:
        - active_level=0: common-anode (low to light, default)
        - active_level=1: common-cathode (high to light)

    Example:
        rgb = RGBLED(Pin.GPIO32, Pin.GPIO30, Pin.GPIO31, active_level=1)
        rgb.set_color_by_name("red")
        rgb.blink(colors=["red", "blue"], interval=0.5, times=3)

    Args:
        red_pin:     Red channel GPIO pin (Pin object)
        green_pin:   Green channel GPIO pin (Pin object)
        blue_pin:    Blue channel GPIO pin (Pin object)
        active_level: level to light, 0=low-active, 1=high-active, default 0
    """

    # Color name -> RGB logical values (1=on, 0=off, decoupled from hardware level)
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
        self._state = (0, 0, 0)

    def set_color(self, r, g, b):
        """Set RGB channel logical state (1=on, 0=off).

        Args:
            r: red channel, 1=on, 0=off
            g: green channel, 1=on, 0=off
            b: blue channel, 1=on, 0=off
        """
        self._state = (r, g, b)
        self.red.write(self._active if r else self._inactive)
        self.green.write(self._active if g else self._inactive)
        self.blue.write(self._active if b else self._inactive)

    def set_color_by_name(self, name):
        """Set LED color by name (case-insensitive).

        Supported: red, green, blue, yellow, purple, cyan, white, off

        Args:
            name: color name string

        Returns:
            bool: True on success, False for unknown color
        """
        name = name.lower()
        if name in self.COLOR_MAP:
            self.set_color(*self.COLOR_MAP[name])
            return True
        return False

    def off(self):
        """Turn off all channels."""
        self.set_color(0, 0, 0)

    def read(self):
        """Get current RGB logical state.

        Returns:
            tuple: (r, g, b), 1=on, 0=off
        """
        return self._state

    def blink(self, colors=None, interval=0.5, times=None):
        """Multi-color blink, cycles through the given color list.

        Args:
            colors:   list of color names, default ["red", "green", "blue"]
            interval: switch interval in seconds, default 0.5s
            times:    number of full cycles, None for infinite
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
        """Demo loop, cycles through all preset colors.

        Args:
            interval: switch interval in seconds, default 1s
        """
        color_names = list(self.COLOR_MAP.keys())
        while True:
            for color in color_names:
                self.set_color_by_name(color)
                print("LED color set to {}".format(color))
                utime.sleep(interval)


if __name__ == "__main__":
    rgb_led = RGBLED(
        red_pin=Pin(Pin.GPIO32, Pin.OUT, Pin.PULL_DISABLE, 0),
        green_pin=Pin(Pin.GPIO30, Pin.OUT, Pin.PULL_DISABLE, 0),
        blue_pin=Pin(Pin.GPIO31, Pin.OUT, Pin.PULL_DISABLE, 0),
        active_level=0,
    )
    rgb_led.demo(interval=1)
```

