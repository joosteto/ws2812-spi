import spidev
import ws2812
import time
import getopt
import numpy
from numpy import exp, sin, pi

def test_gauss(spi, shape=(8,8), intensity=20):
    
    stepTime=0.05
    nLED=shape[0]*shape[1]
    index_i=numpy.array(range(nLED))%shape[0]
    index_j=numpy.array(range(nLED))/shape[0]
    mid_i=shape[0]/2.
    mid_j=shape[1]/2.
    period_i,period_j=3,3.1
    ri,rj=2,2
    tStart=time.time()
    try:
        while True:
            t=time.time()-tStart
            mi=mid_i+sin(2*pi*t/period_i)*ri
            mj=mid_j+sin(2*pi*t/period_j)*rj
            rg0=2*(sin(2*pi*t/6.25)+1)
            rg1=2*(sin(2*pi*t/6.5)+1)
            rg2=2*(sin(2*pi*t/6.75)+1)
            distances2=((index_i-mi)**2+(index_j-mj)**2)
            d=numpy.zeros((nLED,3))
            d[:,0]=exp(-distances2/rg0**2)
            d[:,1]=exp(-distances2/rg1**2)
            d[:,2]=exp(-distances2/rg2**2)
            di=numpy.array(d*intensity, dtype=numpy.uint32)
            
            ws2812.write2812(spi, di)
            time.sleep(stepTime)
            
    except KeyboardInterrupt:
        ws2812.write2812(spi, [[0,0,0]]*(shape[0]*shape[1]))

def test_heart(spi, shape=(8,8), intensity=20):
    
    stepTime=0.05
    nLED=shape[0]*shape[1]
    index_i=numpy.array(range(nLED))%shape[0]
    index_j=numpy.array(range(nLED))/shape[0]
    mid_i=shape[0]/2.
    mid_j=shape[1]/2.
    period_i,period_j=3,3.1
    ri,rj=1.5, 1.5 #2,2
    tStart=time.time()
    try:
        while True:
            t=time.time()-tStart
            mi=mid_i+sin(2*pi*t/period_i)*ri - 2 
            mj=mid_j+sin(2*pi*t/period_j)*rj
            rg0=2*(sin(2*pi*t/6.25)+1)
            rg1=2*(sin(2*pi*t/6.5)+1)
            rg2=2*(sin(2*pi*t/6.75)+1)
            distances2=((index_i-mi)**2+(index_j-mj)**2)
            angles=numpy.abs(numpy.arctan2(index_j-mj, index_i-mi))
            heart=(angles**.5+5/(0.01+abs(angles-numpy.pi))**2)/(1*numpy.pi**.5)
            distances2*=heart
            d=numpy.zeros((nLED,3))
            d[:,0]=exp(-(distances2/rg0**2)**2)
            d[:,1]=exp(-(distances2/rg1**2)**2)
            d[:,2]=exp(-(distances2/rg2**2)**2)
            #rg0=1.5
            #d[:,0]=distances2<rg0*2
            #d[:,1]=distances2<rg0*2
            #d[:,2]=distances2<rg0*2
            di=numpy.array(d*intensity, dtype=numpy.uint32)
            
            ws2812.write2812(spi, di)
            time.sleep(stepTime)
            
    except KeyboardInterrupt:
        ws2812.write2812(spi, [[0,0,0]]*(shape[0]*shape[1]))

if __name__=="__main__":
    spi = spidev.SpiDev()
    spi.open(0,0)  
  
    test_heart(spi, shape=(8,9), intensity=25)
