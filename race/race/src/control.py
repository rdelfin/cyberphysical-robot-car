#!/usr/bin/env python

import rospy
from race.msg import drive_param
from race.msg import pid_input

kp = 14.0
kd = 0.09
servo_offset = 18.5
prev_error = 0.0 
vel_input = 15.0

pub = rospy.Publisher('drive_parameters', drive_param, queue_size=1)

def control(data):
	global prev_error
	global vel_input
	global kp
	global kd

	scaling_factor = 10

	## Your code goes here
	# 1. Scale the error
	# 2. Apply the PID equation on error
	# 3. Make sure the error is within bounds
 	error = data.pid_error*scaling_factor
	angle = kp*error+kd*(prev_error - error)
	#deriv = kd*(error-prev_error)
	if(angle < -100):
		angle = -100
	if(angle > 100):
		angle = 100
	
	prev_error = data.pid_error
	## END

	msg = drive_param();
	msg.velocity = vel_input	
	msg.angle = angle
	pub.publish(msg)

if __name__ == '__main__':
	print("Listening to error for PID")
	kp = input("Enter Kp Value: ")
	kd = input("Enter Kd Value: ")
	vel_input = input("Enter Velocity: ")
	rospy.init_node('pid_controller', anonymous=True)
	rospy.Subscriber("error", pid_input, control)
	rospy.spin()
