#!/usr/bin/env python3

import sys
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
from tf.transformations import quaternion_from_euler
from math import pi

def move_to_position(target_x, target_y, target_z):
    moveit_commander.roscpp_initialize(sys.argv)
    rospy.init_node('move_jaco_test', anonymous=True)

    robot = moveit_commander.RobotCommander()
    scene = moveit_commander.PlanningSceneInterface()
    group_name = "arm"
    move_group = moveit_commander.MoveGroupCommander(group_name)

    # Define the target pose
    target_pose = geometry_msgs.msg.Pose()
    target_pose.position.x = target_x
    target_pose.position.y = target_y
    target_pose.position.z = target_z

    roll = 0 # Your desired roll angle in radians
    pitch = pi/2  # 90-degree rotation around the Y-axis    
    yaw = 0  # Your desired yaw angle in radians
    quaternion = quaternion_from_euler(roll, pitch, yaw)
    target_pose.orientation.x = quaternion[0]
    target_pose.orientation.y = quaternion[1]
    target_pose.orientation.z = quaternion[2]
    target_pose.orientation.w = quaternion[3]




    # Plan the motion
    move_group.set_pose_target(target_pose)
    plan = move_group.plan()

    # Execute the motion
    move_group.go(wait=True)

if __name__ == '__main__':
    target_x = 0.5
    target_y = 0
    target_z = 0.5
    move_to_position(target_x, target_y, target_z)
