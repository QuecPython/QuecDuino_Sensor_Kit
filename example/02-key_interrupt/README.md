# Key Module

## 1. Module Introduction

The key module is the **most basic digital input module**, which realizes on-off control through a tactile switch and outputs high/low level signals. It is essential for embedded/IoT projects, enabling functions such as **human-computer interaction, switch control, command triggering, counting, and mode switching**.

### 1.1 Core Parameters

- Type: Tactile key (mechanical type)
- Power supply: 3.3V – 5V
- Output: **Digital signal (high/low level)**
- Pins: 3 pins (VCC, GND, SIG)
- Default state: **High level (not pressed)**
- Trigger state: **Low level (pressed)**
- Built-in: Pull-up resistor, signal indicator light

### 1.2 Schematic Diagram

![](../../media/key1.png)

Both VCC and the resistor are integrated inside the chip. When the key is disconnected, the current flowing through the resistor is called sink current (about tens of milliamps), so the pin is at a high level at this time. When the key is pressed, it is connected to the ground and becomes a low level.

## 2. Connection Example

Connect the peripheral device to the development board one by one according to the table and image instructions.

| Peripheral   | Module       |
| ------------ | ------------ |
| **KEY（+）** | 3.3V         |
| **KEY（-）** | GND          |
| **KEY（S）** | PIN4(GPIO31) |

![](../../media/key2.png)

## 3.Driver Code

```python
from machine import ExtInt

/# args[0]:gpio号 args[1]:上升沿或下降沿

def fun(args): 

      print(“Key pressed”)

extint = ExtInt(ExtInt.GPIO31,ExtInt.IRQ_FALLING,ExtInt.PULL_PU,fun)

/#中断使能

extint.enable()
```

 