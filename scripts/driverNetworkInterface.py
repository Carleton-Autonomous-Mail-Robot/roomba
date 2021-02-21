#!/usr/bin/env python
import requests 
from reader import ServerReader
import rospy
from std_msgs.msg import String


def __new_client():
    reader = ServerReader()
    if not reader.read_client_id() == '':
        rospy.loginfo("Client ID read from file: "+reader.read_client_id())
        return

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
    if id is '':
        pass
    else:
        #rospy.loginfo('Making Request under client_id:'+__client_info())
        res = __make_request({
            "status": "good",
            "opperation":"getMessage",
            "clientID": str(id)
        })
        return res.json()['payload']
    return None
    

def __make_request(json={}):
    reader = ServerReader()
    url = reader.get_url()
    rospy.loginfo('Making a request to: '+url)
    return requests.post(url,json=json)

def rosMain():
    pub = rospy.Publisher('network', String, queue_size=5)
    rospy.init_node('networkDriver', anonymous=True)
    rate = rospy.Rate(100)
    __new_client()

    while not rospy.is_shutdown():
        msg = __check_mail()
        if msg is "Not Found" or msg is None:
            continue
        rospy.loginfo('network('+msg+')')
        pub.publish(msg)

if __name__ == '__main__':
    try:
        rosMain()
    except rospy.ROSInterruptException:
        pass
