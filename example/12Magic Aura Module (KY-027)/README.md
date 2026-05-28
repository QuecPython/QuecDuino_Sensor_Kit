# Magic Halo Module

## 1. Module Introduction

The Magic Halo Module (KY‑027) is a 2-in-1 digital module integrating **tilt sensing + LED lighting**, with a built-in mercury switch and high-brightness LED. It is used for tilt detection, posture triggering, status indication, and maker interaction projects. The module features small size, fast response, digital level output, 3.3V/5V compatibility, direct GPIO driving, and stable service life.

**Working Principle**:

![](../../media/magic1.png)

The module has power supply, ground, signal output, and LED control terminals. When tilted to a certain angle, the mercury switch is turned on/off to output high/low level; the LED can be controlled to turn on/off via GPIO to achieve effects such as tilt lighting and posture alarm.

## 2. Connection Example

Connect the peripheral to the development board one-to-one according to the table and picture instructions:

| Peripheral  | Development Board |
| ----------- | ----------------- |
| Module（+） | 3.3V              |
| Module（-） | GND               |
| Module（S） | PIN4(GPIO31)      |
| Module（L） | PIN5(GPIO30)      |

![](../../media/magic2.png)

## 3.Driver Code

```python
/# Configure GPIO as input with pull-up
gpio = Pin(Pin.GPIO31, Pin.IN, Pin.PULL_PU)
gpio1 = Pin(Pin.GPIO30, Pin.OUT, Pin.PULL_DISABLE, 0)

def main():
  /# Assume the sensor outputs high level (1) when tilt is detected
  while True:
     if gpio.read() == 1:
       print("Mercury switch detects tilt")
       gpio1.write(1)
     else:
       print("Mercury switch does not detect tilt")
       gpio1.write(0)
     utime.sleep(1)

if __name__ == '__main__':
  main()
```

 