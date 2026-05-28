### Nixie Tube Module

#### 1. Module Introduction

The single-digit nixie tube module is a **digital display device** composed of 7-segment light-emitting diodes, used to display 0-9 digits and simple symbols. It is widely used in counting, timing, status display, and maker DIY scenarios. It features high brightness, clear display, 3.3V/5V compatibility, simple driving, and long service life.

**Composition**:

7-segment LED light-emitting segments, common terminal, decimal point, current-limiting resistor, PCB board, wiring terminal.

**Working Principle**:

The module has a positive electrode, a negative electrode, and a segment selection signal terminal. By controlling the on/off of different segments, it combines to display 0-9 digits, and the development board controls the corresponding segments to light up by outputting levels through GPIO.

#### 2. Connection Example

Connect the peripheral to the development board one-to-one according to the table and picture instructions:

| Peripheral | Development Board |
| ---------- | ----------------- |
| LED（+）   | 3.3V              |
| LED（-）   | GND               |
| LED（S）   | Optional          |

![](../../media/display1.png)

## 三、 驱动代码

```
/# Initialize GPIO for each segment of the nixie tube
seg32 = Pin(Pin.GPIO32, Pin.OUT, Pin.PULL_DISABLE, 1)  # Bottom right (a)
seg31 = Pin(Pin.GPIO31, Pin.OUT, Pin.PULL_DISABLE, 1)  # Top (b)
seg30 = Pin(Pin.GPIO30, Pin.OUT, Pin.PULL_DISABLE, 1)  # Top right (c)
seg33 = Pin(Pin.GPIO33, Pin.OUT, Pin.PULL_DISABLE, 1)  # Bottom (d)
seg2 = Pin(Pin.GPIO2,  Pin.OUT, Pin.PULL_DISABLE, 1)  # Middle (e)
seg3 = Pin(Pin.GPIO3,  Pin.OUT, Pin.PULL_DISABLE, 1)  # Decimal point (f)
seg14 = Pin(Pin.GPIO14, Pin.OUT, Pin.PULL_DISABLE, 1)  # Bottom left (g)
seg15 = Pin(Pin.GPIO15, Pin.OUT, Pin.PULL_DISABLE, 1)  # Top left (h)

/# Segment code table: on/off of each segment corresponding to 0~9 (0=on, 1=off)
/# Order: a b c d e f g h
num_table = [
  [0,0,0,0,1,0,0,0],  # 0
  [0,1,0,1,1,0,1,1],  # 1
  [1,0,0,0,0,0,0,1],  # 2
  [0,0,0,0,0,0,1,1],  # 3
  [0,1,0,1,0,0,1,0],  # 4
  [0,0,1,0,0,0,1,0],  # 5
  [0,0,1,0,0,0,0,0],  # 6
  [0,0,0,1,1,0,1,1],  # 7
  [0,0,0,0,0,0,0,0],  # 8
  [0,0,0,0,0,0,1,0],  # 9
]

def display_num(n):
  if n < 0 or n > 9:
    return
  val = num_table[n]
  seg32.write(val[0])
  seg31.write(val[1])
  seg30.write(val[2])
  seg33.write(val[3])
  seg2.write(val[4])
  seg3.write(val[5])
  seg14.write(val[6])
  seg15.write(val[7])

/# Cycle display 0-9
while True:
  for i in range(10):
    display_num(i)
    utime.sleep(1)
```

