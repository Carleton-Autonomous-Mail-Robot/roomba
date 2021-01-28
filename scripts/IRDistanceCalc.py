# Simple demo of reading each analog input from the ADS1x15 and printing it to
# the screen.
# Author: Tony DiCola
# License: Public Domain
import time
import math
#import rospy

# Import the ADS1x15 module.
import Adafruit_ADS1x15


# Create an ADS1115 ADC (16-bit) instance.
adc = Adafruit_ADS1x15.ADS1115()

# Note you can change the I2C address from its default (0x48), and/or the I2C
# bus by passing in these optional parameters:

# See table 3 in the ADS1015/ADS1115 datasheet for more info on gain.
GAIN = 2

def test():
	#this is just a test function to pass set values to check math
	distance(5.5, 7.25)

def distance(dis1, dis2):
	#the two distance reading are passed to this from the sensors (in cm)
	#and this published the angle and distance values it calculates
	#set R as the angle between the two IR sensors
	R = 20
	#a = dis1, b = dis2
	r = math.sqrt(dis1 ** 2 + dis2 ** 2 - 2 * dis1 * dis2 * math.cos(R*math.pi/180))
	B = math.asin((dis1*math.sin(R*math.pi/180))/r)*180/math.pi
	A = 180 - B - R / 2
	b = math.sin(B)*dis2/math.sin(A)
	print("Distance from wall is "+ str(b) +" centimeters")
	print("Offset angle is "+ str(180 - A) +" degrees.")
	#when actually implemented into the robot publish will replace the prints
	#publish(b, A)
	
print('Reading ADS1x15 values, press Ctrl-C to quit...')
# Print nice channel column headers.
print('| Sensor 1 | Sensor 2 |'.format(*range(2)))
print('-' * 37)

while True:
	
    values = [0]*2
    v = [0]*2
    for i in range(2):
        # Read the specified ADC channel using the gain value.
        #values[i] = adc.read_adc(i, gain=GAIN)
        v[i]=3.3*adc.read_adc(i, gain=GAIN)/65536
        values[i] = (1-(v[i]/13.15))-0.35
        #values[i] = (1/((v[i]*3.3/225)/13.15))-0.35
        #values[i] = adc.read_adc(i, gain=GAIN, data_rate=128)
        #distance(v[0], v[1])
    test()
    # Pause for half a second.
    time.sleep(0.5)
    
    

