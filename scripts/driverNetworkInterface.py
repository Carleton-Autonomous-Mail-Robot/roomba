#!/usr/bin/env python
import requests 
from reader import ServerReader
import rospy
from std_msgs.msg import String

url = ""

def __new_client():
    res = __make_request({"status": "good",
            "opperation": "newClient",
            "payload": "robot"})
    rospy.loginfo(res.json())
    

def __client_info():
    return None

def __check_mail():
    if __client_info() is None:
        res = requests.post(url)

def __make_request(json={}):
    return requests.post(url,json=json)

def rosMain():
    reader = ServerReader()
    url = reader.get_url()
    pub = rospy.Publisher('network', String, queue_size=5)
    rospy.init_node('networkDriver', anonymous=True)
    rate = rospy.Rate(10)
    __new_client()

    while not rospy.is_shutdown():
        rate.sleep()

if __name__ == '__main__':
    try:
        rosMain()
    except rospy.ROSInterruptException:
        pass