#!/usr/bin/env python

import rospy
import math
from race.srv import *
from race.msg import pid_input
from race.msg import wall_dist  #x, distance; theta, radians

desired_trajectory = 0.6
vel = 9

pub = rospy.Publisher('error', pid_input, queue_size=10)



def callback(data):
    rospy.wait_for_service('corner')
    try:
        corner_service = rospy.ServiceProxy('corner', corner_loc)
        corner_data = corner_service()
    except rospy.ServiceException, e:
        print "service call failed: " + str(e)



    error = data.distance - desired_trajectory + data.theta


    msg = pid_input()
    msg.pid_error = error
    msg.pid_vel = vel
    pub.publish(msg)




if __name__ == "__main__":
    rospy.init_node("wall_follower", anonymous = True)
    rospy.Subscriber("wall_distance", wall_dist, callback)
    rospy.spin()
