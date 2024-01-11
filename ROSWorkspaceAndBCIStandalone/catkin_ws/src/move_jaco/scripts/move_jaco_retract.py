#!/usr/bin/env python3

import sys
import rospy
import moveit_commander

def move_to_retract(arm_group):
    # Move to Retract position
    arm_group.set_named_target("Retract")
    arm_group.go(wait=True)

def main():
    # Initialize moveit_commander
    moveit_commander.roscpp_initialize(sys.argv)
    rospy.init_node('move_to_retract_script', anonymous=True)

    # Create MoveGroupCommander for the arm
    arm_group = moveit_commander.MoveGroupCommander("arm")

    # Move to Retract position
    move_to_retract(arm_group)

    # Shutdown moveit_commander
    moveit_commander.roscpp_shutdown()

if __name__ == '__main__':
    main()
