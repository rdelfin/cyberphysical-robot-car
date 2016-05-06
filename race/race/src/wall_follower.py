#!/usr/bin/env python

import rospy
import math
from race.srv import *
from race.msg import pid_input
from race.msg import wall_dist  #x, distance; theta, radians

desired_trajectory = 0.6
vel = 9
turnMode = False

pub = rospy.Publisher('error', pid_input, queue_size=10)



def callback(data):
    global turnMode
    rospy.wait_for_service('corner')
    try:
        corner_service = rospy.ServiceProxy('corner', corner_loc)
        corner_data = corner_service()
    except rospy.ServiceException, e:
        print "service call failed: " + str(e)
    
    if(turnMode):
        error = 1
        
        if(not (corner_data.found)):
            turnMode = False
    else:
        error = data.distance - desired_trajectory + data.theta
        
        if(corner_data.found and corner_data.y < 0.3):
            turnMode = True



    msg = pid_input()
    msg.pid_error = error
    msg.pid_vel = vel
    pub.publish(msg)




if __name__ == "__main__":
    rospy.init_node("wall_follower", anonymous = True)
    rospy.Subscriber("wall_distance", wall_dist, callback)
    rospy.spin()
