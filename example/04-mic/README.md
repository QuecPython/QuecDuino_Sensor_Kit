# Microphone Module

## 1. Module Introduction

A microphone is short for an **acoustic-electric conversion device**, also known as a sound detection sensor module. It can detect the sound intensity in the surrounding environment and convert it into an electrical signal for output. It contains a built-in microphone that can capture sound signals. The sensitivity of the module to sound can be adjusted by tuning the sensitivity potentiometer on the module. It supports analog output mode, meeting the requirements of most applications and design needs.

## 2. Connection Example

Connect the peripheral to the development board one-to-one according to the guidance of the table and picture.

| Peripheral | Development Board |
| ---------- | ----------------- |
| MIC（+）   | 3.3V              |
| MIC（-）   | GND               |
| MIC（S）   | A1(ADC1)          |

![](C:/Users/Aaron.chen/Desktop/QuecDuion套件相关资料/QuecDuino_Sensor_Kit/media/mic1.png) 



## 3.Driver Code

```python
def fun():

  while True:

     num=adc.read(adc.ADC1)

     utime.sleep(1) # Specific voltage value appears, control the duty cycle through the voltage value

     print(num)



if name=='main':

  LED=Pin(1,Pin.OUT,Pin.PULL_DISABLE,0)

  adc = ADC()

  adc.open()

  _thread.start_new_thread(fun,())
```

 