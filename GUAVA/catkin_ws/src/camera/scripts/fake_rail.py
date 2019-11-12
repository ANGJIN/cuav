#! /usr/bin/env python3

import rospy
from std_msgs.msg import String
from main.msg import operate

print('fake_rail')
rospy.init_node("fake_rail")
pub = rospy.Publisher('operate', operate, queue_size=1)
rate = rospy.Rate(5)
rospy.sleep(10)
op = operate()
while not rospy.is_shutdown():
    rospy.sleep(3)
    print("rail start")
    op.command = "start"
    op.direction = True
    pub.publish(op)
    rospy.sleep(60)
    print("rail end")
    op.command = "end"
    op.direction = True
    pub.publish(op)
    rospy.sleep(1)
