#!/usr/bin/env python

#Created on Tue Feb  4 14:52:12 2020
#@author: patrickgavigan

import rospy
import re
from std_msgs.msg import String
from std_msgs.msg import Bool


# Receive the action message and call the method for performing the action
def receiveAction(sensorData):
    # Message will be of the format "lights(True)" or "lights(False)"
    # Extract the message usign regex
    sensorData = str(sensorData)
    print("message was: " +sensorData)
    message = re.search(r'\((.*?)\)',sensorData).group(1)

    # Bullet proof in case it isn't a boolean value
    if message == "true":
        message = True
    else:
        message = False

    # Perform the action    
    performAction(message)


# Perform the action: If message == True, lights on, otherwise lights off
def performAction(message):
    
    # Setup publishers for the different types of lights
    checkLedPub = rospy.Publisher('check_led', Bool, queue_size=10)
    debrisLedPub = rospy.Publisher('debris_led', Bool, queue_size=10)
    dockLedPub = rospy.Publisher('dock_led', Bool, queue_size=10)
    powerLedPub = rospy.Publisher('power_led', Bool, queue_size=10)
    spotLedPub = rospy.Publisher('spot_led', Bool, queue_size=10)

    # Cast the message as a bool
    message = bool(message)

    # Send the messages
    checkLedPub.publish(message)
    debrisLedPub.publish(message)
    dockLedPub.publish(message)
    powerLedPub.publish(message)
    spotLedPub.publish(message)


# Main method: subscribe to relevant actions and receive
def actionTranslatorMain():

    # Setup the node
    rospy.init_node('actionTranslater', anonymous=True)
    
    # Listen to actions messages
    rospy.Subscriber('actions', String, receiveAction)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()
    
    
if __name__ == '__main__':
    try:
        actionTranslatorMain()
    except rospy.ROSInterruptException:
        pass







