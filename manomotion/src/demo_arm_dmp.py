#!/usr/bin/env python


import roslib; 
roslib.load_manifest('dmp')
import rospy 
import numpy as np
from dmp.srv import *
from dmp.msg import *
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
import tf
import sys
import copy
from std_msgs.msg import String

def init():
	
	global phone_info
	phone_info = [0,0,0,0,0,0]	

	global robot
	robot = moveit_commander.RobotCommander()

	global group
	group = moveit_commander.MoveGroupCommander("right_arm")

    	global hand_subs
    	hand_subs = rospy.Subscriber("chatter", String, phone_callback)
    	rospy.sleep(1)

	global waypoints_from_phone
	waypoints_from_phone = []

	global get_x_y_z
	get_x_y_z = []

	global group
	group = moveit_commander.MoveGroupCommander("right_arm")


	global starting_pose
	starting_pose = geometry_msgs.msg.Pose()	
	starting_pose.position.x = 0.0
	starting_pose.position.y = 0.5
	starting_pose.position.z = 0.5
	starting_pose.orientation.w = 0.707
	starting_pose.orientation.x = 0.0
	starting_pose.orientation.y = 0.0
	starting_pose.orientation.z = 0.707

	global starting_pose
	starting_pose = geometry_msgs.msg.Pose()	
	starting_pose.position.x = 0.0
	starting_pose.position.y = 0.85
	starting_pose.position.z = 0.30
	starting_pose.orientation.w = 0.707
	starting_pose.orientation.x = 0.0
	starting_pose.orientation.y = 0.0
	starting_pose.orientation.z = 0.707

	execute_pose(starting_pose)


def phone_callback(data):
	global phone_info
	phone_info = [float(i) for i in data.data.split('_')]



 
 
 #Set a DMP as active for planning
def makeSetActiveRequest(dmp_list):
     try:
         sad = rospy.ServiceProxy('set_active_dmp', SetActiveDMP)
         sad(dmp_list)
     except rospy.ServiceException, e:
         print "Service call failed: %s"%e
 
 
 #Generate a plan from a DMP
def makePlanRequest(x_0, x_dot_0, t_0, goal, goal_thresh, 
                     seg_length, tau, dt, integrate_iter):
     print "Starting DMP planning..."
     rospy.wait_for_service('get_dmp_plan')
     try:
         gdp = rospy.ServiceProxy('get_dmp_plan', GetDMPPlan)
         resp = gdp(x_0, x_dot_0, t_0, goal, goal_thresh, 
                    seg_length, tau, dt, integrate_iter)
     except rospy.ServiceException, e:
         print "Service call failed: %s"%e
     print "DMP planning done"   
             
     return resp;


def execute_pose(pose):
	group.set_pose_target(pose)
	plan1 = group.plan()
	group.execute(plan1, wait = False)






if __name__ == '__main__':
	init()
	rospy.init_node('demo_arm_dmp')

	resp_list = np.load('resp.dmp_list.npy')
	resp_tau  = np.load('resp.tau.npy')
	
	#Set it as the active DMP
	makeSetActiveRequest(resp_list)
	#Get current endeffector pose 
    	#rospy.init_node('tf_ra_listener')
	
    	listener = tf.TransformListener()

	while True: 
		#get the current pose of the endeffector
	    	#listener.waitForTransform('/world', '/ra_ee_link', rospy.Time(), rospy.Duration(4.0))
	     	now = rospy.Time.now()
		rospy.sleep(0.01)
	     	listener.waitForTransform('/world', '/ra_ee_link', now, rospy.Duration(4.0))
	     	(trans,rot) = listener.lookupTransform('/world', '/ra_ee_link', rospy.Time(0)) 
	     	print trans, rot
	
	     	#Now, generate a plan
	     	x_0 = [trans[0], trans[1], trans[2], rot[0], rot[1], rot[2], rot[3]]          #Plan starting at a different point than demo 
	     	x_dot_0 = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]   
	     	t_0 = 0                
	     	goal = [starting_pose.position.x + phone_info[2] * 2.5, 
starting_pose.position.y + phone_info[3] * 2.5,
phone_info[4] * 0.66,
starting_pose.orientation.w ,
starting_pose.orientation.x , 
starting_pose.orientation.y ,
starting_pose.orientation.z ]   #Plan to a different goal than demo
	     	goal_thresh = [0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001]
	     	seg_length = -1          #Plan until convergence to goal
	     	tau = resp_tau       #Desired plan should take twice as long as demo
	     	dt = 1.0
	     	integrate_iter = 5       #dt is rather large, so this is > 1  
	     	plan = makePlanRequest(x_0, x_dot_0, t_0, goal, goal_thresh, 
		                    seg_length, tau, dt, integrate_iter)
	 
	     	#print plan, type(plan)
		a_points = []	

		for i in plan.plan.points:
			next_pose = geometry_msgs.msg.Pose() 
			#next_pose.position.x = plan.plan.points[0].velocities
			#next_pose.position.x = plan.plan.points[].positions
			next_pose.position.x = i.positions[0]
			next_pose.position.y = i.positions[1]
			next_pose.position.z = i.positions[2]
			next_pose.orientation.x = i.positions[3]
			next_pose.orientation.y = i.positions[4]
			next_pose.orientation.z = i.positions[5]
			next_pose.orientation.w = i.positions[6]
	  
			#b = plan.plan.points[0].positions
		
			a_points.append(next_pose)
		
		(plan2, fraction) = group.compute_cartesian_path(
			a_points,   # waypoints to follow
			0.01,        # eef_step
			0.0)         # jump_threshold	
	
	
		group.execute(plan2, wait = False)
