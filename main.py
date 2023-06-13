import utime
import st7789
import tft_config
from network import WLAN, STA_IF   # handles connecting to WiFi
import urequests    # handles making and servicing network requests
import machine
import json
import gc

tft = tft_config.config(3)

# enable display and clear screen
tft.init()


class NetworkManager:
    def __init__(self):
        self.wlan = WLAN(STA_IF)
        self.wlan.active(True)

    def connect_to_network(self):
        with open("network_config.json", "r") as file:
            config_data = json.load(file)
        network_info = config_data["network"]
        ssid = network_info["ssid"]
        password = network_info["network_password"]
        self.wlan.connect(ssid, password)


def set_pico_time_from_server():
    response = urequests.get("http://192.168.1.4:5000/datetime")
    data = response.json()

    year, month, day = map(int, data["date"].split("-"))
    hour, minute, second = map(int, data["time"].split(":"))

    rtc = machine.RTC()
    rtc.datetime((year, month, day, 0, hour, minute, second, 0))


def print_pico_time():
    rtc = machine.RTC()
    year, month, day, weekday, hours, minutes, seconds, subseconds = rtc.datetime()
    current_date = "{:04d}-{:02d}-{:02d}".format(year, month, day)
    current_time = "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)
    date_time = [current_date, current_time]
    return date_time


def get_current_date():
    r = urequests.get("http://192.168.1.4:5000/datetime")  # Server that returns the current GMT+0 time.
    date = r.json()["date"]
    return date


def get_master_bedroom():
    # Replace the URL with the actual URL of your Flask app
    url = 'http://192.168.1.4:5000/masterbedroom'

    # Send a GET request to the /masterbedroom endpoint
    response = urequests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Replace 'image.png' with the desired filename and extension
        filename = 'MasterBedroom.png'

        with open(filename, 'wb') as file:
            # Save the image content to the file
            file.write(response.content)

        print(f'Saved {filename} successfully.')
    else:
        print(f'Request failed with status code {response.status_code}.')


def get_living_room():
    # Replace the URL with the actual URL of your Flask app
    url = 'http://192.168.1.4:5000/livingroom'

    # Send a GET request to the /masterbedroom endpoint
    response = urequests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Replace 'image.png' with the desired filename and extension
        filename = 'LivingRoom.png'

        with open(filename, 'wb') as file:
            # Save the image content to the file
            file.write(response.content)

        print(f'Saved {filename} successfully.')
    else:
        print(f'Request failed with status code {response.status_code}.')


def get_second_bedroom():
    # Replace the URL with the actual URL of your Flask app
    url = 'http://192.168.1.4:5000/secondbedroom'

    # Send a GET request to the /masterbedroom endpoint
    response = urequests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Replace 'image.png' with the desired filename and extension
        filename = 'SecondBedRoom.png'

        with open(filename, 'wb') as file:
            # Save the image content to the file
            file.write(response.content)

        print(f'Saved {filename} successfully.')
    else:
        print(f'Request failed with status code {response.status_code}.')


# Start networking
network_manager = NetworkManager()
network_manager.connect_to_network()
utime.sleep(3)


def main():
    gc.enable()
    try:
        current_date = get_current_date()
        set_pico_time_from_server()
        get_master_bedroom()
        get_living_room()
        get_second_bedroom()
    except Exception as e:
        print(e)

    tft.fill(st7789.BLACK)
    # display png in random locations
    # Set the screen dimensions
    screen_width = 320  # Width of the screen in pixels
    screen_height = 240  # Height of the screen in pixels

    # Set the image dimensions
    image_width = 320  # Width of the image in pixels
    image_height = 240  # Height of the image in pixels

    # Calculate the coordinates for centering the image
    x = (screen_width - image_width) // 2
    y = (screen_height - image_height) // 2

    while True:
        gc.collect()
        tft.png("MasterBedroom.png", x, y)
        utime.sleep(10)
        tft.fill(st7789.BLACK)
        tft.png("LivingRoom.png", x, y)
        utime.sleep(10)
        tft.fill(st7789.BLACK)
        tft.png("SecondBedRoom.png", x, y)
        utime.sleep(10)
        tft.fill(st7789.BLACK)
        date_time = print_pico_time()
        print(date_time[0])
        minute = str(date_time[1]).split(":")[1]
        second = str(date_time[1]).split(":")[2]
        # Refresh charts daily
        if date_time[0] != current_date:
            current_date = date_time[0]
            get_master_bedroom()
            get_living_room()
            get_second_bedroom()
        print(minute)
        # Refresh charts hourly
        if minute == "59":
            print("Hourly Refresh")
            try:
                get_master_bedroom()
                get_living_room()
                get_second_bedroom()
            except Exception as e:
                print(e)
                pass


main()
