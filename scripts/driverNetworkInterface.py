#!/usr/bin/env python
import requests 
from reader import ServerReader
import rospy
from std_msgs.msg import String


def __new_client():
    reader = ServerReader()
    res = __make_request({"status": "good",
            "opperation": "newClient",
            "payload": "robot"})
    rospy.loginfo("Client ID Registered: "+str(res.json()['clientID']))
    reader.write_client_id(str(res.json()['clientID']))
    

def __client_info():
    reader = ServerReader()
    return reader.read_client_id()

def __check_mail():
    id = __client_info()
    if __client_info() is '':
        pass
    else:
        res = __make_request({
            "status": "good",
            "opperation":"getMessage",
            "clientID": __client_info()
        })
        return res.json()['payload']
    return None
    

def __make_request(json={}):
    reader = ServerReader()
    url = reader.get_url()
    rospy.loginfo('Making a request to: '+url)
    return requests.post("https://web-services-mail.herokuapp.com/",json=json)

def rosMain():
    pub = rospy.Publisher('network', String, queue_size=5)
    rospy.init_node('networkDriver', anonymous=True)
    rate = rospy.Rate(10)
    __new_client()

    while not rospy.is_shutdown():
        msg = __check_mail()
        if msg is None:
            continue
        rospy.loginfo('network('+msg+')')
        pub.publish(msg)

if __name__ == '__main__':
    try:
        rosMain()
    except rospy.ROSInterruptException:
        pass