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
beginTime = time.time()       # Used for telling how long obstacle avoidance is taking
foundWall = True

# Sensor information
currLocation = ""   # beacons in proximity
currDistance = ""   # distance from/between beacons
currWallDist = ""   # distance from wall
currWallAngle = ""  # angle from wall
currBumper = ""     # bumper state

# Translate the sensor data into actions then publish
def reason(publisher):
    # Setup globals
    global beginTime
    global currBumper
    global currDistance
    global currLocation
    global currWallAngle
    global currWallDist
    global foundWall
    
    # Extract the publisher
    (actionPublisher) = publisher
    
    act = "forward"        # holds the desired action. defaults to forward
    
    # Wall following state
    if str(currState) == 'WallfollowState':
        # Bumper status checks
        if currBumper == "unpressed":
            # since there are no obstacles, check status of robot relative to wall
            
            # Too far from wall, make small correction right. ensure robot angle to wall is proper
            if currWallDist > 20 and currWallAngle > 90:
                act = "sright"
            # Touching wall, so send bleft msg
            elif currWallDist == 1 and currWallAngle == 90.0:
                if time.time() - beginTime > 0.5:  # consecutive bleft msgs is a problem, so put 0.5s delay between calls
                    act = "bleft"
                    beginTime = time.time()
            # Too close to wall, make small correction left. ensure robot angle to wall is proper
            elif currWallDist < 10 and currWallAngle < 90:
                act = "sleft"
                
        elif currBumper == "pressed":
            act = "backward"
            beginTime = time.time()
            foundWall = False
            currState.on_event('bump')      # change to avoidance state
         
    
    # Bumper driven obstacle avoidance state
    elif str(currState) == 'AvoidanceState':
        if currBumper == "unpressed":
            # Turn 90 degrees left
            if time.time() - beginTime < 1:
                act = "left"
            # Move forward for 2 seconds
            elif time.time() - beginTime < 3:
                act = "forward"
            # Turn 90 degrees right
            elif time.time() - beginTime < 4:
                act = "right"
            # Move forward for 2 Seconds
            elif time.time() - beginTime < 6:
                act = "forward"
            # Turn 90 degrees right
            elif time.time() - beginTime < 7:
                act = "right"
            # Move forward until bump
            if foundWall:
                # Turn 90 degrees left
                if time.time() - beginTime < 10:
                    act = "left"
                if time.time() - beginTime > 10:
                    currState.on_event("foundwall")
                
        elif currBumper == "pressed":
            # It's the wall
            act = "backward"
            foundWall = True
                
                    
    # Publish desired acton
    actionPublisher.publish(act)
    


def perceive(data, args):
    # Setup global variables
    global currBumper
    global currDistance
    global currLocation
    global currWallAngle
    global currWallDist
    
    # Extract the publisher and the message data
    (actionPublisher) = args
    message = str(data.data)
    msg = message.split()
    
    # Find perception source and update curr status variables
    if msg[0] == "bumper:":
        currBumper = msg[1]
    elif msg[0] == "distance":
        currWallDist = float(msg[1])
        currWallAngle = float(msg[3])


def setMission(data, args):
    global targetDestination
    
    #extract the message data
    location = data.data
    targetDestination = location #update targetLocation
    rospy.loginfo("Target Destination updated to " + targetDestination) #log changes
    

# Initialize the node, setup the publisher and subscriber
def rosMain():
    rospy.init_node('Reasoner', anonymous=True)
    actionPublisher = rospy.Publisher('actions', String, queue_size=20)
    rospy.Subscriber('perceptions', String, perceive, (actionPublisher))
    rospy.Subscriber('inbox', String, setMission, (actionPublisher))
    
    rate = rospy.Rate(10)   # 10 Hz
    while not rospy.is_shutdown():
        reason((actionPublisher))
        rate.sleep()

if __name__ == '__main__':
    try:
        rosMain()
    except rospy.ROSInterruptException:
        pass


