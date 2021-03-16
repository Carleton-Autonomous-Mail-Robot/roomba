#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from states import *
from reader import *
from pathFinder import *
import time
import math


#Takes delivery requests and environmental data and publishes actions
#Subscribes to inbox and perceptions
#Publishes to actions

path = ""       # The selected path the robot is following
targetNode = "" # Target destination is the end goal of the robot and is a global variable
interNode = ""  # Intermediate destination before the target
currState = DockState()
beginTime = time.time()       # Used for telling how long robot is in certain states
foundWall = True
progress = 0        # tracks progress of current path. Used as index

# Sensor information
currNode = "A"  # beacons in proximity
currDistance = 10    # distance from/between beacons
currWallDist = 0   # distance from wall
currWallAngle = 0  # angle from wall
currBumper = ""     # bumper state

# Translate the sensor data into actions then publish
def reason(publisher):
    # Setup globals
    global path
    global currState
    global targetNode
    global interNode
    global beginTime
    global currBumper
    global currDistance
    global currNode
    global currWallAngle
    global currWallDist
    global foundWall
    global progress
    
    # Extract the publisher
    (actionPublisher) = publisher
    
    act = ""        # holds the desired action.
    
    # Wall following state
    if str(currState) == 'WallfollowState':
        
        # Are we at our destination?
        if targetNode == currNode:
            beginTime = time.time()
            currState = currState.on_event('dock')
            
        # Are we at our intermediate destination?
        if interNode == currNode:
            beginTime = time.time()
            currState = currState.on_event('newdest')
        
        # Bumper status checks
        if currBumper == "unpressed":
            # Since there are no obstacles, check status of robot relative to wall
    
            # Turned too far
            if currWallAngle < 60:
                act = "left"
            elif currWallAngle > 120:
                act = "right"
            # Too far from wall, make small correction right. ensure robot angle to wall is proper
            elif currWallDist > 30 and currWallAngle > 90:
                act = "sright"
            # Too close to wall, so send bleft msg
            elif currWallDist == 1 and currWallAngle == 90.0:
                if time.time() - beginTime > 0.75:  # consecutive bleft msgs is a problem, so put 0.5s delay between calls
                    act = "bleft"
                    beginTime = time.time()
            # Too close to wall, make small correction left. ensure robot angle to wall is proper
            elif currWallDist < 18 and currWallAngle < 90:
                act = "sleft"
            else:
                act = "forward"
                
        elif currBumper == "Lpressed" or (currBumper == "Rpressed" and currWallDist > 11):
            act = "backward"
            beginTime = time.time()
            foundWall = False
            currState = currState.on_event('bump')      # change to avoidance state
         
    
    # Bumper driven obstacle avoidance state
    elif str(currState) == 'AvoidanceState':
        now = time.time()
        print(now - beginTime)
        
        # Turn 90 degrees left initially
        if now - beginTime < 0.5:
            act = "left"
        else:
            if currBumper == "unpressed":
                # go in arc around obstacle
                if now - beginTime < 13:
                    act = "sright"
                # passed obstacle, ram into wall
                else:
                    act = "forward"
                
                if foundWall:   # change to wallfollowing state
                    currState = currState.on_event('foundwall')
            
            elif currBumper == "Lpressed" or currBumper == "Rpressed":
                # adjust around new obstacle
                if now - beginTime < 12:
                    act = "sleft"
                # its been more than allowed seconds
                else:
                    # Should be back at wall. Rotate and then wallfollow
                    foundWall = True
                    beginTime = now
                    act = "backward"
    
    
    # Robot is in docked state
    elif str(currState) == 'DockState':
        now = time.time()
        if now - beginTime < 0.2:
            act = 'dock'
        else:
            if not targetNode == "":
                act = 'backward'
                beginTime = now
                currState = currState.on_event("newdest")
    
    # Robot is at a node and has a new destination, adjust bearing than move
    elif str(currState) == 'InterState':
        now = time.time()
        if now - beginTime < 0.1:
            progress = progress + 1
            interNode = path[progress+1]
        elif now - beginTime < 4:
            action = int(path[progress])
            # Adjust direction you are facing
            if action == -90:
                if now - beginTime < 0.6:
                    act = 'left'
            elif action == 180:
                if now - beginTime < 1.1:
                    act = 'left'
            elif action == 90:
                if now - beginTime < 0.6:
                    act = 'right'
            elif action == 0:
                if now - beginTime < 1.1:
                    act = 'stop'
                    
            # Move forward into new region
            if now - beginTime > 1.5:
                act = 'forward'
        else:
            # Begin wall following again
            act = "stop"
            currState = currState.on_event("dirconfirm")
        
        
    # Publish desired acton
    if not act == '':
        actionPublisher.publish(act)
    


def perceive(data, args):
    # Setup global variables
    global currBumper
    global currDistance
    global currNode
    global currWallAngle
    global currWallDist
    
    # Extract the publisher and the message data
    (actionPublisher) = args
    message = str(data.data)
    msg = message.split()   # split @ space
    
    # Find perception source and update curr status variables
    if msg[0] == "bumper:":
        currBumper = msg[1]
    elif msg[0] == "distance:":
        currWallDist = float(msg[1])
        currWallAngle = float(msg[3])
    elif msg[0] == "node:":
        # Register current location
        currNode = msg[1]
        
        if len(currNode) == 2:
            # Choosing which distance to track, depending on destination
            if interNode == currNode[0]:
                currDistance = msg[2]
            if interNode == currNode[1]:
                currDistance = msg[3]
        else:
            currDistance = msg[2]


# Identifies the path to follow
def setMission(data, args):
    global currNode
    global targetNode
    global path
    global progress
    
    (publisher) = args
    
    # Extract information from data
    tmp = data.data.split()     # Break up message @ spaces
    currNode = tmp[1]
    targetNode = tmp[2]
    
    # Read information on paths and select valid one.
    finder = PathFinder()
    path = finder.find_path(currNode,targetNode)
    progress = 0
    
    # Log changes
    rospy.loginfo("Target Destination updated to " + targetNode)
    rospy.loginfo("Path set to " + path)
    

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


