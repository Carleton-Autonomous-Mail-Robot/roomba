#!/usr/bin/env python

import rospy
from std_msgs.msg import String

#Takes delivery requests and environmental data and publishes actions
#Subscribes to inbox and perceptions
#Publishes to actions

targetDestination = "" #target destination is the end goal of the robot and is a global variable

# Translate the line sensor data into a perception and publish
def reason(data, args):
    # Extract the publisher and the message data
    (actionPublisher) = args
    message = data.data

    #do something with the data below and publish actions to action topic
    actionPublisher.publish("drive(forward)") #for example

    

def setMission(data, args):
    #extract the message data
    location = data.data
    targetDestination = location #update targetLocation
    rospy.loginfo("Target Destination updated to " + targetDestination) #log changes
       



# Initialize the node, setup the publisher and subscriber
def rosMain():
    rospy.init_node('Reasoner', anonymous=True)
    actionPublisher = rospy.Publisher('actions', String, queue_size=10)
    rospy.Subscriber('perceptions', String, reason, (actionPublisher))
    rospy.Subscriber('inbox', String, setMission, (actionPublisher))
    rospy.spin()

if __name__ == '__main__':
    try:
        rosMain()
    except rospy.ROSInterruptException:
        pass


