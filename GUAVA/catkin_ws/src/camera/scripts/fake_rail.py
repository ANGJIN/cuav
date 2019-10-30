#! /usr/bin/env python3

import rospy
from std_msgs.msg import String

print('fake_rail')
rospy.init_node("fake_rail")
pub = rospy.Publisher('operate', String, queue_size=1)
rate = rospy.Rate(5)
while not rospy.is_shutdown():
    print("rail start")
    pub.publish("start")
    rospy.sleep(8)
    # rate.sleep()
    print("rail end")
    pub.publish("end")
    # rate.sleep()
    rospy.sleep(1)
