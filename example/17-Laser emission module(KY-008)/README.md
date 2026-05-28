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

```
from machine import Pin

/# Create GPIO object
gpio1 = Pin(Pin.GPIO31, Pin.OUT, Pin.PULL_DISABLE, 1)

/# Set pin level
gpio1.write(1)
```

