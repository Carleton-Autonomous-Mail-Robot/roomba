#!/usr/bin/env python

# Simple test tool for the user interface.

# @author: Simon Yacoub

import rospy
from std_msgs.msg import String
import time

def bumperReasoning(data, args):
    (publisher) = args

    message = str(data.data)
    if message == "bumper is not being pressed":
        #driveforward
        publisher.publish("forward")
    elif message == "bumper is being pressed":
        #drivebackward
        publisher.publish("backward")


# Main program
def rosMain():

    # Init the node
    rospy.init_node('BumperReasoner', anonymous=True)

    # Setup the publisher to publish to actions
    actionPublisher = rospy.Publisher('actions', String, queue_size=10)

    # Subscribe to perceptions
    rospy.Subscriber('perceptions', String, bumperReasoning, (actionPublisher))


    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


if __name__ == '__main__':
    try:
        rosMain()
    except rospy.ROSInterruptException:
        pass
        