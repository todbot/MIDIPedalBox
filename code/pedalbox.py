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

from adafruit_debouncer import Debouncer

import usb_midi
import adafruit_midi
from adafruit_midi.note_off         import NoteOff
from adafruit_midi.note_on          import NoteOn

midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=0)

# One pixel connected internally!
dot = dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1, brightness=0.2)

# Built in red LED
led = DigitalInOut(board.D13)
led.direction = Direction.OUTPUT

b1 = DigitalInOut(board.D1)
b1.direction = Direction.INPUT
b1.pull = Pull.UP
b1s = Debouncer(b1)

# Digital input with pullup on D2
b2 = DigitalInOut(board.D2)
b2.direction = Direction.INPUT
b2.pull = Pull.UP
b2s = Debouncer(b2)

b3 = DigitalInOut(board.D3)
b3.direction = Direction.INPUT
b3.pull = Pull.UP
b3s = Debouncer(b3)

b4 = DigitalInOut(board.D4)
b4.direction = Direction.INPUT
b4.pull = Pull.UP
b4s = Debouncer(b4)

# Used if we do HID output, see below
#kbd = Keyboard()

######################### HELPERS ##############################

# Helper to give us a nice color swirl
def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if (pos < 0):
        return [0, 0, 0]
    if (pos > 255):
        return [0, 0, 0]
    if (pos < 85):
        return [int(pos * 3), int(255 - (pos*3)), 0]
    elif (pos < 170):
        pos -= 85
        return [int(255 - pos*3), 0, int(pos*3)]
    else:
        pos -= 170
        return [0, int(pos*3), int(255 - pos*3)]

######################### MAIN LOOP ##############################

i = 0
while True:
  b1s.update()
  b2s.update()
  b3s.update()
  b4s.update()
  
  # spin internal LED around! autoshow is on
  dot[0] = wheel(i & 255)


  if b1s.fell:
      print("Button D1 pressed!")
      midi.send(NoteOn(44, 120))  # G sharp 2nd octave
      time.sleep(0.001)
      midi.send(NoteOff(44, 120))  # G sharp 2nd octave

  if b2s.fell:
      print("Button D2 pressed")
      midi.send(NoteOn(46, 120))  # G sharp 2nd octave
      time.sleep(0.001)
      midi.send(NoteOff(46, 120))  # G sharp 2nd octave

  if b3s.fell:
      print("Button D3 pressed!")
      midi.send(NoteOn(48, 120))  # G sharp 2nd octave
      time.sleep(0.001)
      midi.send(NoteOff(48, 120))  # G sharp 2nd octave

  if b4s.fell:
      print("Button D4 pressed!")
      midi.send(NoteOn(49, 120))  # G sharp 2nd octave
      time.sleep(0.001)
      midi.send(NoteOff(49, 120))  # G sharp 2nd octave

  i = (i+1) % 256  # run from 0 to 255
  #time.sleep(0.01) # make bigger to slow down
  #time.sleep(0.1)
