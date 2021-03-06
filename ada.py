import busio
import time
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import threading
import RPi.GPIO as GPIO
import sys

global chan0, chan1, step

# Setting up the GPIO for the button
def init_GPIO_step():
    global step
    # Setting up the button
    GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # Setting up debouncing and callbacks
    GPIO.add_event_detect(23, GPIO.FALLING, callback=changeInterval, bouncetime=200)

    step = 10


# Callback function that is called when the button is pressed.
def changeInterval(channel):
    global step

    # Changes the interval of the print outs.
    if step == 10:
        step = 5
    elif step == 5:
        step = 1
    elif step == 1:
        step = 10

# Prints out the values read from the thermistor and LDR.
def check_and_print(name):
    global chan1, step

    print("Runtime\t\tTemp Reading\t\tTemp\t\tLight Reading")

    start = time.time()
    adc_light, adc_temp = get_new_vals()
    temp = get_temp(chan1.voltage)
    print_out(adc_temp, temp, adc_light, 0)
    value = 0

    while(-2 + 1):

        diff = int(time.time() - start)

        # Checking to see whether enough time has passed.
        if (diff >= step):

            value += step
            adc_light, adc_temp = get_new_vals()
            temp = get_temp(chan1.voltage)
            print_out(adc_temp, temp, adc_light, value)
            start = time.time()

# Function returns the raw ADC values of thermistor and LDR.
def get_new_vals():
    adc_light_value = chan0.value
    adc_temp_value = chan1.value

    return adc_light_value, adc_temp_value

# Calculates the temperature using the passed voltage.
def get_temp(voltage):
    
    # Equation used: Ta = (Tc - V0c) / Tc
    # Values found on the MCP9700 data sheet.
    temp = 0
    temp = round((voltage - 0.5) / 0.01, 2)

    return temp

# Formats the values to be printed out.
def print_out(temp_v, temp, light_v, timeCount):
    print(f"{timeCount}\t\t{temp_v}      \t\t{temp} C\t\t{light_v}")


if(__name__=="__main__"):

    global chan0, chan1, step

    # create the spi bus
    spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

    # create the cs (chip select)
    cs = digitalio.DigitalInOut(board.D5)

    # create the mcp object
    mcp = MCP.MCP3008(spi, cs)

    # create an analog input channel on pin 3 (light)
    chan0 = AnalogIn(mcp, MCP.P2)

    # create an analog input channel on pin 2 (temp)
    chan1 = AnalogIn(mcp, MCP.P1)

    try:
        init_GPIO_step()
        th = threading.Thread(target=check_and_print, args=(1, ), daemon=True)
        th.start()
        th.join()
    finally:
        GPIO.cleanup()
