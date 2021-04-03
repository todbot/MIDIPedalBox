# MIDIPedalBox -- USB and Classic MIDI output on a Trinket M0
#
# 2020-2021 @todbot / Tod E. Kurt
#
# To use:
#  - Copy this file as `code.py` in your Trinket's CIRCUITPY drive
#  - Install necessary extra libraries (see below)
#
# Extra modules needed:
# - adafruit_dotstar
# - adafruit_midi (but only "__init.mpy", "node_on.mpy", "note_off.mpy")
# - adafruit_debouncer
#
# These libraries can be installed all at once with:
#  circup install circup install adafruit_dotstar adafruit_midi adafruit_debouncer
# Get `circup` with `pip3 install circup`
#
# Classic MIDI (5-pin DIN MIDI) is on pin D0 and can be wired up as shown in
# the diagrams here:
#  https://learn.adafruit.com/classic-midi-synth-control-with-trellis-m4/midi-connections
# Specifically I've had luck with the following wiring:
#  - Trinket Gnd    --> Ring of Type-B adapter --> MIDI pin 2
#  - Trinket 3v3    --> Tip of Type-B adapter  --> MIDI pin 4
#  - Trinket Pin D0 --> 47 ohm resistor --> Sleeve of Type-B adapter --> MIDI pin 5
#

import time
import board
import busio
from digitalio import DigitalInOut, Direction, Pull
from analogio import AnalogOut, AnalogIn
import adafruit_dotstar as dotstar

import usb_midi
import adafruit_midi
from adafruit_midi.note_off         import NoteOff
from adafruit_midi.note_on          import NoteOn
from adafruit_debouncer import Debouncer

# memory is tight on Trinket, so let's clean up before we start
import gc
gc.collect()

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
uart = busio.UART(board.D0, baudrate=31250, timeout=0.001) # initialize UART 
classic_midi = adafruit_midi.MIDI(midi_out=uart )

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
                classic_midi.send(onPress)
                
            if button.rose:
                print("release:",pin)
                midi.send(onRelease)
                classic_midi.send(onRelease)
                
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
print("Hello MIDIPedalBox")
main()
