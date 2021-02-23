#!/usr/bin/env python

import rospy
from ca_msgs.msg import Bumper 
from std_msgs.msg import String

# Translate the line sensor data into a perception and publish
def bumpAndDoSomething(data, args):
    # Extract the publisher and the message data
    (publisher) = args
    bumperLeft = data.is_left_pressed
    bumperRight = data.is_right_pressed 
    message = String()
    message.data = "bumper is not being pressed"

    if(bumperLeft or bumperRight):message.data = "bumper is being pressed"
    
# Publish the perception
    publisher.publish(message)


# Initialize the node, setup the publisher and subscriber
def rosMain():
    rospy.init_node('bumperboy', anonymous=True)
    publisher = rospy.Publisher('perceptions', String, queue_size=10)
    rospy.Subscriber('bumper', Bumper, bumpAndDoSomething, (publisher))
    rospy.spin()

if __name__ == '__main__':
    try:
        rosMain()
    except rospy.ROSInterruptException:
        pass


