import board
import neopixel
import time

from threading import Thread

class Lights(Thread):
    colours_h = [
        (255, 60, 0),   # orange
        (0, 128, 0),    # green
        (128, 0, 128)   # purple
    ]
    colours_c = [
        (255, 0, 0),    # red
        (0, 128, 0),    # green
        (128, 128, 128) # white
    ]
    def __init__(self):
        Thread.__init__(self)
        self.pixel_pin = board.D18
        self.num_pixels = 50
        self.brightness = 0.2
        self.order = neopixel.RGB
        self.colours = self.colours_h
    def create(self):
        self.pixels = neopixel.NeoPixel(self.pixel_pin, self.num_pixels, brightness=self.brightness, auto_write=False, pixel_order=self.order)
    def run(self):
        self.create()
        offset = 0
        print("starting...")
        while True:
            for p in range(0, self.num_pixels):
                num = (p+offset) % len(self.colours)
                self.pixels[p] = self.colours[num]
            self.pixels.show()
            offset+=1
            if offset == len(self.colours):
                offset = 0
            time.sleep(0.5)

