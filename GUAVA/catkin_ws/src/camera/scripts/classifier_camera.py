#!/usr/bin/env python3

import time
import cv2
import rospy
from std_msgs.msg import String
from camera.msg import sendframe, sendsummary
from cv_bridge import CvBridge, CvBridgeError
from camera_log import log_generator
from process_img import ProcessImage


class ClassifierCamera:
	def __init__(self, node_name, pub_log):
		rospy.Subscriber('img_camera', sendframe, self.callback)
		self.realtime = rospy.Publisher('realtime_camera', sendframe, queue_size=3)
		self.summary = rospy.Publisher('summary_camera', sendsummary, queue_size=3)
		self.log = pub_log
		self.node_name = node_name
		self.total_frames = 0
		self.det_frames = []
		self.det_percentages = []
		self.det_coords = []
		self.bridge = CvBridge()
		self.frame_data = sendsummary()
		self.processor = ProcessImage()

	def callback(self, data):
		# if object is detected, convert ros message to cv_frame
		# append data to class variables
		if data.coords:
			self.accumulate_detections(data.frame, data.percent, data.coords)

		self.total_frames += 1
		if data.operate == "start":
			self.log.publish(log_generator(self.node_name, "img_camera(rail operating)", "sub"))
			self.realtime_callback(data)

		elif data.operate == "end":
			self.log.publish(log_generator(self.node_name, "img_camera(rail ended)", "sub"))
			self.summary_callback(data)

	# publish subscribed data directly
	def realtime_callback(self, sub_data):
		self.realtime.publish(sub_data)
		self.log.publish(log_generator(self.node_name, "realtime_camera", "pub"))
		print(sub_data.percent, sub_data.coords)

	# process accumulated detection data
	# and the publish summarized information
	def summary_callback(self, sub_data):
		# process summarized data
		frame, self.frame_data.direction, self.frame_data.percent = \
			self.processor.process_summary(self.det_frames, self.det_coords, self.det_percentages, self.total_frames)
		print("Summarized Result - ", self.frame_data.direction, self.frame_data.percent)

		# if no detection at all, send last frame to summary
		if frame is None:
			self.frame_data.frame = sub_data.frame
			cv2.putText(frame, self.frame_data.direction, (40, 40), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 0), 2)
		else:
			try:
				self.frame_data.frame = self.bridge.cv2_to_imgmsg(frame, encoding="passthrough")
			except CvBridgeError as e:
				print(e)

		# save image file
		fileName = time.strftime("%Y%m%d_%H%M%S")
		directory = '/home/project/cuav/GUAVA/catkin_ws/src/camera/'
		cv2.imwrite(directory + fileName + '_image.jpg', frame)
		print("image saved")

		self.summary.publish(self.frame_data)
		self.log.publish(log_generator(self.node_name, "summary_camera", "pub"))

		# empty data
		self.det_frames.clear()
		self.det_percentages.clear()
		self.det_coords.clear()
		self.total_frames = 0

	# accumulate detection information
	def accumulate_detections(self, fr, per, cor):
		try:
			cv_image = self.bridge.imgmsg_to_cv2(fr, desired_encoding="passthrough")
			self.det_frames.append(cv_image)
			self.det_percentages.append(per)
			self.det_coords.append(cor)
		except CvBridgeError as e:
			print(e)


if __name__ == '__main__':
	rospy.init_node('classifier_camera', anonymous=True)
	log = rospy.Publisher('logs', String, queue_size=10)
	time.sleep(2)
	log.publish(log_generator("classifier_camera", "Start classifier_camera"))
	classifier_camera = ClassifierCamera('classifier_camera', log)
	time.sleep(2)
	try:
		rospy.spin()
	except KeyboardInterrupt:
		print("Shut down - keyboard interruption")
