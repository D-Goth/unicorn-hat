#!/usr/bin/env python

import unicornhat as unicorn
import time
from random import randint

unicorn.set_layout(unicorn.AUTO)
unicorn.rotation(0)
unicorn.brightness(0.4)
uh_width,uh_height=unicorn.get_shape()

heights = []

def setup():

    global heights
    heights = []
    for b in range(0, (uh_width-2)):
        heights.append(0)
    unicorn.off()
    for b in range(0, uh_height):
        unicorn.set_pixel(0, b, 255, 255, 255)
    for b in range(0, uh_height):
        unicorn.set_pixel((uh_width-1), b, 255, 255, 255)
    for b in range(1, (uh_width-1)):
        unicorn.set_pixel(b, 0, 255, 255, 255)
    unicorn.show()


def drop_ball():

    ball_colour = [randint(100, 255), randint(100, 255), randint(100, 255)]
    ball_column = randint(0, (uh_width-3))

    while heights[ball_column] == (uh_height-1):
        ball_column = randint(0, (uh_width-3))
    height = heights[ball_column]
    ball_y = (uh_height-1)
    unicorn.set_pixel(ball_column + 1, ball_y, ball_colour[0], ball_colour[1], ball_colour[2])
    unicorn.show()
    dropcount = (uh_height-2) - height
    for y in range(0, dropcount):
        unicorn.set_pixel(ball_column + 1, ball_y, 0, 0, 0)
        ball_y -= 1
        unicorn.set_pixel(ball_column + 1, ball_y, ball_colour[0], ball_colour[1], ball_colour[2])
        unicorn.show()
        time.sleep(0.02)
    heights[ball_column] += 1


while True:
  for rot in [0, 90, 180, 270]:
    unicorn.rotation(rot)
    uh_width,uh_height=unicorn.get_shape()
    setup()
    for i in range(0, (uh_width-2)*(uh_height-1)):
        drop_ball()
    time.sleep(1)


