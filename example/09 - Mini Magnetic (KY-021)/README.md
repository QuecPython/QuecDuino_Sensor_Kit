# Mini Reed Module

## 1. Module Introduction

The mini reed, full name **Mini Reed Switch (Reed Pipe Module)**, is a passive switch component whose on-off is controlled by a magnetic field. This type of magnetic induction device is generally used for door magnetic detection, position detection, and limit triggering, and is currently widely used in embedded devices, smart hardware, and maker DIY scenarios; it can conduct when a magnetic field approaches and disconnect when the magnetic field moves away, with advantages such as small size, fast response, no mechanical contact wear, low power consumption, plug-and-play, adaptation to 3.3V/5V low-voltage environment, direct connection to GPIO detection, and long service life.

Composition of Mini Reed Module:

![](../../media/mini1.png)

**Working Principle:**

The module is essentially a switch controlled by a magnetic field. When a magnet approaches the module, the reed in the glass tube is magnetized and attracted to each other to contact, and the circuit is conducted; when the magnet moves away, the reed loses its magnetism and separates by elasticity, and the circuit is disconnected, so as to realize the switch signal output triggered by the magnetic field.

## 2. Connection Example

Connect the peripherals to the development board one by one according to the table and picture instructions

| Peripheral  | Development Board |
| ----------- | ----------------- |
| Module（+） | 3.3V              |
| Module（-） | GND               |
| Module（S） | PIN4(GPIO31)      |

![](../../media/mini2.png)

## 3.Driver Code

```python
# Configure GPIO as input, pull-up
gpio = Pin(Pin.GPIO31, Pin.IN, Pin.PULL_PU)
gpio1=Pin(Pin.GPIO30,Pin.OUT,Pin.PULL_DISABLE,0)

def main():
  # Assume the sensor outputs high level (1) when tilt is detected
  while True:
      if gpio.read() == 0:
        print("Magnetic field change detected")
        gpio1.write(1)
      else:
        print("No magnetic field change detected")
        gpio1.write(0)
      utime.sleep(1)

if __name__ == '__main__':
  main()
```

