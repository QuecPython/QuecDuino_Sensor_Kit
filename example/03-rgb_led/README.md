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
R_PIN = 32

G_PIN = 30

B_PIN = 31

 

r = Pin(Pin.GPIO32, Pin.OUT,Pin.PULL_DISABLE, 0)

g = Pin(Pin.GPIO30, Pin.OUT,Pin.PULL_DISABLE, 0)

b = Pin(Pin.GPIO31, Pin.OUT,Pin.PULL_DISABLE, 0)

 

def set_color(red, green, blue):

  r.write(red)

  g.write(green)

  b.write(blue)

# Display multiple light colors through permutation and combination

while True:

  set_color(1, 0, 0)  # 红色

  utime.sleep(1)

  set_color(0, 1, 0)  # 绿色

  utime.sleep(1)

  set_color(0, 0, 1)  # 蓝色

  utime.sleep(1)

  set_color(1, 1, 0)  # 黄色

  utime.sleep(1)

  set_color(1, 0, 1)  # 紫色

  utime.sleep(1)  

  set_color(0, 1, 1)  # 青色

  utime.sleep(1)

  set_color(1, 1, 1)  # 白色

  utime.sleep(1)

 
```

