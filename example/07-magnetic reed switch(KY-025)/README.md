# KY-025 Reed Switch Sensor Module Introduction

The KY-025 is a magnetic control sensor module based on the principle of **Reed Switch (also known as Reed Pipe)**. It is essentially a miniature electrical switch controlled by a magnetic field. When a magnet approaches, the internal metal reed will close to conduct the circuit; when the magnet moves away, the reed will automatically bounce open to disconnect the circuit.

Due to its simple structure, high sensitivity and trigger without direct contact, the KY-025 is often used as a non-contact proximity detection or position limit device in various IoT projects.

![](../../media/reed1.png)

### Core Features

- **Dual signal output**: The module provides both digital (DO) and analog (AO) output interfaces, which can not only make simple switch judgments, but also perceive the relative change of magnetic field intensity.
- **Adjustable sensitivity**: The onboard precision potentiometer (trim knob) can rotate to adjust the detection distance and trigger sensitivity of the sensor according to the actual application scenario.
- **Intuitive working indication**: Equipped with power indicator light and working status LED. When the magnetic field trigger is detected, the onboard LED will light up, which is convenient for debugging and observation.
- **Wide voltage compatibility**: It usually supports wide voltage power supply from 3.3V to 5V, and can perfectly adapt to various mainstream single-chip microcomputer development boards such as Arduino, STM32 and QuecDuino in your hand.

### Pin Description and Wiring

The KY-025 module usually leads out 4 standard pins, and the specific definitions are as follows:

| Pin Name    | Function Description  | Wiring Suggestion                                            |
| :---------- | :-------------------- | :----------------------------------------------------------- |
| **+ (VCC)** | Positive power supply | Connect to 3.3V or 5V of the development board               |
| **G (GND)** | Negative power supply | Connect to GND of the development board                      |
| **D0**      | Digital signal output | Connect to ordinary GPIO of the development board (such as pin 4) |
| **A0**      | Analog signal output  | Connect to ADC pin of the development board (such as A0)     |

### Detailed Working Principle

1. **Digital Output (D0)**: This is a switch signal. After adjusting the sensitivity, once a magnet enters the effective detection range, pin 4 will output a high level (or low level, depending on the specific circuit design), and the onboard LED will light up at the same time; it will return to the original state after the magnet is removed. This is very suitable for making "door magnetic alarm" or "in-position detection".
2. **Analog Output (A0)**: The voltage value output by this pin will change linearly with the change of magnetic field intensity. Usually, a higher value is output when there is no magnetic field, and the output voltage will gradually decrease as the magnet approaches. By reading this analog value, you can roughly judge the distance between the magnet and the sensor.

### Common Application Scenarios

- **Door and window anti-theft alarm**: Install the module on the door frame and the magnet on the door leaf, and the alarm will be triggered when the door is opened.
- **Intelligent counting and speed measurement**: Install a magnet on the fan blade or rotating object, which is triggered once per revolution, so as to calculate the speed or accumulate the number of times.
- **Position limit detection**: Used on robotic arms or mobile trolleys to detect whether the preset physical boundary is reached.
- **Contactless switch**: As a trigger for opening the cover to turn on the light of jewelry boxes and gift boxes, it is both hidden and durable.

### Driver Code

Please refer to `example/07-Reed Switch (KY-025)/gpio.py` and `example/07-Reed Switch (KY-025)/adc.py` for the driver code, which can be run after importing the module.