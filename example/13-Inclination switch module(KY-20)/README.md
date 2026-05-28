# Tilt Switch Module

## 1. Module Introduction

The tilt switch is a **posture-sensing digital switch device**, also known as a ball switch or topple sensor. It is commonly used in tilt detection, anti-toppling protection, posture triggering, and intelligent alarm scenarios. It can automatically switch level signals when the module is tilted to a certain angle. It has the advantages of small size, no contacts, low power consumption, 3.3V/5V compatibility, direct GPIO detection, sensitive response, and long service life.

**Working Principle**:

The module has a positive electrode, a negative electrode, and a signal terminal. When tilted, the internal ball/conductive liquid moves, turning the internal contacts on or off to output high/low levels. The development board can directly read the state to determine whether it is tilted.

## 2. Connection Example

Connect the peripheral to the development board one-to-one according to the table and picture instructions:

| Peripheral  | Development Board |
| ----------- | ----------------- |
| Module（+） | 3.3V              |
| Module（-） | GND               |
| Module（S） | PIN4(GPIO31)      |

![](../../media/lnclination1.png)

## 3.Driver Code

```python
/# 配置GPIO为输入，上拉

gpio = Pin(Pin.GPIO31, Pin.IN, Pin.PULL_PU)

def main():

  /# 假设传感器检测到触摸时输出低电平（0）

  while True:

     if gpio.read() == 0:

       print("检测到倾斜")

     else:

       print("水平状态")

     utime.sleep(1)

if name == 'main':

  main()
```

