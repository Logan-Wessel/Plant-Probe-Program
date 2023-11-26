import time as t
from adafruit_clue import clue
import pwmio, board, busio


# Setup stuff
uart = busio.UART(board.TX, board.RX, baudrate = 9600, timeout = .1)
speaker = pwmio.PWMOut(board.SPEAKER, variable_frequency = True)
speaker.frequency = 600 # Hz
speaker.duty_cycle = 0
data = clue.simple_text_display(title = "PPP Sensor data", title_scale = 2)


# Calibration coefficient from my house
clue_humidity_calibration = 53 / 42.3
clue_temperature_calibration = .8526491152
pm_humidity_calibration = 53 / 49.5
pm_temperature_calibration = 1.044176707

'''
Wiring for Clue <-> PM
0 <-> Up
1 <-> Down
3V <-> 3V
GND <-> GND
''' 


# Temporary bounds for testing
lower_temperature = 15 # °C
upper_temperature = 25 # °C


# Functions
def clear():
    print("\n" * 20)

def show_data():
    wetness, humidity, temperature = PM_sensors()
    avg_temperature = ((clue.temperature * clue_temperature_calibration) + temperature) / 2
    avg_humidity = ((clue.humidity * clue_humidity_calibration) + humidity) / 2
    light = light_levels()

    data[0].text = "Soil Wetness:  {:5.0f} %".format(wetness)
    data[1].text = "Temperature:  {:2.3f} °C".format(avg_temperature)
    data[2].text = "Humidity:     {:2.3f} %".format(avg_humidity)
    data[3].text = "Light level:    {:3.2f} L".format(light) # if > 2.5?, theres sunlight
    
    if upper_temperature < avg_temperature or avg_temperature < lower_temperature:
        scream(True)
        data[5].color = (255, 0, 0)
        data[5].text = "Temperature of {} fell out of bounds".format(avg_temperature)
        # print(f"Temperature of {avg_temperature} fell out of bounds")
    else:
        scream(False)
        data[5].text = ""

    data.show()

def light_levels():
    # level = math.floor(clue.color[3] / 100)
    level = clue.color[3] / 100
    return level

def scream(state):
    if state:
        speaker.duty_cycle = 65000 # int(65535 * .6) # 65535 is 100% volume, speaker bugs out above 65500
    else:
        speaker.duty_cycle = 0

def PM_sensors():
    uart.write(b"w")
    resp = uart.read()
    wetness = float(resp[2:-2])

    uart.write(b"h")
    resp = uart.read()
    humidity = float(resp[2:-2]) * pm_humidity_calibration

    uart.write(b"t")
    resp = uart.read()
    temperature = float(resp[2:-2]) * pm_temperature_calibration

    return wetness, humidity, temperature


if __name__ == "__main__":
    clear()
    print("Proficient Python Programmers\nProbe Program P0.01\n")

    '''
    for i in range(10, 251):
        freq = int(10 * i)
        print(freq)
        speaker.frequency = freq
        time.sleep(.05)
    #'''

    while True:
        show_data()
