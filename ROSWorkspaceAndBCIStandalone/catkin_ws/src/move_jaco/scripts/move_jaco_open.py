#!/usr/bin/env python3

import sys
import rospy
import moveit_commander
from moveit_commander import MoveGroupCommander

def open_gripper():
    moveit_commander.roscpp_initialize(sys.argv)
    rospy.init_node('move_jaco_open_gripper', anonymous=True)

    # Create a MoveGroupCommander for the gripper
    gripper_group = MoveGroupCommander("gripper")

    # Open the gripper
    gripper_group.set_named_target("Open")
    gripper_group.go(wait=True)

    moveit_commander.roscpp_shutdown()

if __name__ == '__main__':
    open_gripper()
