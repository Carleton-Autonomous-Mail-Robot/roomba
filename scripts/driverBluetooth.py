#!/usr/bin/env python

import rospy
from bluepy.btle import Scanner
from std_msgs.msg import String

__measured_power = -65.72 #hardcoded, make some sort of beacon object
__enviromental = 1.201020985239786 #hardcoded, make some sort of beacon object
__known_MACS = ['fc:e2:2e:62:9b:3d','ea:2f:93:a6:98:20'] #hardcoded, please make config file

'''
    Read RSSIs using bluepy library,
    returns RSSIs in a dictionary with MAC addresses as the key
'''
def __read_RSSI():
    ble_list = Scanner().scan(1.0)
    found_beacons = dict()
    for dev in ble_list:
        if dev.addr in __known_MACS:
            found_beacons[dev.addr] = dev.rssi
    return found_beacons



'''
    Calculates distances from given RSSIs
    returns dictionary of distances with MAC addresses as the keys
'''
def __get_distance():
    read_rssi = __read_RSSI()
    MAC_ADDRs = read_rssi.keys()
    if len(MAC_ADDRs) == 0:
        return None

    distances = dict()
    for MAC in MAC_ADDRs:
        distances[MAC] = pow(10,(__measured_power - read_rssi[MAC])/(10*__enviromental))
    
    return distances




def rosMain():
    pub = rospy.Publisher('beacons', String, queue_size=100)
    rospy.init_node('bluetoothBeacons', anonymous=True)
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        current_distances = __get_distance()
        if current_distances is None:
            pass
        else:
            MAC_ADDRs = current_distances.keys()
            for MAC in MAC_ADDRs:
                rospy.loginfo('Beacon: '+str(MAC)+','+str(current_distances[MAC])+'m')
                pub.publish(str(MAC) + ':' + str(current_distances[MAC]))
        rate.sleep()

if __name__ == '__main__':
    try:
        rosMain()
    except rospy.ROSInterruptException:
        pass