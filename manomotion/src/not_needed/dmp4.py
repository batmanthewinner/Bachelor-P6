#!/usr/bin/env python
import roslib; 
roslib.load_manifest('dmp')
import rospy 
import numpy as np
#from dmp import *
from dmp.srv import *
from dmp.msg import *
from moveit_msgs.msg import RobotState, PositionIKRequest
from geometry_msgs.msg import PoseStamped, Pose, Point, Quaternion
from std_msgs.msg import Header
from sensor_msgs.msg import JointState

rospy.init_node("test", anonymous=True)
cartesian_goal = [0.5, 0.5, 0.5, 0, 0, 0, 1]

	
msg = PositionIKRequest
msg.pose_stamped = PoseStamped
msg.pose_stamped.header = Header
msg.pose_stamped.pose = Pose
msg.pose_stamped.pose.position = Point
msg.pose_stamped.pose.orientation = Quaternion

msg.group_name = "right_arm"
	

#print msg.robot_state
msg.avoid_collisions = True 
msg.ik_link_name = "ra_wrist_3_joint"
 
	
#header
#msg.pose_stamped.header.seq = PoseStamped()
msg.pose_stamped.header.frame_id = "ra_wrist_3_joint"	
msg.pose_stamped.header.stamp = rospy.Time.now() #Note you need to call rospy.init_node() before this will work

#point
msg.pose_stamped.pose.position.x = cartesian_goal[0]
msg.pose_stamped.pose.position.y = cartesian_goal[1]
msg.pose_stamped.pose.position.z = cartesian_goal[2]

#pose 
msg.pose_stamped.pose.orientation.x = cartesian_goal[3]
msg.pose_stamped.pose.orientation.y = cartesian_goal[4]
msg.pose_stamped.pose.orientation.z = cartesian_goal[5]
msg.pose_stamped.pose.orientation.w = cartesian_goal[6]
	


#request service
rospy.ServiceProxy('/compute_ik', msg)
	  







