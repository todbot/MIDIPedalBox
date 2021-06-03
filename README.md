# MIDIPedalBox

<img src="./docs/pedalbox-pic1.jpg" width="400"><img src="./docs/pedalbox-render.jpg" width="400">

## Trinket M0 + CircuitPython USB MIDI Pedal Box

## Wiring  

The wiring is pretty straight-forward. A single wire goes from each button to pins 1,2,3,4 and a common ground connecting everybody.

<img width=400 src="./docs/pedalbox_wiring.png">


## Parts

The parts used for MIDIPedalBox:

- 1 - Adafruit Trinket M0
   - [Buy from Adafruit](https://www.adafruit.com/product/3500)
   - A [QT Py](https://www.adafruit.com/product/4600) or [Seeed XIAO](http://amzn.com/B08745JBRP?tag=todbotblog-20) will work too, with minor code modifications

- 4 - effects pedal switches
  - I chose these [generic momentary ones](http://amzn.com/B076V8C3LV?tag=todbotblog-20),
  but there are many to choose from and most all will work. Be sure to check dimensions to be sure!

or if you want push buttons instead of foot switches,

- 4 - 12 mm momentary buttons
  - I used [these from All Electronics](https://www.allelectronics.com/item/pb-138/spst-n.o.-pushbutton-red/1.html), but the equivalent are [available from Amazon](http://amzn.com/B07F24Y1TB?tag=todbotblog-20)

If you want to add serial MIDI out, the CAD includes a hole for a panel mount MIDI jack,
like [this one](http://amzn.com/B01GBT9RC0?tag=todbotblog-20)

_(Note: all Amazon links are affiliate links)_
