#!/usr/bin/python
NumpyImported=False
try:
    import numpy
    from numpy import sin, cos, pi
    NumpyImported=True
except ImportError:
    #print("Warning: no numpy found, routines will be slow")
    pass
"""
T0H: 0.35   -> 2p=0.31  3p=0.47
T0L: 0.80   -> 6p=0.94  5p=0.78
T1H: 0.70   -> 4p=0.625 5p=0.78
T1L: 0.60   -> 4p=0.625 3p=0.47
"""

def write2812_numpy8(spi,data):
    d=numpy.array(data).ravel()
    tx=numpy.zeros(len(d)*8, dtype=numpy.uint8)
    for ibit in range(8):
        #print ibit
        #print ((d>>ibit)&1)
        #tx[7-ibit::8]=((d>>ibit)&1)*0x18 + 0xE0   #0->3/5, 1-> 5/3 
        #tx[7-ibit::8]=((d>>ibit)&1)*0x38 + 0xC0   #0->2/6, 1-> 5/3
        tx[7-ibit::8]=((d>>ibit)&1)*0x78 + 0x80    #0->1/7, 1-> 5/3
        #print [hex(v) for v in tx]
    #print [hex(v) for v in tx]
    spi.xfer(tx.tolist(), int(8/1.25e-6))
    #spi.xfer(tx.tolist(), int(8e6))
def write2812_numpy4(spi,data):
    #print spi
    d=numpy.array(data).ravel()
    tx=numpy.zeros(len(d)*4, dtype=numpy.uint8)
    for ibit in range(4):
        #print ibit
        #print ((d>>(2*ibit))&1), ((d>>(2*ibit+1))&1)
        tx[3-ibit::4]=((d>>(2*ibit+1))&1)*0x60 + ((d>>(2*ibit+0))&1)*0x06 +  0x88
        #print [hex(v) for v in tx]
    #print [hex(v) for v in tx]
    #spi.xfer(tx.tolist(), int(4/1.25e-6)) #works, but flashes (max white) on Zero
    spi.xfer(tx.tolist(), int(4/1.15e-6))  #works, no flashes on Zero
    #spi.xfer(tx.tolist(), int(4/1.05e-6))  #works, no flashes on Zero
    #spi.xfer(tx.tolist(), int(4/.95e-6))  #works, no flashes on Zero
    #spi.xfer(tx.tolist(), int(4/.90e-6))  #works, no flashes on Zero
    #spi.xfer(tx.tolist(), int(4/.85e-6))  #doesn't work (first 4 LEDS work, others have flashing colors)
    #spi.xfer(tx.tolist(), int(4/.65e-6))  #doesn't work
    #spi.xfer(tx.tolist(), int(8e6))

def write2812_pylist8(spi, data):
    tx=[]
    for rgb in data:
        for byte in rgb: 
            for ibit in range(7,-1,-1):
                tx.append(((byte>>ibit)&1)*0x78 + 0x80)
    spi.xfer(tx, int(8/1.25e-6))

def write2812_pylist4(spi, data):
    tx=[]
    for rgb in data:
        for byte in rgb: 
            for ibit in range(3,-1,-1):
                #print ibit, byte, ((byte>>(2*ibit+1))&1), ((byte>>(2*ibit+0))&1), [hex(v) for v in tx]
                tx.append(((byte>>(2*ibit+1))&1)*0x60 +
                          ((byte>>(2*ibit+0))&1)*0x06 +
                          0x88)
    #print [hex(v) for v in tx]
    spi.xfer(tx, int(4/1.05e-6))


if NumpyImported:
    write2812=write2812_numpy4
else:
    write2812=write2812_pylist4    


if __name__=="__main__":
    import spidev
    import time
    timeUse=0
    nUse=0
    totTimeUse=0
    totNUse=0
    def time_write2812(spi, data):
        global timeUse, nUse, totTimeUse, totNUse
        tStart=time.time()
        #write2812_numpy4(spi, data)       #8: 5.6ms;   300: 18ms
        write2812_numpy8(spi, data)        #8: 6.1ms;   150: 13ms
        #write2812_pylist4(spi, data)      #8: 54ms;   300: 1860ms
        #write2812_pylist8(spi, data)      #8: 53ms;   150: 986ms
        timeUse+=time.time()-tStart
        nUse+=1
        if nUse>200:
            totTimeUse+=timeUse
            totNUse+=nUse
            print "av execute time: {0}, last few: {1}".format(1000*totTimeUse/totNUse,1000*timeUse/nUse)
            nUse=0
            timeUse=0

    def test_pattern_sin(spi):
        n=150
        tStart=time.time()
        indices=numpy.array(range(n))*numpy.pi/7
        period0=2
        period1=2.1
        period2=2.2
        while True:
            t=tStart-time.time()
            #t=1.1
            f=numpy.zeros((n,3))
            f[:,0]=sin(2*pi*t/period0+indices)
            f[:,1]=sin(2*pi*t/period1+indices)
            f[:,2]=sin(2*pi*t/period2+indices)
            f=20*((f+1.01)/2.02)
            fi=numpy.array(f, dtype=numpy.uint8)
            #print fi[0]
            #time_write2812(spi, fi)
            write2812(spi, fi)
            time.sleep(0.01)
            
    def test_fixed(spi):
        #write fixed pattern for 8 LEDs
        write2812(spi, numpy.array([[10,0,0],
                                    [0,10,0],
                                    [0,0,10],
                                    [10,0,0],
                                    
                                    [10,0,0],
                                    [10,0,0],
                                    [10,0,0],
                                    [10,0,0]], dtype=numpy.uint8)
        )
        
    spi = spidev.SpiDev()
    spi.open(0,0)
    
    test_pattern_sin(spi)
    #test_fixed(spi)


