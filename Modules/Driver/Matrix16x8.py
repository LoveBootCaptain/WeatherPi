# Based heavily off of
# Matrix8x8.py
# by:
#   Copyright (c) 2014 Adafruit Industries
#   Author: Tony DiCola
#
import time

import HT16K33


class Matrix16x8(HT16K33.HT16K33):
    """Single color 16x8 matrix LED backpack display."""

    def __init__(self, **kwargs):
        """Initialize display.  All arguments will be passed to the HT16K33 class
        initializer, including optional I2C address and bus number parameters.
        """
        super(Matrix16x8, self).__init__(**kwargs)
        self.max_x = 15

    def set_pixel(self, x, y, value):
        """Set pixel at position x, y to the given value.  X and Y should be values
        of 0 to 16.  Value should be 0 for off and non-zero for on.
        """
        if x < 0 or x > self.max_x or y < 0 or y > 7:
            # Ignore out of bounds pixels.
            return

        led_number = (y * 16) + x
        self.set_led(led_number, value)

    def set_image(self, image):
        """Set display buffer to Python Image Library image.  Image will be converted
        to 1 bit color and non-zero color values will light the LEDs.
        """
        imwidth, imheight = image.size
        if imwidth != 16 or imheight != 8:
            raise ValueError('Image must be an 16x8 (15x7) pixels in size.')
        # Convert image to 1 bit color and grab all the pixels.
        pix = image.convert('1').load()
        # Loop through each pixel and write the display buffer pixel.
        for x in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]:
            for y in [0, 1, 2, 3, 4, 5, 6, 7]:
                color = pix[(x, y)]

                # Developer Note:
                # I did notice some random leds flicker on the far right
                # edge ( or the x=0 edge ) so until I figure out why
                # I decided to just blank out this row.
                if x == 0:
                    color = 0

                # Handle the color of the pixel, off or on.
                if color == 0:
                    self.set_pixel(x, y, 0)
                else:
                    self.set_pixel(x, y, 1)

    def display_16x8_buffer(self, value):
        """
        Display the contents of the value buffer which is assumed
        to be a 16x8 buffer of data to turn pixels on and off
        :param value: byte buffer
        :return: none
        """
        for x in range(0, 16):
            column_byte = value[x]
            column_bits_string = bin(column_byte)[2:].zfill(8)
            for y in range(0, 8):
                column_bit = column_bits_string[y]
                if column_bit == '0':
                    self.set_pixel(x, y, 0)
                else:
                    self.set_pixel(x, y, 1)
        # self.set_brightness(self.brightness)
        self.write_display()

    def get_message_buffer(self, message, bitmap_font):
        the_message = message
        message_buffer = []
        for theChar in the_message:
            message_buffer = message_buffer + bitmap_font[theChar]

        return message_buffer

    def scroll_buffer(self, message_buffer, delay=0.2):
        start_index = 0
        end_index = start_index + 16
        while end_index < len(message_buffer):
            self.display_16x8_buffer(message_buffer[start_index:end_index])
            time.sleep(delay)
            end_index += 1
            start_index += 1

    def scroll_message(self, message, bitmap_font, delay=0.02):
        the_message = "  " + message + "  "
        message_buffer = []
        for theChar in the_message:
            message_buffer = message_buffer + bitmap_font[theChar]

        self.scroll_buffer(message_buffer, delay)
