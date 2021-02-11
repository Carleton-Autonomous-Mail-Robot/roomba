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
def zone(dictionary_macs):
    macs = dictionary_macs.keys()

    if 'ea:2f:93:a6:98:20' in macs and 'fc:e2:2e:62:9b:3d' in macs:
        if dictionary_macs['fc:e2:2e:62:9b:3d'] > 4.5 and dictionary_macs['ea:2f:93:a6:98:20'] > 4.5:
            rospy.loginfo('AB')
    if 'ea:2f:93:a6:98:20' in macs and dictionary_macs['ea:2f:93:a6:98:20'] < 4.5:
        rospy.loginfo('A')
    if 'fc:e2:2e:62:9b:3d' in macs and dictionary_macs['fc:e2:2e:62:9b:3d'] < 4.5:
        rospy.loginfo('B')
    rospy.loginfo('Zone was called and nothing happened')

    
def read_bluetooth(str_in):
    split_lines = str_in.data.splitlines() #splits the published data on new line
    dict_macs = dict()
    for line in split_lines: #iterates through the lines
        tmp = line.split(',') #splits line of formate MAC,distance along the period
        dict_macs[tmp[0]] = float(tmp[1])

    if len(dict_macs) == 0:
        return
    zone(dict_macs)
    




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