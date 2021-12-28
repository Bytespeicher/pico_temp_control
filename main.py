from machine import Pin
from neopixel import Neopixel
import utime
from DHT22 import DHT22

THL = 2     # Anschalttemperatur
THH = 10     # Abschalttemperatur

state = 'off'
# Configure the number of WS2812 LEDs, pins and brightness.
NUM_LEDS = 8
brightness = 0.1

PURPLE = (180, 0, 255)

GRADIENT = [(255,0,0),
(255,10,0),
(255,20,0),
(255,30,0),
(255,40,0),
(255,50,0),
(255,60,0),
(255,70,0),
(255,80,0),
(255,90,0),
(255,100,0),
(255,110,0),
(255,120,0),
(255,130,0),
(255,140,0),
(255,150,0),
(255,160,0),
(255,170,0),
(255,180,0),
(255,190,0),
(255,200,0),
(255,210,0),
(255,220,0),
(255,230,0),
(255,240,0),
(255,250,0),
(253,255,0),
(215,255,0),
(176,255,0),
(138,255,0),
(101,255,0),
(62,255,0),
(23,255,0),
(0,255,16),
(0,255,54),
(0,255,92),
(0,255,131),
(0,255,168),
(0,255,208),
(0,255,244),
(0,228,255),
(0,212,255),
(0,196,255),
(0,180,255),
(0,164,255),
(0,148,255),
(0,132,255),
(0,116,255),
(0,100,255),
(0,84,255),
(0,68,255),
(0,50,255),
(0,34,255),
(0,18,255),
(0,2,255),
(0,0,255)]

#reverse gradient
TEMPS = GRADIENT[::-1]

pin_tip = Pin(18, Pin.OUT, Pin.PULL_DOWN)

pixels = Neopixel(8, 1, 27, "GRB")
pixels.fill(PURPLE)
pixels.show()

pin_dht = Pin(2,Pin.IN,Pin.PULL_UP)

delay = 0
while True:
    utime.sleep_ms(1000)
    print('.')
    delay += 1
    if delay > 3:
        break

hyst = THH - THL    # breite des temp bandes eg: 2 bis 15 = 13 grad
led_step = hyst / (NUM_LEDS-2)  # eg. 13 / (8-2) = 2.16...
color_step = hyst / (len(TEMPS) - 2)  # eg. 13 / 6 = 2.16...
print("led step: {:2.2f} '  color step: {:2.2f}".format(led_step,color_step))

testtemps = (-5, 1.9, 2.0, 2.1, 3, 5, 7, 9, 11, 13, 14.8, 15, 15.5, 20)
while True:
    utime.sleep_ms(1000)
    print('.')
    delay += 1
    if delay > 3:
        break
    
# startup demo and test
for T in testtemps:
    # print("{:3.1f}'C".format(T))
    t = 0 if (T<THL) else (len(TEMPS)-1) if (T>(THH - 0.1)) else int((T - THL)/color_step) + 1
    p = 0 if (T<THL) else (NUM_LEDS-1) if (T>(THH - 0.1)) else int((T - THL) / led_step) + 1
    print("color: {:2d} '  pixels: {:2d}".format(t,p))
    
    pixels.fill((0,0,0))
    pixels.set_pixel_line(0, p, TEMPS[t])
    pixels.show()
    utime.sleep_ms(1000)
 
# work loop
while True:
        # DHT22 not responsive if delay to short
        utime.sleep_ms(500)
        dht_sensor=DHT22(pin_dht, None, dht11=False, smID=5)
        T,H = dht_sensor.read()
        if T is None:
            print(" sensor error")
        else:
            print("{:3.1f}'C  {:3.1f}%".format(T,H))
            #DHT22 not responsive if delay to short

            t = 0 if (T<THL) else (len(TEMPS)-1) if (T>(THH - 0.1)) else int((T - THL)/color_step) + 1
            p = 0 if (T<THL) else (NUM_LEDS-1) if (T>(THH - 0.1)) else int((T - THL) / led_step) + 1
            # print("color: {:2d} '  pixels: {:2d}".format(t,p))
            
            pixels.fill((0,0,0))
            pixels.set_pixel_line(0, p, TEMPS[t])
            pixels.show()
            
            if (T < THL and state == 'off'):
                pin_tip.on()
                print("Power On!")
                utime.sleep_ms(5000)
                state = 'on'
                pin_tip.off()
            if (T > THH and state == 'on'):
                pin_tip.on()
                print("Power Off!")
                utime.sleep_ms(5000)
                state = 'off'
                pin_tip.off()

        utime.sleep_ms(2000)
 

