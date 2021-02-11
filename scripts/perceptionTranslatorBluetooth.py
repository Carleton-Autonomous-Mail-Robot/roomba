#!/usr/bin/env python
'''

@author Gabriel Ciolac
@last-edit 2021/02/10-22:04
@contributers 
'''

import rospy
from bluepy.btle import Scanner
from std_msgs.msg import String

'''
Hard coded, needs to be redone
'''
def zone(MAC, distance):
    if distance < 3 and MAC == 'fc:e2:2e:62:9b:3d':
        rospy.loginfo('ZONE A')
    elif distance < 3 and MAC == 'ea:2f:93:a6:98:20':
        rospy.loginfo('ZONE B')
    elif distance > 3:
        rospy.loginfo('ZONE AB')

    
def read_bluetooth(str_in):
    split_txt = str_in.data.split(':')
    rospy.loginfo(split_txt[0]+','+split_txt[1])
    




def rosMain():
    pub = rospy.Publisher('perceptions', String, queue_size=20)
    rospy.init_node('bluetoothTranslator', anonymous=True)
    rospy.Subscriber('beacons', String, read_bluetooth)
    rate = rospy.Rate(10)

    rospy.spin()


if __name__ == '__main__':
    try:
        rosMain()
    except rospy.ROSInterruptException:
        pass