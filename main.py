import utime
import st7789
import tft_config
import vga2_bold_16x32 as bigFont
import vga1_8x16 as smallFont
from network import WLAN, STA_IF   # handles connecting to WiFi
import urequests    # handles making and servicing network requests
from machine import Pin, I2C
import machine
import json
import gc
import random
import os

#tft = tft_config.config(3, buffer_size=30*2)
gc.enable()
gc.collect()
tft = tft_config.config(3, buffer_size=30 * 2)

# enable display and clear screen
tft.init()


class NetworkManager:
    def __init__(self):
        self.wlan = WLAN(STA_IF)
        self.wlan.active(True)

    def connect_to_network(self):
        with open("./etc/network_config.json", "r") as file:
            config_data = json.load(file)
        network_info = config_data["network"]
        ssid = network_info["ssid"]
        password = network_info["network_password"]
        self.wlan.connect(ssid, password)


# Start networking
network_manager = NetworkManager()
network_manager.connect_to_network()
utime.sleep(3)


def main():
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

    tft.png(f'LivingRoom_155452030623.png', 0, 140)
    # Replace 'http://<pi_ip_address>:5000/images' with the URL of your Flask app
    """
    url = 'http://192.168.1.4:5000/image'
    # Send a GET request to the Flask app
    response = urequests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Get the list of image URLs from the response
        image_urls = response.json()
        print(response.json())
        # Iterate over the image URLs
        for i, image_url in enumerate(image_urls):
            # Send a GET request for each image URL
            image_response = urequests.get(image_url)

            # Check if the request for the image was successful
            if image_response.status_code == 200:
                # Save the received image to a file
                with open(f'image_{i}.png', 'r') as f:
                    f.write(image_response.content)
                    tft.png(i, 160, 120)
                print(f'Image {i} saved successfully.')
            else:
                print(f'Error occurred while retrieving image {i}:', image_response.status_code)
    else:
        print('Error occurred:', response.status_code)
    """

main()
