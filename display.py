#!/usr/bin/python
# Copyright (c) 2023 Blue Rock Softwarea
# Author: Yash Gandhi & Ben Payne

import time

import BRS_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import PIL.ImageOps

import subprocess
import re 
import os
import sys

# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isnt used
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

TEST_MAX = False

# ALSA card id of the Digital Hat.  The kernel derives it from the card name
# "snd_IA_Digital_Hat" by dropping non-alphanumeric characters.  Override with
# the IA_CARD_ID environment variable for older driver builds that used a
# different name (e.g. "sndinterludeaud").
CARD_ID = os.environ.get("IA_CARD_ID", "sndIADigitalHat")
HW_PARAMS_PATH = f"/proc/asound/{CARD_ID}/pcm0p/sub0/hw_params"


# 128x32 display with hardware I2C:
disp = BRS_SSD1306.SSD1306_128_32(rst=RST)

# format of the proc entry at /proc/asound/sndIADigitalHat/pcm0p/sub0/hw_params
# access: MMAP_INTERLEAVED
# format: S24_LE
# subformat: STD
# channels: 2
# rate: 44100 (44100/1)
# period_size: 1470
# buffer_size: 22050
def get_sample_rate():
    # The file reads "closed" when nothing is playing, and does not exist at
    # all if the sound card has not come up; both mean "no sample rate".
    try:
        with open(HW_PARAMS_PATH, "r") as sample_fd:
            string_data = sample_fd.readlines()
    except OSError:
        return 0

    for line in string_data:
        parts = line.split(" ")
        if parts[0] == "rate:":
            return int(parts[1])

    return 0


def text_width(font, text):
    # Pillow 8.0 added getlength(); older releases (e.g. the apt package on
    # Volumio) only have getsize().
    if hasattr(font, "getlength"):
        return font.getlength(text)
    return font.getsize(text)[0]


def update_stats(image):
    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)
    # Load default font.
    font_small = ImageFont.truetype("assets/Questrial-Regular.ttf", 10)
    font_medium = ImageFont.truetype("assets/Questrial-Regular.ttf", 14)
    font_large = ImageFont.truetype("assets/Questrial-Regular.ttf", 24)
    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,image.width,image.height), outline=0, fill=0)

    sample_rate = get_sample_rate()

    if not TEST_MAX:
        sample_rate_str = f"{sample_rate/1000}"
    else:
        sample_rate_str = "172.4"

    # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    cmd = "hostname -I"
    if not TEST_MAX:
        ip_str = subprocess.check_output(cmd, shell = True, text = True)
    else:
        ip_str = "255.255.255.255"

    # start just above screen with text so that it doesn't leave blank space at the top of the screen
    top = -2

    draw.text((0, top),       "IP : " ,  font=font_medium, fill=255)
    draw.text((40,top), str(ip_str), font=font_medium, fill=255)
    draw.text((0, top+14),    "Sample",  font=font_small, fill=255)
    draw.text((0, top+22),    "Rate",  font=font_small, fill=255)

    left = text_width(font_small, "Sample") + 10
    if sample_rate == 0:
        draw.text((left, top+14),    "None",  font=font_medium, fill=255)
    else:
        draw.text((left, top+14),    sample_rate_str,  font=font_large, fill=255)

    if sample_rate != 0:
        left += text_width(font_large, sample_rate_str) + 2
        draw.text((left, top+24),    "kHz",  font=font_small, fill=255)


def display_splash(image):
    logo = Image.open('assets/logo3.png').convert('1')

    #print(f"logo size {logo.width}, {logo.height}")
    #print(f"disp size {disp.width}, {disp.height}")
    offset_x = (disp.width-logo.width)/2
    offset_y = (disp.height-logo.height)/2
    #print(f"disp size {offset_x}, {offset_y}")

    draw = ImageDraw.Draw(image)
    draw.rectangle((0,0,image.width-1,image.height-1), outline=1, fill=0)

    # paste logo into display centered.
    image.paste(logo, (int(offset_x),int(offset_y)))


def main():
    # Initialize library.  The I2C bus or the display may not be ready in the
    # first seconds after boot; retry rather than letting systemd restart us.
    for attempt in range(30):
        try:
            disp.begin()
            break
        except OSError as e:
            print(f"display not ready ({e}), retrying", file=sys.stderr)
            time.sleep(2)
    else:
        print("giving up: no display found on I2C", file=sys.stderr)
        sys.exit(1)

    # Clear display.
    disp.clear()
    disp.display()

    # Create blank image for drawing.
    # Make sure to create image with mode '1' for 1-bit color.
    image = Image.new('1', (disp.width, disp.height))

    display_splash(image)
    disp.image(image)
    disp.display()

    time.sleep(10 if not TEST_MAX else 1)

    while True:
        update_stats(image)
        disp.image(image)
        disp.display()

        time.sleep(1)


if __name__ == "__main__":
    main()