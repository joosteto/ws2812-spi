#!/usr/bin/python
import spidev
import ws2812
import time
import getopt
import numpy
from numpy import sin, pi

def test_pattern_sin(spi, nLED=8, intensity=20):
    tStart=time.time()
    indices=4*numpy.array(range(nLED), dtype=numpy.uint32)*numpy.pi/nLED
    period0=2
    period1=2.1
    period2=2.2
    try:
        while True:
            t=tStart-time.time()
            #t=1.1
            f=numpy.zeros((nLED,3))
            f[:,0]=sin(2*pi*t/period0+indices)
            f[:,1]=sin(2*pi*t/period1+indices)
            f[:,2]=sin(2*pi*t/period2+indices)
            f=(intensity)*((f+1.0)/2.0)
            fi=numpy.array(f, dtype=numpy.uint8)
            #print fi[0]
            #time_write2812(spi, fi)
            ws2812.write2812(spi, fi)
            time.sleep(0.01)
    except KeyboardInterrupt:
        test_off(spi, nLED)

def test_off(spi, nLED):
    ws2812.write2812(spi, [0,0,0]*nLED)

if __name__=="__main__":
    spi = spidev.SpiDev()
    spi.open(0,0)
    
    test_pattern_sin(spi, nLED=8, intensity=255)
    #test_fixed(spi)


