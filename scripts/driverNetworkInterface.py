import requests 

__URL = 'localhost:5000/'

def __get_client_json():
    return {"status": "good",
            "opperation": "newClient"}

def __client_info():
    return None

def __check_mail():
    if __client_info() is None:
        res = requests.post(url)

def rosMain():
    pub = rospy.Publisher('network', String, queue_size=5)
    rospy.init_node('networkDriver', anonymous=True)
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        rate.sleep()

if __name__ == '__main__':
    try:
        rosMain()
    except rospy.ROSInterruptException:
        pass