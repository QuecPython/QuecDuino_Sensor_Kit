# Ultrasonic Module

## 1. Module Introduction

The working process of HC-SR04 is initiated by a "trigger signal" and feeds back the distance through an "echo signal", with the specific steps as follows:

- Trigger ranging: STM32 outputs a high-level signal of at least 10μs to the Trig pin (high-precision delay is required, which has been implemented in the author's timer notes, please review);
- The module automatically transmits/receives ultrasonic waves: After the Trig receives the trigger signal, the module will automatically send 8 40kHz square waves and start detecting whether the ultrasonic waves are reflected back;
- Echo signal feedback: If the ultrasonic waves are reflected back, the module will output a high level through the Echo pin —— the duration of the high level = the total time for the ultrasonic waves to "transmit to return";
- Distance calculation: Derived from the "time-distance" formula, the final distance = (Echo high-level duration × speed of sound) / 2.

(Note: The speed of sound is 340m/s, divided by 2 because the ultrasonic waves need to "transmit→reflect→return", traveling twice the distance.)

**Core Parameters**:

- Working voltage: **3.3V–5V**
- Measuring range: **2cm–450cm**
- Resolution: 1mm
- Measuring angle: about 15°
- Output mode: **GPIO / I2C / UART**
- Features: non-contact, high precision, fast response, not affected by light and color

​	**schematic diagram**

![](../../media/hc1.png)

​	**sequence chart**

![](../../media/hc2.png)

 

## 2. Connection Example

Connect the peripheral to the development board one-to-one according to the table and picture instructions:

| **外设**           | **模块**     |
| ------------------ | ------------ |
| Ultrasonic（+）    | VCC(5V)      |
| Ultrasonic（Trig） | Pin5(GPIO30) |
| Ultrasonic（Echo） | Pin4(GPIO31) |
| Ultrasonic（-）    | GND          |

![](../../media/hc3.png)

## **三、** **驱动代码**

```python
from machine import Pin
import utime

/# Pin definition (modify according to actual wiring)
TRIG_PIN = Pin.GPIO30  # Trigger pin
ECHO_PIN = Pin.GPIO31  # Echo pin

/# Initialize pins
trig = Pin(TRIG_PIN, Pin.OUT, Pin.PULL_DISABLE, 0)
echo = Pin(ECHO_PIN, Pin.IN, Pin.PULL_DISABLE, 0)

def measure_distance():
  /# Send a high-level trigger signal for more than 10us
  trig.write(0)
  utime.sleep_us(2)
  trig.write(1)
  utime.sleep_us(10)
  trig.write(0)

  /# Wait for the ECHO pin to go high (start timing)
  timeout = utime.ticks_ms() + 200  # Timeout 200ms
  while echo.read() == 0:
     if utime.ticks_ms() > timeout:
       return -1  # Timeout, measurement failed
  start_time = utime.ticks_us()
  
  /# Wait for the ECHO pin to go low (end timing)
  while echo.read() == 1:
     if utime.ticks_ms() > timeout:
       return -1  # Timeout, measurement failed

  end_time = utime.ticks_us()

  /# Calculate distance (speed of sound = 340m/s = 0.034cm/us, divided by 2 for round trip)
  pulse_duration = end_time - start_time
  distance = (pulse_duration * 0.034) / 2

  return round(distance, 2)

if __name__ == "__main__":
  print("RCWL-9206 Ultrasonic Ranging Module Test (GPIO Mode)")
  print("Measurement interval >200ms to avoid interference")
  while True:
     dist = measure_distance()
     if dist == -1:
       print("Measurement timeout/failed")
     else:
       print("Current distance: {} cm".format(dist))
     utime.sleep(0.2)  # Interval between two measurements ≥200ms
```

