"""Waveshare Pico LCD 2 inch display"""

#Current settings:
#rotation = 0
#madctl = 0x00 ()
#inversion_mode(True)
#color_order = st7789.RGB
#for rotation 0 use offset(0, 0)
#for rotation 1 use offset(0, 0)
#for rotation 2 use offset(0, 0)
#for rotation 3 use offset(0, 0)



from machine import Pin, SPI
import st7789

TFA = 0	 # top free area when scrolling
BFA = 0	 # bottom free area when scrolling

def config(rotation=0, buffer_size=0, options=0):
    return st7789.ST7789(
        SPI(1, baudrate=1000000, sck=Pin(14), mosi=Pin(15)),
        240,
        320,
        reset=Pin(13, Pin.OUT),
        cs=Pin(11, Pin.OUT),
        dc=Pin(12, Pin.OUT),
        # backlight=Pin(9, Pin.OUT),
        rotation=rotation,
        options=options,
        buffer_size=buffer_size)
