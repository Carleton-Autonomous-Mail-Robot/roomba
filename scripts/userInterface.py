#!/usr/bin/env python

# Simple test tool for the user interface.

# @author: Patrick Gavigan
# @author: Simon Yacoub

import rospy
from std_msgs.msg import String
import time
from datetime import datetime

startTime = 0   # Set the start time as a global variable

def mailMission(publisher):
    
    # Prompt user for input (using Pyton 7 method, ROS does not use Python 3)
    mission = raw_input("Please enter the delivery location")
    message = "new mission to" + mission
    
    # Build message with the dock location, log and send it
    #rospy.loginfo("Sending message: " + str(message))
    publisher.publish(message)

    # Give it a moment
    time.sleep(1)

# Main program
def rosMain():

    # Init the node
    rospy.init_node('user', anonymous=True)

    # Sleep for 5 seconds, give everything a chance to come online.
    time.sleep(5)

    publisher = rospy.Publisher('inbox', String, queue_size=10)

    mailMission(publisher)
    # Log the start time of the mission
    #global startTime
    #startTime = datetime.now()
    
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


if __name__ == '__main__':
    try:
        rosMain()
    except rospy.ROSInterruptException:
        pass
        