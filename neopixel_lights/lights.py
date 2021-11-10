import board
import neopixel
import time

from threading import Thread

modes = [
    'chase'
    'wheel'
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
            elif self.mode == 'off':
                self.mode_off()
            else:
                print("Unrecognised mode {0}".format(self.mode))
    def set_mode(self, mode):
        self.mode = mode
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

