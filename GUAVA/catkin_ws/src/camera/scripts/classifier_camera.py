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
		self.classify = rospy.Subscriber('img_camera', sendframe, self.callback)
		self.realtime = rospy.Publisher('realtime_camera', sendframe, queue_size=3)
		self.summary = rospy.Publisher('summary_camera', sendframe, queue_size=3)

	def preprocess_frames(self):
		try:
			for o, p in zip(self.detected_objects, self.detected_percentages):
				print(o, p)
			return self.detected_frames[0], self.detected_objects[0], self.detected_percentages[0]
		except EOFError:
			print("EOF error")

	def realtime_callback(self, frame_data):
		print("Send frame in realtime")
		# self.realtime.publish(frame_data)
		try:
                    cv_image = self.bridge.imgmsg_to_cv2(frame_data.frame, encoding="bgr8")
		except CvBridgeError as e:
			print(e)

		cv2.imshow("Frame", cv_image)

		# accumulate detected frames + labels + percentages
		# self.detected_frames.append(cv_image)
		self.detected_objects.append(frame_data.object)
		self.detected_percentages.append(frame_data.percent)

	def summary_callback(self, frame_data):
		print("Send summarized frame")
		
		# preprocess summarized data
		frame, self.send_frame.object, self.send_frame.percent = self.preprocess_frames()

		try:   
			self.send_frame.operate = frame_data.operate
			self.send_frame.frame = self.bridge.cv2_to_imgmsg(frame, "bgr8")
			self.summary.publish(self.send_frame)
		except CvBridgeError as e:
			print(e)

		print("SUMMARY CALLBACK")

		# empty data
		self.detected_frames.clear()
		self.detected_objects.clear()
		self.detected_percentages.clear()

	def callback(self, data):

		print("Start classifier camera")
		if data.operate == "start":
			self.realtime_callback(data)
		elif data.operate == "end":
			pass
			# self.summary_callback(data)


if __name__ == '__main__':
	classifier_camera = ClassifierCamera()
	rospy.init_node('classifier_camera', anonymous=True)
	try:
		rospy.spin()
	except KeyboardInterrupt:
		print("Shut down - keyboard interruption")

