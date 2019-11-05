#!/usr/bin/env python3
#-*-coding:utf-8-*-

import rospy
from std_msgs.msg import String
from datetime import datetime
from radar.msg import raw
import time

# from main.msg import result


# raw data from raw topic in radar
def callback_raw(data,args):
	pub_log = args
	fileNmae = time.strftime("%Y%m%d_%H%M%S") + '_binary.txt'
	directory = '/home/project/cuav/GUAVA/catkin_ws/src/main/logs/storage/raw/'
	binary_data = open(directory+fileNmae, 'wb')

	received_data = bytearray()
	received_data = data.data

	lengthMSb = bytes([11025 >> 8])
	lengthLSb = bytes([11025 & 0xFF])
	binary_data.write(lengthMSb + lengthLSb + data)
	binary_data.close()

	# log
	str_time = str(datetime.now()).replace(' ', '_')
	log = '[{}/{}][{}] {}'.format('main', 'storage', str_time, 'raw data file from radar <' + fileNmae + '> is saved.')
	pub_log.publish(log)
	print(log)




def callback_result(data,args):
	pub_log = args
	rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
	#publish/subscribe log
	str_time2 = str(datetime.now()).replace(' ','_')
	log_result ='[{}/{}][{}][{}] {}'.format('main','storage','SUB',str_time2,"Get Message From <result> topic : "+data.data)
	pub_log.publish(log_result)
	print(log_result)
	
	# assign the value from parameter(message) to local variable #
	#							     #
	# class = data.class					     #
	# img = data.img					     #
	# ....							     #
	##############################################################

	# make file for backup
	
	now = datetime.now() # current time for filename
	f = open('/home/project/cuav/GUAVA/catkin_ws/src/main/storage/'+str(now)+'.dat','w')
	test_str = ["for test", "teeeeest"]
	test_str.append(data.data)
	f.write('\n'.join(test_str))
	f.close()

def storage(pub_log):

	rospy.init_node('storage', anonymous=True)

	# log
	str_time = str(datetime.now()).replace(' ', '_')
	log = '[{}/{}][{}] {}'.format('main', 'storage', str_time, 'storage node is initialized..')
	print(log)
	pub_log.publish(log)

	rospy.Subscriber('result', String, callback_result, pub_log)
	rospy.Subscriber('raw', raw, callback_raw, pub_log)
	rospy.spin()

if __name__ == '__main__':
	pub_log = rospy.Publisher('logs', String, queue_size=10)

	storage(pub_log)
