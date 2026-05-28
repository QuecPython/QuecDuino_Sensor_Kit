# Photosensitive Resistor Module

## 1. Module Introduction

The photosensitive resistor sensor is a type of sensor that can convert optical signals into electrical signals, and its resistance value changes with the intensity of light. In many practical applications, such as automatic lighting systems, ambient light detection, etc., the photosensitive resistor sensor plays an important role. The EG800Z Duino development board is equipped with rich peripheral resources, which can be easily combined with the photosensitive resistor sensor to realize the detection and processing of light intensity.

Photosensitive resistors are usually made of semiconductor materials, and their working principle is based on the internal photoelectric effect. When light irradiates the photosensitive resistor, electrons in the semiconductor material absorb the energy of photons and transition from the valence band to the conduction band, thereby enhancing the conductivity of the material and reducing the resistance value. Conversely, when the light intensity weakens, the resistance value increases.

The characteristic curve of a photosensitive resistor usually shows a non-linear relationship, that is, the relationship between light intensity and resistance value is not a simple linear proportional relationship. In practical applications, calibration and processing need to be carried out according to specific requirements and characteristic curves.

**Composition of Photosensitive Resistor:**

![](../../media/light1.png)

Working Principle:

![](../../media/light2.png)

**The stronger the light, the smaller the resistance and the lower the voltage; the weaker the light, the larger the resistance and the higher the voltage.**

## 2. Connection Example

Connect the peripherals to the development board one by one according to the table and picture instructions

| Peripheral | Development Board |
| ---------- | ----------------- |
| LDR（+）   | 3.3V              |
| LDR（-）   | GND               |
| LDR（S）   | A1（ADC1）        |

![](../../media/light3.png)

## 三、 驱动代码

```python
def fun():

  while True:

     num=adc.read(adc.ADC1)

     utime.sleep(1)#出现具体电压值，通过电压值控制占空比

     print(num)

     return num

def LED_SW(num):

  if num<50:

     LED.write(1)

     print("光线较强")

  else:

     LED.write(0)

     print("光线较弱")

if name=='main':

  LED=Pin(Pin.GPIO31,Pin.OUT,Pin.PULL_DISABLE,0)

  adc = ADC()

  adc.open()

  _thread.start_new_thread(fun,())

  while True:

     num=fun()     

     LED_SW(num)
```

