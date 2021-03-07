#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from states import *
import time

#Takes delivery requests and environmental data and publishes actions
#Subscribes to inbox and perceptions
#Publishes to actions

targetDestination = "" #target destination is the end goal of the robot and is a global variable
currState = WallfollowState() 
begin = 0       # Used for telling how long obstacle avoidance is taking

# Translate the line sensor data into a perception and publish
def reason(data, args):
    # Extract the publisher and the message data
    (actionPublisher) = args
    message = str(data.data)
    msg = message.split()
    
    # Wall following state
    if str(currState) == 'WallfollowState':
        # bumper msg
        if msg[0] == "bumper:": 
            if msg[1] == "unpressed":
                actionPublisher.publish("forward")
            # elif msg[1] == "pressed":
                # actionPublisher.publish("stop")
                # currState.on_event('bump')      # change to avoidance state
                # goAround(actionPublisher)
                # begin = time.time()
        # IR msg
        elif msg[0] == "distance:":
            # Too far, make small correction right
            if float(msg[1]) > 20:
                actionPublisher.publish("sright")
            # Too close, make small correction left
            elif float(msg[1]) < 10:
                actionPublisher.publish("sleft")
            else:
                actionPublisher.publish("forward")
    
    # Bumper driven obstacle avoidance state
    elif str(currState) == 'AvoidanceState':
        if msg[0] == "bumper:":
            if msg[1] == "unpressed":
                pass
            elif msg[1] == "pressed":
                # If it hasnt been 6 seconds yet, its a new obsacle
                if time.time() - begin < 6:
                    goAround(actionPublisher)
                # It's the wall
                else:
                    actionPublisher.publish('stop')
                    actionPublisher.publish("backward")
                    actionPublisher.publish("left")
                    currState.on_event("foundwall")


def setMission(data, args):
    #extract the message data
    location = data.data
    targetDestination = location #update targetLocation
    rospy.loginfo("Target Destination updated to " + targetDestination) #log changes
       

# Called when a new obstacle is found
def goAround(actionPublisher):
    actionPublisher.publish("backward")
    actionPublisher.publish("left")
    actionPublisher.publish("forward")
    actionPublisher.publish("forward")
    actionPublisher.publish("right")
    actionPublisher.publish("forward")
    actionPublisher.publish("forward")
    actionPublisher.publish("right")
    actionPublisher.publish("forward")
    actionPublisher.publish("forward")
    actionPublisher.publish("forward")
    

# Initialize the node, setup the publisher and subscriber
def rosMain():
    rospy.init_node('Reasoner', anonymous=True)
    actionPublisher = rospy.Publisher('actions', String, queue_size=20)
    rospy.Subscriber('perceptions', String, reason, (actionPublisher))
    rospy.Subscriber('inbox', String, setMission, (actionPublisher))
    rospy.spin()

if __name__ == '__main__':
    try:
        rosMain()
    except rospy.ROSInterruptException:
        pass


