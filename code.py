import time
from adafruit_clue import clue
import board
import busio

uart = busio.UART(board.TX, board.RX, baudrate = 9600, timeout = .1)

def clear():
    print("\n" * 20)

data = clue.simple_text_display(title = "PPP Sensor data", title_scale = 2)

def clue_sensors():
    data[0].text = "Pressure:       {:.3f} milibar".format(clue.pressure)
    data[1].text = "Temperature:    {:.3f} °C".format(clue.temperature)
    data[2].text = "Humidity:       {:.3f} %".format(clue.humidity)
    data.show()

def PM_sensors():
    uart.write(b"w")
    resp = uart.read()
    wetness = float(resp[2:-2])

    uart.write(b"h")
    resp = uart.read
    humidity = float(resp[2:-2])

    uart.write(b"t")
    resp = uart.read
    temperature = float(resp[2:-2])

    return wetness, humidity, temperature

if __name__ == "__main__":
    clear()
    print("Proficient Python Programmers\nProbe Program P0.01\n")

    uart.write(b"w")
    resp = uart.read()
    # wetness = float(resp[2:-2])
    wetness = resp
    print(f"Wetness:       {wetness} %")

    '''
    while True:
        clue_sensors()
        wetness, humidity, temperature = PM_sensors()
        print(f"Wetness:       {wetness:.3f} %")
        print(f"Humidity:       {humidity:.3f} %")
        print(f"Temperature:    {temperature:.3f} °C")
    '''

