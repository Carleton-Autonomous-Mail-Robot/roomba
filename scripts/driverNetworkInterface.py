#!/usr/bin/env python

import requests 
from reader import ServerReader
import rospy
from std_msgs.msg import String

SERVER = 'https://web-services-mail.herokuapp.com'


def __new_client():
    reader = ServerReader()
    res = requests.get(SERVER+"/newClient?robot=yes")
    rospy.loginfo("Client ID Registered: "+str(res.json()['clientID']))
    reader.write_client_id(str(res.json()['clientID']))
    

def __client_info():
    return None

def __check_mail():
    if __client_info() is None:
        reader = ServerReader()
        clientID = reader.read_client_id()
        res = __get_request('getMessage',clientID)
        return res.json()['payload']


def __get_request(endpoint,clientID):
    return requests.get(SERVER+"/"+endpoint+'?clientID='+clientID)

    

def __make_request(endpoint,clientID,json={}):
    reader = ServerReader()
    url = reader.get_url()
    #rospy.loginfo('Making a request to: '+url)
    return requests.post(SERVER+'/'+endpoint+'?clientID='+clientID,json=json)

def rosMain():
    pub = rospy.Publisher('inbox', String, queue_size=5)
    rospy.init_node('networkDriver', anonymous=True)
    rate = rospy.Rate(10)
    __new_client()

    while not rospy.is_shutdown():
        mail = __check_mail()
        if not mail is None:
            rospy.loginfo(mail)
            pub.publish(mail)

        rate.sleep()

if __name__ == '__main__':
    try:
        rosMain()
    except rospy.ROSInterruptException:
        pass
