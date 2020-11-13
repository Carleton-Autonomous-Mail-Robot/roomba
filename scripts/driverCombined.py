#!/usr/bin/env python

from imutils.video import VideoStream
from pyzbar import pyzbar
import rospy
from std_msgs.msg import String
#import datetime
import imutils
import time
import RPi.GPIO as GPIO

# Global variables to remember current and previous qr codes
previous = "unknown"
current = "unknown"

# Initialize GPIO
GPIO.setmode(GPIO.BOARD)

right_sensor = 8
center_sensor = 10
left_sensor = 12

GPIO.setwarnings(False)
GPIO.setup(right_sensor, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(center_sensor, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(left_sensor, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


# Initialize the video stream and allow the camera sensor to warm up
vs = VideoStream(src=0).start()
time.sleep(4.0)

# Get the sesor data
def getLine():
    centerLED = GPIO.input(center_sensor)
    leftLED = GPIO.input(left_sensor)
    rightLED = GPIO.input(right_sensor)
    LEDs = (leftLED, centerLED, rightLED)
    
    # Interpret the data; 0 indicates the location of the line
    if LEDs == (1,0,1):
        result = "line(center)"
    elif (LEDs == (1,1,0)) or (LEDs == (1,0,0)):
        result = "line(right)"
    elif (LEDs == (0,1,1)) or (LEDs == (0,0,1)):
        result = "line(left)"
    elif LEDs == (0,0,0):
        result = "line(across)"
    else:
        result = "line(lost)"
        
    return (result, LEDs)


# Translate the line sensor data into a perception and publish
# def translateQr(qr):

#     acceptable = ["post1", "post2", "post3", "post4", "post5"]
#     if not (qr in acceptable):
#         return
    
#     # Get access to the global variables (a bit hacky)
#     global previous
#     global current
    
#     # Check if the post point changed, update history if necessary
#     if qr != current:
#         previous = current
#         current = qr

#     # Publish the perception
#     postPoint = "postPoint({},{})".format(current, previous)
#     return postPoint


def getQr():
    qr = "nothingGoodHere"
    
    # Get a frame from the threaded video stream and resize it to have a 
    # maximum width of 400 pixels
    frame = vs.read()
    frame = imutils.resize(frame, width=400)

    # Find the barcodes in the frame and decode each of the barcodes
    barcodes = pyzbar.decode(frame)

    for barcode in barcodes:
        # The barcode data is a bytes object so if we want to draw it
        # on our output image we need to convert it to a string first
        qr = barcode.data.decode("utf-8")
        
        
    acceptable = ["post1", "post2", "post3", "post4", "post5"]
    if not (qr in acceptable):
        return "nothingGoodHere"
    
    # Get access to the global variables (a bit hacky)
    global previous
    global current
    
    # Check if the post point changed, update history if necessary
    if qr != current:
        previous = current
        current = qr

    # Publish the perception
    postPoint = "postPoint({},{})".format(current, previous)
    return postPoint
    
    
# Poll the sensors, publish data
def rosMain():
    # Initialize the node
    perceptionsPub = rospy.Publisher('perceptions', String, queue_size=1)
    postPointPub = rospy.Publisher('postPoint', String, queue_size=1)
    rospy.init_node('sensorDriver', anonymous=True)
    rate = rospy.Rate(10)

    
    while not rospy.is_shutdown():
        
        # Get the sensor data
        (linePerception, LEDs) = getLine()
        postPoint = getQr()
        rospy.loginfo("Line sensor data: " + str(linePerception) + ", " + str(LEDs))
        rospy.loginfo("Qr data: " + str(postPoint))

        message = linePerception
        if not "nothingGoodHere" in postPoint:
            message = message + " " + postPoint

        perceptionsPub.publish(message)
        
        if not "nothingGoodHere" in postPoint:
            postPointPub.publish(postPoint)
        
        rate.sleep()


if __name__ == '__main__':
    try:
        rosMain()
    except rospy.ROSInterruptException:
        vs.stop()
        pass
