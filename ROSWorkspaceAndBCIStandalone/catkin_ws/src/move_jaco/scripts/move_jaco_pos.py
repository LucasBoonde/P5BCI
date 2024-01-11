#!/usr/bin/env python3

import sys
import rospy
import moveit_commander
from moveit_commander import MoveGroupCommander

def print_current_pose():
    moveit_commander.roscpp_initialize(sys.argv)
    rospy.init_node('print_current_pose', anonymous=True)

    # Create a MoveGroupCommander for the arm
    arm_group = MoveGroupCommander("arm")

    # Print the current pose of the end-effector (gripper)
    current_pose = arm_group.get_current_pose().pose
    print("Current Gripper Pose:")
    print("Position: [x, y, z] =", [current_pose.position.x, current_pose.position.y, current_pose.position.z])
    print("Orientation: [x, y, z, w] =", [current_pose.orientation.x, current_pose.orientation.y, current_pose.orientation.z, current_pose.orientation.w])

    moveit_commander.roscpp_shutdown()

if __name__ == '__main__':
    print_current_pose()
