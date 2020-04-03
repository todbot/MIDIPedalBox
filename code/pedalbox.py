# MIDIPedalBox
#
# 2020 @todbot / Tod E. Kurt
#
# Extra modules needed:
# - adafruit_midi (but only "__init.mpy", "node_on.mpy", "note_off.mpy")
# - adafruit_debouncer
#

import board
from digitalio import DigitalInOut, Direction, Pull
from analogio import AnalogOut, AnalogIn
import adafruit_dotstar as dotstar
import time
#import neopixel

import usb_midi
import adafruit_midi
from adafruit_midi.note_off         import NoteOff
from adafruit_midi.note_on          import NoteOn
from adafruit_debouncer import Debouncer

# Your config!
# Set this to be which pins you're using, and what to do
button_config = [
		# pin,     midi press msg, midi release msg
		[board.D1, NoteOn(44,120), NoteOff(44,120) ],
		[board.D2, NoteOn(46,120), NoteOff(46,120) ],
		[board.D3, NoteOn(48,120), NoteOff(48,120) ],
		[board.D4, NoteOn(50,120), NoteOff(50,120) ],
]
debouncers = [] 

midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=0)

# One pixel connected internally!
dot = dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1, brightness=0.2)

# Built in red LED
led = DigitalInOut(board.D13)
led.direction = Direction.OUTPUT

# set up the pins and the debouncer on each pin
for (pin,*rest) in button_config:
		button = DigitalInOut(pin)
		button.direction = Direction.INPUT
		button.pull = Pull.UP
		debouncers.append( Debouncer(button) )
   
######################### MAIN LOOP ##############################
def main():
		doti = 0 
		while True:
				for i in range(len(button_config)):
						button = debouncers[i]
						button.update()
						
						(pin,onPress,onRelease) = button_config[i]
						
						if button.fell:
								print("push:",pin)
								midi.send(onPress)
								
						if button.rose:
								print("release:",pin)
								midi.send(onRelease)
								
				# spin internal LED around! autoshow is on
				dot[0] = wheel(doti & 255)
				doti = (doti+1) % 256  # run from 0 to 255

######################### HELPERS ##############################

# Helper to give us a nice color swirl
def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if (pos < 0):   return [0, 0, 0]
    if (pos > 255): return [0, 0, 0]
    if (pos < 85):  return [int(pos * 3), int(255 - (pos*3)), 0]
    elif (pos < 170):
        pos -= 85
        return [int(255 - pos*3), 0, int(pos*3)]
    else:
        pos -= 170
        return [0, int(pos*3), int(255 - pos*3)]

# actually call main
main()
