#!/usr/bin/env python3

import sys
import rospy
import moveit_commander
from moveit_commander import MoveGroupCommander

def move_to_pickup():
    moveit_commander.roscpp_initialize(sys.argv)
    rospy.init_node('move_jaco_pickup', anonymous=True)

    # Create a MoveGroupCommander for the arm
    arm_group = MoveGroupCommander("arm")

    # Move to the "Home" position
    arm_group.set_named_target("PickupOne")
    arm_group.go(wait=True)

    moveit_commander.roscpp_shutdown()

if __name__ == '__main__':
    move_to_pickup()