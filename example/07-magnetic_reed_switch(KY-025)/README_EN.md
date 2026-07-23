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

#### ADC Mode (Analog magnetic field intensity)

```python
from misc import ADC
from machine import Pin
import _thread
import utime


class MagneticReedSwitch(object):
    """Magnetic reed switch sensor class (ADC mode), reads magnetic field intensity via analog signal.

    Example:
        sensor = MagneticReedSwitch(led_pin=Pin.GPIO31, threshold=900)
        sensor.set_callback(lambda val: print("magnet!", val))
        sensor.start()

    Args:
        adc_channel: ADC channel, default ADC1
        led_pin:     LED indicator GPIO pin, default GPIO31, pass None to disable
        threshold:   magnetic field detection threshold, below this value = detected, default 900
        led_on_ms:   LED on duration in ms, default 500 (non-blocking)
    """

    def __init__(self, adc_channel=None, led_pin=Pin.GPIO31,
                 threshold=900, led_on_ms=500):
        self._threshold = threshold
        self._led_on_ms = led_on_ms
        self._led = None
        if led_pin is not None:
            self._led = Pin(led_pin, Pin.OUT, Pin.PULL_DISABLE, 0)
        self._adc = ADC()
        self._adc_channel = self._adc.ADC1 if adc_channel is None else adc_channel
        self._callback = None
        self._is_running = False
        self._last_value = 0
        self._led_off_at = 0

    def set_callback(self, callback):
        """Set magnetic field detection callback.

        Args:
            callback: function with signature callback(adc_value)
        """
        self._callback = callback

    @property
    def threshold(self):
        return self._threshold

    @threshold.setter
    def threshold(self, value):
        self._threshold = value

    def read_value(self):
        """Read current magnetic field ADC value.

        Returns:
            int: ADC reading
        """
        self._last_value = self._adc.read(self._adc_channel)
        return self._last_value

    def is_detected(self):
        """Check if magnetic field was detected in last sample.

        Returns:
            bool: True if detected
        """
        return self._last_value < self._threshold

    def _led_on(self):
        if self._led is not None:
            self._led.write(1)
            self._led_off_at = utime.ticks_ms() + self._led_on_ms

    def _led_tick(self):
        if self._led is not None and self._led_off_at > 0:
            if utime.ticks_diff(utime.ticks_ms(), self._led_off_at) >= 0:
                self._led.write(0)
                self._led_off_at = 0

    def _monitor(self):
        """Background monitoring loop, non-blocking sampling."""
        while self._is_running:
            value = self.read_value()
            detected = value < self._threshold
            print("ADC: {} | Status: {}".format(value, "Magnetic field detected" if detected else "No magnetic field"))

            if detected:
                self._led_on()
                if self._callback:
                    self._callback(value)

            self._led_tick()
            utime.sleep_ms(500)

    def start(self):
        """Open ADC and start background monitoring thread."""
        self._adc.open()
        self._is_running = True
        _thread.start_new_thread(self._monitor, ())

    def stop(self):
        """Stop monitoring thread and turn off LED."""
        self._is_running = False
        if self._led is not None:
            self._led.write(0)


if __name__ == '__main__':
    def on_magnet(value):
        print("Magnetic field detected! ADC = {}".format(value))

    sensor = MagneticReedSwitch(led_pin=Pin.GPIO31, threshold=900)
    sensor.set_callback(on_magnet)
    sensor.start()

    while True:
        utime.sleep_ms(1000)
```

#### GPIO Mode (Digital switch state detection)

```python
from machine import Pin
import utime


class ReedSwitch(object):
    """Reed switch sensor class (GPIO mode), detects magnetic field state changes via digital signal.

    Example:
        sensor = ReedSwitch(pin=Pin.GPIO31, trigger_level=0, pull=Pin.PULL_PU)
        sensor.set_callback(lambda triggered: print("triggered!" if triggered else "released"))
        sensor.monitor(interval_sec=1)

    Args:
        pin:           GPIO pin number, default GPIO31
        trigger_level: trigger level, 0=low-trigger, 1=high-trigger, default 0
        pull:          pull-up/down config, default pull-up (Pin.PULL_PU)
    """

    def __init__(self, pin=Pin.GPIO31, trigger_level=0, pull=Pin.PULL_PU):
        self._gpio = Pin(pin, Pin.IN, pull)
        self._trigger_level = trigger_level
        self._last_state = self._gpio.read()
        self._callback = None
        self._trigger_count = 0

    def set_callback(self, callback):
        """Set state change callback.

        Args:
            callback: function with signature callback(is_triggered)
        """
        self._callback = callback

    def read_state(self):
        """Read current GPIO level state.

        Returns:
            int: 0 or 1
        """
        return self._gpio.read()

    def is_triggered(self):
        """Check if currently in triggered state (magnetic field detected).

        Returns:
            bool: True if triggered
        """
        return self.read_state() == self._trigger_level

    def check_state_change(self):
        """Detect state change and update records.

        Returns:
            tuple: (changed, current_level)
        """
        current = self.read_state()
        changed = current != self._last_state
        if changed:
            if current == self._trigger_level:
                self._trigger_count += 1
            if self._callback:
                self._callback(current == self._trigger_level)
        self._last_state = current
        return changed, current

    @property
    def trigger_count(self):
        """Get cumulative trigger count."""
        return self._trigger_count

    def reset_count(self):
        """Reset trigger count to zero."""
        self._trigger_count = 0

    def wait_for_trigger(self, timeout_ms=None):
        """Block and wait for magnetic trigger, with optional timeout.

        Args:
            timeout_ms: timeout in ms, None for infinite wait

        Returns:
            bool: True=triggered, False=timeout
        """
        start = utime.ticks_ms()
        while True:
            changed, state = self.check_state_change()
            if changed and state == self._trigger_level:
                return True
            if timeout_ms is not None:
                if utime.ticks_diff(utime.ticks_ms(), start) >= timeout_ms:
                    return False
            utime.sleep_ms(10)

    def monitor(self, interval_sec=1):
        """Polling monitor loop, detects and outputs magnetic field state changes.

        Args:
            interval_sec: polling interval in seconds, default 1s
        """
        while True:
            changed, state = self.check_state_change()
            if changed:
                if state == self._trigger_level:
                    print("[ReedSwitch] Triggered: magnetic field change detected")
                else:
                    print("[ReedSwitch] Released: magnetic field back to normal")
            utime.sleep(interval_sec)


if __name__ == "__main__":
    sensor = ReedSwitch(pin=Pin.GPIO31, trigger_level=0, pull=Pin.PULL_PU)
    sensor.monitor(interval_sec=1)
```

