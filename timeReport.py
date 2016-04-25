import timeit
import ws2812
"""
Run timing report on functions

Raspberry Pi Zero:
write2812_numpy4    (nLED=  8):   3.45 ms
write2812_numpy4    (nLED= 64):   6.24 ms
write2812_numpy4    (nLED=144):  10.15 ms
write2812_numpy4    (nLED=300):  17.53 ms
write2812_numpy8    (nLED=  8):   4.03 ms
write2812_numpy8    (nLED= 64):   7.31 ms
write2812_numpy8    (nLED=144):  11.83 ms
write2812_pylist4   (nLED=  8):   1.41 ms
write2812_pylist4   (nLED= 64):   9.80 ms
write2812_pylist4   (nLED=144):  21.03 ms
write2812_pylist4   (nLED=300):  44.20 ms
write2812_pylist8   (nLED=  8):   1.75 ms
write2812_pylist8   (nLED= 64):  12.47 ms
write2812_pylist8   (nLED=144):  27.21 ms


Raspberry Pi 3:
write2812_numpy4    (nLED=  8):   1.57 ms
write2812_numpy4    (nLED= 64):   4.98 ms
write2812_numpy4    (nLED=144):   9.75 ms
write2812_numpy4    (nLED=300):  19.01 ms
write2812_numpy8    (nLED=  8):   1.81 ms
write2812_numpy8    (nLED= 64):   5.66 ms
write2812_numpy8    (nLED=144):  11.07 ms
write2812_pylist4   (nLED=  8):   0.96 ms
write2812_pylist4   (nLED= 64):   6.97 ms
write2812_pylist4   (nLED=144):  15.51 ms
write2812_pylist4   (nLED=300):  32.12 ms
write2812_pylist8   (nLED=  8):   1.08 ms
write2812_pylist8   (nLED= 64):   7.87 ms
write2812_pylist8   (nLED=144):  17.57 ms

"""

setupFmt="import ws2812,spidev;spi=spidev.SpiDev();spi.open(0,0);n=[[i%30,4*(i%3),i%7] for i in range({nLED})];ws2812.write2812(spi, [0,0,0]*150)" #.format(nLED=8)
stmtFmt="ws2812.{function}(spi, n)" #.format(function="write2812_numpy4")


nCall=200
for function in ["write2812_numpy4", "write2812_numpy8",
                 "write2812_pylist4", "write2812_pylist8"
]:
    for nLED in [5, 64, 144, 300]:
        if (function[-1]=='8') and nLED>170:
            continue
        
        tCall=timeit.timeit(stmt=stmtFmt.format(function=function),
                            setup=setupFmt.format(nLED=nLED),
                            number=nCall)
        print("{function:<20s}(nLED={nLED:3d}): {ms:6.2f} ms".format(function=function,
                                                             nLED=nLED,
                                                             ms=1000*tCall/nCall))

