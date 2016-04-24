# raspberry_ws2812
python routines to program the WS2812 RGB LED chips on the raspberry,
using the hardware SPI MOSI.


Connections from the Raspberry to the WS2812:

WS2812     Raspbery
GND   --   GND. At least one of pin 6, 9, 14, 20, 25
DIN   --   MOSI, Pin 19, GPIO 10
VCC   --   5V. At least one of pin 2 or 4

Of course the WS2812 can (should) be chained, the DOUT of the first
connected to the DIN of the next, and so on.

The spidev module can be obtained from:
https://github.com/doceme/py-spidev
*
git clone https://github.com/doceme/py-spidev.git
cd py-spidev
make
make install


Then, this module can be tested using:
python ws2812.py

Sample program that uses the module:
```
import spidev
import ws2812
spi = spidev.SpiDev()
spi.open(0,0)
#write 4 WS2812's, with the following colors: red, green, blue, yellow
write2812(spi, [[10,0,0], [0,10,0], [0,0,10], [10, 10, 0]])
```
    
************
Note: this module tries to use numpy, if available.
Without numpy it still works, but is *really* slow (more than a second
to update 300 LED's on a Raspberry Pi Zero).
So, if possible, do:
```
sudo apt install python-numpy
```