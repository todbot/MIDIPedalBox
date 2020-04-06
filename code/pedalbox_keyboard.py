# KeyboardPedalBox
#
# 2020 @todbot / Tod E. Kurt
#
# Extra modules needed:
# - adafruit_hid (but only "__init.mpy", "node_on.mpy", "note_off.mpy")
# - adafruit_debouncer
#

import board
from digitalio import DigitalInOut, Direction, Pull
from analogio import AnalogOut, AnalogIn
import time

import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_debouncer import Debouncer

# Your config!
# Set this to be which pins you're using, and what to do. 
# For list of keycodes, see:
# https://circuitpython.readthedocs.io/projects/hid/en/latest/api.html
button_config = [
		# pin,     (Keycodes and modifier keycodes)
		[board.D1, (Keycode.SPACEBAR,) ], # just a space
		[board.D2, (Keycode.A, Keycode.SHIFT, Keycode.GUI) ],# zoom mute
		[board.D3, (Keycode.C, Keycode.CONTROL) ],
		[board.D4, (Keycode.H, Keycode.GUI) ], # CMD-H hide
]
debouncers = [] 

# start up the keyboardy-ness
time.sleep(1)  # Sleep for a bit to avoid a race condition on some systems
kbd = Keyboard(usb_hid.devices)

# Built in red LED
led = DigitalInOut(board.D13)
led.direction = Direction.OUTPUT

# set up the pins and the debouncer on each pin
for (pin,*rest) in button_config:
		button = DigitalInOut(pin)
		button.direction = Direction.INPUT
		button.pull = Pull.UP
		debouncers.append( Debouncer(button) )

print("Hello from KeyboardPedalBox")

######################### MAIN LOOP ##############################
def main():
    while True:
        for i in range(len(button_config)):
            button = debouncers[i]
            button.update()
            
            (pin,keycodes) = button_config[i]
            
            if button.fell:
                print("push:",pin,"keycodes:",keycodes)
                #kbd.send(Keycode.SHIFT,Keycode.A)
                kbd.press(*keycodes)
                
            if button.rose:
                print("release:",pin)
                kbd.release(*keycodes)
                

######

# actually call main
main()
