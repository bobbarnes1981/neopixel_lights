import board
import neopixel
import time

from threading import Thread

modes = [
    'chase'
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
    def __init__(self):
        Thread.__init__(self)
        self.pixel_pin = board.D18
        self.num_pixels = 50
        self.brightness = 0.2
        self.order = neopixel.RGB
        self.running = False

        self.chase_selected_colours = 'h2'
        self.chase_offset = 0

        self.mode = 'chase'
    def create(self):
        self.pixels = neopixel.NeoPixel(self.pixel_pin, self.num_pixels, brightness=self.brightness, auto_write=False, pixel_order=self.order)
    def run(self):
        self.create()
        print("starting neopixel...")
        self.running = True
        while self.running:
            if self.mode == 'chase':
                self.mode_chase()
            elif self.mode == 'off':
                self.mode_off()
            else:
                print("Unrecognised mode {0}".format(self.mode))
    def set_mode(self, mode):
        self.mode = mode
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

