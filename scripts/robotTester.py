#!/usr/bin/env python

# Simple test tool for the user interface.

# @author: Simon Yacoub

import rospy
from std_msgs.msg import String
import time

# Main program
def rosMain():

    # Init the node
    rospy.init_node('RobotTester', anonymous=True)

    # Setup the publisher to publish to actions
    actionPublisher = rospy.Publisher('actions', String, queue_size=10)
    
    # Get input, send message to actionTranslator
    while not rospy.is_shutdown():
        x = raw_input("Type action message: ")
        actionPublisher.publish(x)
        
        
if __name__ == '__main__':
    try:
        rosMain()
    except rospy.ROSInterruptException:
        pass
