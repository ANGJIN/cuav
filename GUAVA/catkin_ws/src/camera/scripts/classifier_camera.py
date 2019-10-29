#!/usr/bin/env python3

import cv2
import rospy
from std_msgs.msg import String
from camera.msg import sendframe
from cv_bridge import CvBridge, CvBridgeError


class ClassifierCamera:
	def __init__(self):
		self.detected_frames = []
		self.detected_objects = []
		self.detected_percentages = []
		self.bridge = CvBridge()
		self.send_frame = sendframe()
		self.classify = rospy.Subscriber('img_camera', sendframe, classifier_camera.callback)
		self.realtime = rospy.Publisher('realtime_camera', sendframe, queue_size=10)
		self.summary = rospy.Publisher('summary_camera', sendframe, queue_size=10)


	def preprocess_frames(self):
		try:
			for o, p in zip(self.detected_objects, self.detected_percentages):
				print(o,p)
			return self.detected_frames[0], self.detected_objects[0], self.detected_percentages[0]
		except EOFError:
			print("EOF error")

	def realtime_callback(self, frame_data):
		print("Send frame in realtime")
		try:
			cv_image = self.bridge.imgmsg_to_cv2(frame_data.frame, "bgr8")
			cv2.imshow("YOLO", cv_image)
			print(frame_data.object)
			print(frame_data.percentage)
		except CvBridgeError as e:
			print(e)

		# accumulate detected frames + labels + percentages
		self.detected_frames.append(cv_image)
		self.detected_objects.append(frame_data.object)
		self.detected_percentages.append(frame_data.percentage)

	def summary_callback(self, frame_data):
		print("Send summarized frame")
		
		# preprocess summarized data
		frame, self.send_frame.object, self.send_data.percentage = self.preprocess_frames()

		try:   
			self.send_frame.operate = frame_data.operate
			self.send_frame.frame = self.bridge.cv2_to_imgmsg(frame, "bgr8")
			self.summary.publish(self.send_frame)
		except CvBridgeError as e:
			print(e)

		print("SUMMARY CALLBACK")
		print(send_data.object)
		print(send_data.percentage)

		# empty data
		self.detected_frames.clear()
		self.detected_objects.clear()
		self.detected_percentage.clear()

	def callback(self, data):

		print("Start classifier camera")
		if data.operate == "start":
			self.realtime_callback(data)
		elif data.operate == "end":
    			
			self.summary_callback(data)
    			

if __name__ == '__main__':
	classifier_camera = ClassifierCamera()
	rospy.init_node('classifier_camera', anonymous=True)
	try:
		rospy.spin()
	except KeyboardInterrupt:
		print("Shut down - keyboard interruption")

