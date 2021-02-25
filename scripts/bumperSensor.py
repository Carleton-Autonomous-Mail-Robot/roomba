#!/usr/bin/env python

import rospy
from ca_msgs.msg import Bumper 
from std_msgs.msg import String

# Translate the line sensor data into a perception and publish
def bumpAndDoSomething(data, args):
    # Extract the publisher and the message data
    (publisher) = args
    is_left_pressed = data.is_left_pressed
    is_right_pressed = data.is_right_pressed 

    # Bumper light sensors (Create 2 only) in order from left to right
    # Value = true if an obstacle detected
    is_light_left = data.is_light_left
    is_light_front_left = data.is_light_front_left
    is_light_center_left = data.is_light_center_left
    is_light_center_right = data.is_light_center_right
    is_light_front_right = data.is_light_front_right
    is_light_right = data.is_light_right

    message = String()
    
    if(is_left_pressed or is_right_pressed):message.data = "bumper is being pressed"
    else: message.data = "bumper is not being pressed"

    if(data.is_light_front_right or  is_light_center_right):
        message.data = "bumper detects an object to the left"
    elif(is_light_center_left or is_light_front_left):
        message.data = "bumper detects an object to the right"

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


