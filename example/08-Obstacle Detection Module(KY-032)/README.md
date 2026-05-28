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
gpio = Pin(Pin.GPIO31, Pin.IN, Pin.PULL_DISABLE)

def main():

  # Assume the sensor outputs high level (1) when tilt is detected

  while True:

     if gpio.read() == 1:

       print("No obstacle detected")

     else:

       print("Obstacle detected")

     utime.sleep(1)

if name == 'main':

  main()


```

 