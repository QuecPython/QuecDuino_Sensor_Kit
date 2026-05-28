# Water Level Detection Module

## 1. Module Introduction

The water level monitoring module is a **resistive liquid detection sensor**, which is used in scenarios such as detecting water level height, presence or absence of water, and water leakage alarm; it detects liquid level changes through conductive probes and outputs analog signals, with advantages such as **fast response, small size, 3.3V compatibility, direct connection to ADC, and long service life**.

**Working Principle:**

The Water Sensor can monitor the water level. This module mainly utilizes the current amplification principle of transistors: when the liquid level height makes the base of the transistor conduct with the positive pole of the power supply, a certain amount of current is generated between the base and emitter of the transistor, and at this time, a current with a certain amplification factor is generated between the collector and emitter of the transistor. This current generates a characteristic voltage through the resistor at the emitter, which is collected by the AD converter.

## 2. Connection Example

Connect the peripherals to the development board one by one according to the table and picture instructions

| Peripheral | Development Board |
| ---------- | ----------------- |
| Module (+) | 3.3V              |
| Module (-) | GND               |
| Module (S) | A1（ADC1）        |

![](../../media/water1.png)

## 3.Driver Code

```python
def fun():

  while True:

     num=adc.read(adc.ADC1)

     utime.sleep(1)

     print(num)



if name=='main':

  adc = ADC()

  adc.open()

  _thread.start_new_thread(fun,())
```

 