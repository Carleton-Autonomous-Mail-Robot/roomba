#!/usr/bin/env python

import rospy
from std_msgs.msg import String
import RPi.GPIO as GPIO

# Initialize GPIO
GPIO.setmode(GPIO.BOARD)

front_sensor = 8
back_sensor = 10

GPIO.setwarnings(False) 
GPIO.setup(front_sensor, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(back_sensor, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


# Get the sesor data
def getinfrared():
    frontIR = GPIO.input(front_sensor)
    backIR = GPIO.input(back_sensor)
    IRsensors = (frontIR, backIR)
    
    # Interpret the data; 1 = wall in front of object, 0 = wall undetected TODO use analog values for finer control of robots movement
    if IRsensors == (1, 1): #front sensor 1, back sensor 1 ==> wall
        result = "w"
    elif (IRsensors == (0, 1)): #front sensor 1, back sensor 0 ==> intersection start
        result = "b"
    elif (IRsensors == (1, 0)): #front sensor 0, back sensor 1 ==> intersection end
        result = "f"
    elif IRsensors == (0,0): #front sensor 0, back sensor 0 ==> no wall
        result = "l"
    else:
        result = "x"
        
    return (result, IRsensors)
    
# Poll the sensors, publish data
def rosMain():
    # Initialize the node
    pub = rospy.Publisher('wall', String, queue_size=10)
    rospy.init_node('wallSensor', anonymous=True)
    rate = rospy.Rate(10)

    
    while not rospy.is_shutdown():
        
        # Get the sensor data
        (wallStatus, IRsensors) = getinfrared()
        rospy.loginfo("wall sensor data: " + str(wallStatus) + ", " + str(IRsensors)) # example: "Wall sensor data: w, (0, 0)"
        pub.publish(wallStatus) #w, b, f, l, x
        rate.sleep()


# Run the program
if __name__ == '__main__':
    try:
        rosMain()
    except rospy.ROSInterruptException:
        GPIO.cleanup()
        pass
