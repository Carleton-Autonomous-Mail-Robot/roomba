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



averages = dict()

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
        distances[MAC] = pow(10,(reader.read_beacons()[MAC][1] - read_rssi[MAC])/(10*reader.read_beacons()[MAC][0]))
    
    return distances

def __calc_average(mac, distance):
    global averages
    
    averages[mac].insert(0, distance)
    averages[mac].pop(5)
    avg = sum(averages[mac])/5
    if distance < avg * 1.25 and distance > avg * 0.75:
        return True
    return False

def rosMain():
    global averages
    
    pub = rospy.Publisher('beacons', String, queue_size=5)
    rospy.init_node('bluetoothBeacons', anonymous=True)
    rate = rospy.Rate(10)
    
    reader = BeaconReader()
    beacons = reader.read_beacons()
    
    for n in beacons: 
        averages[n] = [0, 0, 0, 0, 0]
    
    while not rospy.is_shutdown():
        
        # Get sums of 10 samples
        samples = 0
        sumDist = dict()
        while (samples < 10)
            distances = __get_distance()
            # Do it for every different beacon
            for mac in distances.keys():
                sumDist[mac] += distances[mac]
            rate.sleep()
            samples += 1
        
        # Find average of 10 samples (1 per second)
        avg = dict()
        for mac in sumDist:
            avg[mac] = sumDist[mac]/10
        
        # Construct message to publish and filter outlier
        MAC_ADDRs = avg.keys()
        to_send = ''
        for MAC in MAC_ADDRs:
            outlier = __calc_average(MAC, avg[MAC])
            if not outlier:
                rospy.loginfo('Beacon: '+str(MAC)+','+str(avg[MAC])+'m')
                to_send = to_send +str(MAC)+','+str(avg[MAC]) + '\n'
        
        # If at least 1 beacon wasnt an outlier, then publish
        if not to_send == '':
            pub.publish(to_send)
            
        rate.sleep()

if __name__ == '__main__':
    try:
        rosMain()
    except rospy.ROSInterruptException:
        pass



