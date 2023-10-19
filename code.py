import time
from adafruit_clue import clue

def clear():
    print("\n" * 20)

data = clue.simple_text_display(title = "PPP Sensor data", title_scale = 2)

def sensors():
    data[0].text = "Pressure:       {:.3f} milibar".format(clue.pressure)
    data[1].text = "Temperature:    {:.3f} °C".format(clue.temperature)
    data[2].text = "Humidity:       {:.3f} %".format(clue.humidity)
    data.show()

if __name__ == "__main__":
    clear()
    print("Proficient Python Programmers\nProbe Program P0.01\n")

    while True:
        sensors()
