#!/usr/bin/env python
from __future__ import print_function
import unicornhat as uh
import datetime
from time import sleep

print("""True Binary Clock made by Iorga Dragos Florian and Jarrod Price
Displays the following:
Top row ->  First 4 = Month(Pink), Last 4 = Day(Blue)
Second row ->  First 2 = Alarm(Orange), Last 6 = Hour(Red)
Third row -> First 2 = Alarm(Orange), Last 6 = Minute(Yellow)
Fourth row ->  First 2 = Alarm(Orange), Last 6 = Second(Green)""")
uh.set_layout(uh.AUTO)
#default brightness does not need to be too bright
uh.brightness(0.5)
#we need the width of the hat for the padding, see below
width, height = uh.get_shape()

#colour tuples 
red = (255,0,0)
orange = (255,127,0)
yellow = (255,255,0)
green = (0,255,0)
blue = (0,127,255)
magenta = (255,0,255)
white = (255,255,255)

#alarm must be 24 hour format
alarm_time = '07:00'
alarm_flash_time=5
#inform the world what time the alarm will go off
print('Alarm set for: ', alarm_time)

#This function will draw the binary time at a specified location and colour
#t = time value which will be converted to binary
#l = length of the binary string once converted, e.g. day will not go past 31 so only needs 4 bits not like minutes or seconds which need 6 bits
#o = offset, all values are displayed with right alignment as conventional binary dictates, the offest will move it to the left
#y = this is the y-axis, i.e. what row you want it displayed on
#c = colour you want the binary to display as
def draw_time_string(time_string,width,offset,row,colour):
    #convert the time value to binary
    value = bin(int(time_string))
    #loop through the given width of the binary time 
    for i in range(0,width):
        #if it's 1 then the LED should be ON otherwise it will be OFF, i.e. display the colour specified or else it will be black
        if value & 1:
            rgb = colour
        else:
            rgb = (0,0,0)
        #determine where on the row it should display this LED
        column = (width - width - offset) + i
        #set the pixel... duh!
        uh.set_pixel(column,row,rgb)
        value >>= 1

#make use of the remaining space to be used an alarm
def alarm(t,c):
    #by default we will assume the alarm will not be triggered so keep the default states of the brightness and LED colours
    uh.brightness(0.5)
    b = '0'
    #grab the hour and minute from the set alarm time
    h = int(alarm_time[:2])
    m = int(alarm_time[3:])
    s = 0
    #create time slot for alarm for today
    at = t.replace(hour=h,minute=m,second=s)
    #create a new time object by adding x minutes to the alarm time
    ft = at + datetime.timedelta(minutes=alarm_flash_time)
    #now check if it's time to flash the alarm or not, by checking if we have passed the time it is meant to go off or 5 minutes have not gone passed
    if t >= at and t < ft:
        #signal the alarm!
        uh.brightness(1)
        #this will make it flash ON when a second is equal and OFF when it is odd
        if int(t.second % 2) == 0:
            #when converted to binary 3 = '11', so this will turn ON 2 LEDs per row
            b = '3'
    #always update the pixels, the logic above will decide if it displays or not
    #3 rows, 2 LEDs wide for the alarm
    draw_time_string(b, 2, 6, 1, c)
    draw_time_string(b, 2, 6, 2, c)
    draw_time_string(b, 2, 6, 3, c)



def binary_clock():
    try:
        while True:
            now = datetime.datetime.now()
            #print(now)

            #draw each time string in their specific locations
            draw_time_string(now.month, 4, 4, 0, magenta)
            draw_time_string(now.day, 4,0, 0, blue)
            draw_time_string(now.hour, 6, 0, 1, red)
            draw_time_string(now.minute, 6, 0, 2, yellow)
            draw_time_string(now.second, 6, 0, 3, green)

            #check if the alarm needs to be signalled or not
            alarm(now, orange)

            #we've now set all the LEDs, time to show the world our glory!
            uh.show()

            #sleep for sec, cos we don't want to wast unnecessary CPU
            sleep(1)
    except:
        print("Exiting")

if __name__ == "__main__":
    binary_clock()
