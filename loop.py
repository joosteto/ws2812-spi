import spidev
import ws2812
import time
import getopt

def test_loop(spi, nLED=8, intensity=20):
    stepTime=0.1
    iStep=0
    while True:
        d=[[0,0,0]]*nLED
        d[iStep%nLED]=[intensity]*3
        ws2812.write2812(spi, d)
        iStep=(iStep+1)%nLED
        time.sleep(stepTime)

if __name__=="__main__":
    spi = spidev.SpiDev()
    spi.open(0,0)  
  
    test_loop(spi, nLED=64+8)
