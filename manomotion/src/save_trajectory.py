#!/usr/bin/env python

from moveit_msgs.msg import RobotTrajectory
import sys
import rospy
from sr_robot_commander.sr_hand_commander import SrHandCommander
from sr_utilities.hand_finder import HandFinder
from std_msgs.msg import String
import time 
import math
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from sr_robot_commander.sr_arm_commander import SrArmCommander
from sr_robot_commander.sr_arm_commander import *


s = "1_-1"
#rospy.init_node("basic_hand_examples", anonymous=True)
rospy.init_node('listener2', anonymous=True)
arm_commander = SrArmCommander(set_ground=False)
reference_frame = arm_commander.get_pose_reference_frame()
#hand_finder = HandFinder()
#hand_parameters = hand_finder.get_hand_parameters()
#hand_serial = hand_parameters.mapping.keys()[0]
#hand_commander = SrHandCommander(hand_parameters=hand_parameters,hand_serial=hand_serial)
#hand_mapping = hand_parameters.mapping[hand_serial]
#joints = hand_finder.get_hand_joints()[hand_mapping]
print "this", #SrArmCommander.get_end_effector_pose_from_state()		
a = 2
print("Setup Done.")

new_position = [0.5, 0.5, 0.5, 0.0, 0.0, 0.0]

plan = arm_commander.plan_to_position_target(new_position)

new_position = [0.5, 0.5, 1.0, 0.0, 0.0, 0.0]

plan = arm_commander.plan_to_position_target(new_position)

print "Planning frame: ", arm_commander.get_planning_frame()

print("plan")
print("this is the plan", plan)
