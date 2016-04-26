#!/usr/bin/env python
import rospy
from std_msgs.msg import String

message_received = False
message = 0

def talker_callback(data):
	message_received = True
	message = data.data

def talker():
	pub = rospy.Publisher('drive_parameters', String, queue_size=10)
	rospy.init_node('talker', anonymous=True)
	rospy.Subscriber('drive_parameters', String, talker_callback) 
	rospy.spin()
	while True:
		if message_received:
			message_received = False
			pub.publish(message)

if __name__ == '__main__':
	try:
		talker()
	except rospy.ROSInterruptException:
		pass
