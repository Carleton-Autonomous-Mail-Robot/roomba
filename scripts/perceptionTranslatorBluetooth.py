#!/usr/bin/env python
'''

@author Gabriel Ciolac
@last-edit 2021/02/10-22:04
@contributers Devon Daley
'''

import rospy
from bluepy.btle import Scanner
from std_msgs.msg import String
from reader import BeaconReader


nodes = dict()  # used to get the correcponding node letter of MAC. Eg: nodes['A'] = MAC
proxDistance = 0.4  # How far you have to be from node to be considered in it's region

'''
Assign macs to node letters
'''
def set_Zones():
    global nodes
    
    read = BeaconReader()
    beacons = read.read_beacons()
    for tmp in beacons:
        nodes[beacons[tmp][2]] = tmp

'''
Returns the zone/region the robot is currently located at.
'''
def zone(dictionary_macs):
    global proxdistance
    global nodes
    
    # Find the closest MAC/node
    shortest = 100
    closeMAC = ''
    closeNode = ''
    for key in dictionary_macs:
        if dictionary_macs[key] < shortest:
            for k in nodes:
                if nodes[k] == key:
                    shortest = dictionary_macs[key]
                    closeMAC = key
                    closeNode = k
    
    # If directly at node
    if shortest < proxDistance:
        return closeNode
    # Special case for when at imaginary node F
    elif closeNode == 'C' and shortest > 1.6:
        return 'F'
    # Special case for when at imaginary region CF
    elif closeNode == 'C' and shortest < 1.6:
        return 'CF'
    # If between nodes (in a region)
    else:
        # Find the 2nd closest MAC/node
        shortest2 = 100
        closeMAC2 = ''
        closeNode2 = ''
        for key in dictionary_macs:
            if dictionary_macs[key] < shortest2 and not key == closeMAC:
                for k in nodes:
                    if nodes[k] == key:
                        shortest2 = dictionary_macs[key]
                        closeMAC2 = key
                        closeNode2 = k
                
        # Send region result
        out = ''.join(sorted((closeNode,closeNode2)))
        return out


'''
Find out bluetooth information, send zone and distance measurements to reasoner
'''
def read_bluetooth(str_in, args):
    global nodes
    
    (pub) = args
    set_Zones()
    
    split_lines = str_in.data.splitlines() #splits the published data on new line
    dict_macs = dict()
    for line in split_lines: #iterates through the lines
        tmp = line.split(',') #splits line of formate MAC,distance along the period
        dict_macs[tmp[0]] = float(tmp[1])

    if len(dict_macs) == 0:
        return
    
    # Publish current zone and corresponding distances
    tmp = zone(dict_macs)
    out = ''
    
    # Special case imaginary F
    if tmp == 'F' or tmp == 'CF':
        dist = 1 - int(dict_macs[nodes['C']])
        if dist < 0:
            dist = 0
        out = 'node: ' + tmp + ' ' + str(dist)
    # Not Special case
    elif len(tmp) == 2:
        out = 'node: ' + tmp + ' ' + str(dict_macs[nodes[tmp[0]]]) + ' ' + str(dict_macs[nodes[tmp[1]]])
    else:
        out = 'node: ' + tmp + ' ' + str(dict_macs[nodes[tmp[0]]])
        
    rospy.loginfo(out)
    pub.publish(out)


def rosMain():
    pub = rospy.Publisher('perceptions', String, queue_size=20)
    rospy.init_node('bluetoothTranslator', anonymous=True)
    rospy.Subscriber('beacons', String, read_bluetooth, (pub))
    rate = rospy.Rate(10)

    rospy.spin()


if __name__ == '__main__':
    try:
        rosMain()
    except rospy.ROSInterruptException:
        pass
