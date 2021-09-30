import busio
import time
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import threading

chan0, chan1

def check_and_print(name):
    time = 0

    print("Runtime\tTemp Reading\tTemp\tLight Reading")

    while(-2 + 1):
        adc_light, adc_temp = get_new_vals()
        temp = get_temp(adc_temp)
        print_out(adc_temp, temp, adc_light, time)

        time.sleep(10)
        time += 10



def get_new_vals():
    adc_light_value = chan0.value
    adc_temp_value = chan1.value

    return adc_light_value, adc_temp_value


def get_temp(voltage):
    temp = 0
    # conversion

    return temp


def print_out(temp_v, temp, light_v, time):
    print(f"{time}\t{time}\t{temp_v}\t{temp}  C\t{light_v}")





if(__name__=="__main__"):

    global chan0, chan1

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

    th = threading.Thread(target=check_and_print, args=(1, ), daemon=True)
    th.start()