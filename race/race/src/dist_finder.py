#!/usr/bin/env python

import rospy
import math
from sensor_msgs.msg import LaserScan
from race.msg import wall_dist
from race.srv import *

#desired_trajectory = 0.5 
#vel = 30

#pub = rospy.Publisher('error', pid_input, queue_size=10)
pub = rospy.Publisher('wall_distance', wall_dist, queue_size=10)


##	Input: 	data: Lidar scan data
##			theta: The angle at which the distance is requried
##	OUTPUT: distance of scan at angle theta
def getRange(data,theta):
# Find the index of the array that corresponds to angle theta.
# Return the lidar scan value at that index
# Do some error checking for NaN and absurd values
	theta += 45
	theta = math.radians(theta)
	newTheta = data.ranges[(int)((1/data.angle_increment)*theta)]
	if(newTheta > data.angle_max or newTheta < data.angle_min):
		return None
	else:
		return newTheta

def callback(data):
        rospy.wait_for_service('corner')
        try:
        	corner_service = rospy.ServiceProxy('corner', corner_loc)
        	corner_data = corner_service()
        except rospy.ServiceException, e:
    		print "Service Call Failed: " + str(e)



	distance = 0
	alpha = 0
	theta = 50;
	a = getRange(data,theta)
	b = getRange(data,0)
		
	swing = math.radians(theta)
	
	print "Data a: " + str(a)
	print "Data b: " + str(b)
	
	if(a != None and b != None):
		# Calculate distance to wall
		alpha = math.atan((a*math.cos(swing) - b)/(a*math.sin(swing)))
		distance = b*math.cos(alpha)

		# Include offset caused by 
		distance = distance + 0*math.sin(alpha)
		print "Calculated Distance: " + str(distance)
	
	## END

	msg = wall_dist()
	msg.distance = distance
	msg.theta = alpha
	pub.publish(msg)

if __name__ == '__main__':
	print("Laser node started")
	rospy.init_node('dist_finder',anonymous = True)
	rospy.Subscriber("scan",LaserScan,callback)
	rospy.spin()
