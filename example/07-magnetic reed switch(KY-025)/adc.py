from misc import ADC
import _thread
import utime

def fun():
    while True:
        num=adc.read(adc.ADC0)
        utime.sleep(1)
        print(num)


if __name__=='__main__':
    adc = ADC()
    adc.open()
    _thread.start_new_thread(fun,())