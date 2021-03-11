#!/usr/bin/env python
'''

@author Gabriel Ciolac
@last-edit 2021/02/10-22:04
@contributers 
'''

import rospy
from bluepy.btle import Scanner
from std_msgs.msg import String


# Initialize constants
A = 'ea:2f:93:a6:98:20'
B = 'fc:e2:2e:62:9b:3d'
C = 'e2:77:fc:f9:04:93'
D = '00:00:00:00:00:00'
E = '11:11:11:11:11:11'

'''
Returns the zone the robot is currently located at.
'''
def zone(dictionary_macs):
    macs = dictionary_macs.keys()
    
    if A in macs and B in macs:
        if dictionary_macs[B] > 5 and dictionary_macs[A] > 5:
            rospy.loginfo('AB')
    elif A in macs and dictionary_macs[A] < 4.5:
        rospy.loginfo('A')
    elif B in macs and dictionary_macs[B] < 4.5:
        rospy.loginfo('B')
    elif C in macs:
        if D in macs:
            if dictionary_macs[D] < 0.5:
                rospy.loginfo('D')
                return 'D'
            elif dictionary_macs[D] < 2 and dictionary_macs[C] < 2:
                rospy.loginfo('CD')
                return 'CD'
        if E in macs:
            if dictionary_macs[E] < 0.5:
                rospy.loginfo('E')
                return 'E'
            elif dictionary_macs[C] > 0.5:
                rospy.loginfo('CE')
                return 'CE'
        if dictionary_macs[C] < 0.5:
            rospy.loginfo('C')
            return 'C'
        elif dictionary_macs[C] < 3:
            rospy.loginfo('CF')
            return 'CF'
        else:
            rospy.loginfo('F')
            return 'F'
    else:
        rospy.loginfo('Zone was called and nothing happened')
    

    
def read_bluetooth(str_in, args):
    (pub) = args
    
    split_lines = str_in.data.splitlines() #splits the published data on new line
    dict_macs = dict()
    for line in split_lines: #iterates through the lines
        tmp = line.split(',') #splits line of formate MAC,distance along the period
        dict_macs[tmp[0]] = float(tmp[1])

    if len(dict_macs) == 0:
        return
    
    # Publish current zone and corresponding distances
    tmp = 'node: ' + zone(dict_macs)
    if tmp == "CF" or tmp == "CD" or tmp == "CE":
        tmp = tmp + ' ' + dict_macs[C]
    pub.publish(tmp)


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
