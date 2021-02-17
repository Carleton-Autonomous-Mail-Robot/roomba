#!/usr/bin/env python
'''

@author Gabriel Ciolac
@last-edit 2021/02/10-21:39
@contributers 
'''
import rospy
from bluepy.btle import Scanner
from std_msgs.msg import String
from reader import BeaconReader

__measured_power = -59 #hardcoded, make some sort of beacon object
__enviromental = 2.688683131805121 #hardcoded, make some sort of beacon object
__known_MACS = ['fc:e2:2e:62:9b:3d','ea:2f:93:a6:98:20'] #hardcoded, please make config file

'''
    Read RSSIs using bluepy library,
    returns RSSIs in a dictionary with MAC addresses as the key
'''
def __read_RSSI():
    reader = BeaconReader()
    ble_list = Scanner().scan(0.5)
    found_beacons = dict()
    for dev in ble_list:
        if dev.addr in reader.read_beacons().keys():
            found_beacons[dev.addr] = dev.rssi
    return found_beacons



'''
    Calculates distances from given RSSIs
    returns dictionary of distances with MAC addresses as the keys
'''
def __get_distance():
    reader = BeaconReader()
    read_rssi = __read_RSSI()
    MAC_ADDRs = read_rssi.keys()
    if len(MAC_ADDRs) == 0:
        return None

    distances = dict()
    for MAC in MAC_ADDRs:
        distances[MAC] = pow(10,(reader.read_beacons()[MAC][2] - read_rssi[MAC])/(10*reader.read_beacons()[MAC][1]))
    
    return distances




def rosMain():
    pub = rospy.Publisher('beacons', String, queue_size=5)
    rospy.init_node('bluetoothBeacons', anonymous=True)
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        current_distances = __get_distance()
        if current_distances is None:
            pass
        else:
            MAC_ADDRs = current_distances.keys()
            to_send = ''
            for MAC in MAC_ADDRs:
                rospy.loginfo('Beacon: '+str(MAC)+','+str(current_distances[MAC])+'m')
                to_send = to_send +str(MAC)+','+str(current_distances[MAC]) + '\n'
            pub.publish(to_send)
        rate.sleep()

if __name__ == '__main__':
    try:
        rosMain()
    except rospy.ROSInterruptException:
        pass