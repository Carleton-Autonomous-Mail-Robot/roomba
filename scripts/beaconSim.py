#!/usr/bin/env python

# Simple test tool for the user interface.

# @author: Devon Daley

import rospy
from std_msgs.msg import String
import time
from pathFinder import *

# Main program
def rosMain():
        # Init the node and setup publisher
        rospy.init_node('RobotTester', anonymous=True)
        perceptionsPublisher = rospy.Publisher('perceptions', String, queue_size=10)
        
        while not rospy.is_shutdown():
            inp = raw_input("Type a series of node letters with spaces between (eg 'A B C'): ")
            inp = inp.split()
            
            for node in inp:
                raw_input("Press enter when @ node " + node)   
                out = 'node: ' + node + ' 0.3'  # Prepare message saying we are 0.3 m away from beacon
                perceptionsPublisher.publish(out)
        
        
if __name__ == '__main__':
    try:
        rosMain()
    except rospy.ROSInterruptException:
        pass
