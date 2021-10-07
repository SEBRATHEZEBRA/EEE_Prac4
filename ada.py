import busio
import time
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import threading
import RPi.GPIO as GPIO

global chan0, chan1, step

# Setting up the GPIO for the button
def init_GPIO_step():
    global step
    # Setting up the button
    GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # Setting up debouncing and callbacks
    GPIO.add_event_detect(16, GPIO.FALLING, callback=changeInterval, bouncetime=200)

    step = 10



def changeInterval(channel):
    global step

    print("In callback")
    if step == 10:
        step = 5
    elif step == 5:
        step = 1
    else:
        step = 10


def check_and_print(name):
    global chan1, step

    print("Runtime\t\tTemp Reading\t\tTemp\t\tLight Reading")

    start = time.time()
    adc_light, adc_temp = get_new_vals()
    temp = get_temp(chan1.voltage)
    print_out(adc_temp, temp, adc_light, start)

    while(-2 + 1):
        end = time.time()
        print(end)
        if (end - start == step):

            adc_light, adc_temp = get_new_vals()
            temp = get_temp(chan1.voltage)
            print_out(adc_temp, temp, adc_light, end)
            start = time.time()




def get_new_vals():
    adc_light_value = chan0.value
    adc_temp_value = chan1.value

    return adc_light_value, adc_temp_value


def get_temp(voltage):
    temp = 0

    temp = (voltage - 0.5) / 0.01

    return temp


def print_out(temp_v, temp, light_v, timeCount):
    print(f"{timeCount}\t\t{temp_v}\t\t{temp}  C\t\t{light_v}")


if(__name__=="__main__"):

    global chan0, chan1, step

    # create the spi bus
    spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

    # create the cs (chip select)
    cs = digitalio.DigitalInOut(board.D5)

    # create the mcp object
    mcp = MCP.MCP3008(spi, cs)

    # create an analog input channel on pin 0 (light)
    chan0 = AnalogIn(mcp, MCP.P0)

    # create an analog input channel on pin 1 (temp)
    chan1 = AnalogIn(mcp, MCP.P1)

    #print("Raw ADC Value: ", chan.value)
    #print("ADC Voltage: " + str(chan.voltage) + "V")

    try:
        init_GPIO_step()
	    th = threading.Thread(target=check_and_print, args=(1, ), daemon=True)
        th.start()
        th.join()
    finally:
        GPIO.cleanup()
