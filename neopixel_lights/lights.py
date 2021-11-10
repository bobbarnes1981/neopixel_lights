import board
import neopixel
import time
import random

from threading import Thread

modes = [
    'chase',
    'wheel',
    'twinkle'
]

class Lights(Thread):
    chase_colours = {
        'h1': [
            (255, 60, 0),   # orange
            (0, 128, 0),    # green
            (128, 0, 128)   # purple
        ],
        'h2': [
            (255, 60, 0),   # orange
            (0, 128, 0),    # green
        ],
        'c': [
            (255, 0, 0),    # red
            (0, 128, 0),    # green
            (128, 128, 128) # white
        ]
    }
    def __init__(self, mode, selected_colours):
        Thread.__init__(self)
        self.pixel_pin = board.D18
        self.num_pixels = 50
        self.brightness = 0.2
        self.order = neopixel.RGB
        self.running = False

        self.chase_selected_colours = selected_colours
        self.chase_offset = 0

        self.wheel_offset = 0

        self.twink_max_time = 4
        self.twink_twinkles = 3
        self.twink_pixels = []
        for _ in range(self.num_pixels):
            self.twink_pixels.append(0)

        self.mode = mode
    def create(self):
        self.pixels = neopixel.NeoPixel(self.pixel_pin, self.num_pixels, brightness=self.brightness, auto_write=False, pixel_order=self.order)
    def run(self):
        self.create()
        print("starting neopixel...")
        self.running = True
        while self.running:
            if self.mode == 'chase':
                self.mode_chase()
            elif self.mode == 'wheel':
                self.mode_wheel()
            elif self.mode == 'twinkle':
                self.mode_twinkle()
            elif self.mode == 'off':
                self.mode_off()
            else:
                print("Unrecognised mode {0}".format(self.mode))
    def set_mode(self, mode):
        self.mode = mode
    def mode_twinkle(self):
        for _ in range(self.twink_twinkles):
            r = random.randrange(self.num_pixels)
            t = random.randrange(self.twink_max_time)
            if self.twink_pixels[r] == 0:
                self.twink_pixels[r] = t
        for i in range(self.num_pixels):
            if self.twink_pixels[i] == 4:
                self.pixels[i] = (255, 255, 255)
            if self.twink_pixels[i] == 3:
                self.pixels[i] = (192, 192, 192)
            if self.twink_pixels[i] == 2:
                self.pixels[i] = (128, 128, 128)
            if self.twink_pixels[i] == 1:
                self.pixels[i] = (64, 64, 64)
            if self.twink_pixels[i] == 0:
                self.pixels[i] = (0, 0, 0)
            if self.twink_pixels[i] > 0:
                self.twink_pixels[i] -= 1
        self.pixels.show()    
        time.sleep(0.25)
    def mode_wheel(self):
        for p in range(0, self.num_pixels):
            idx = (p * 256 // self.num_pixels) + self.wheel_offset
            self.pixels[p] = self.wheel(idx & 255)
        self.pixels.show()
        self.wheel_offset += 1
        if self.wheel_offset > 255:
            self.wheel_offset = 0
        time.sleep(0.001)
    def mode_chase(self):
        for p in range(0, self.num_pixels):
            num = (p+self.chase_offset) % len(self.chase_colours[self.chase_selected_colours])
            self.pixels[p] = self.chase_colours[self.chase_selected_colours][num]
        self.pixels.show()
        self.chase_offset+=1
        if self.chase_offset == len(self.chase_colours[self.chase_selected_colours]):
            self.chase_offset = 0
        time.sleep(0.5)
    def mode_off(self):
        for p in range(0, self.num_pixels):
            self.pixels[p] = (0, 0, 0)
        self.pixels.show()
    def wheel(self, pos):
        # Input a value 0 to 255 to get a color value.
        # The colours are a transition r - g - b - back to r.
        if pos < 0 or pos > 255:
            r = g = b = 0
        elif pos < 85:
            r = int(pos * 3)
            g = int(255 - pos * 3)
            b = 0
        elif pos < 170:
            pos -= 85
            r = int(255 - pos * 3)
            g = 0
            b = int(pos * 3)
        else:
            pos -= 170
            r = 0
            g = int(pos * 3)
            b = int(255 - pos * 3)
        return (r, g, b) if self.order in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)

