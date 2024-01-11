#!/usr/bin/env python3

import sys
import rospy
import moveit_commander
import geometry_msgs.msg
from moveit_commander import MoveGroupCommander
from moveit_commander import PlanningSceneInterface

def wait_for_key():
    input("Press Enter to continue...")

def move_to_position(group, x, y, z):
    pose_target = geometry_msgs.msg.Pose()
    pose_target.orientation.w = 1.0
    pose_target.position.x = x
    pose_target.position.y = y
    pose_target.position.z = z
    group.set_pose_target(pose_target)
    print("Current joint values:", group.get_current_joint_values())
    group.go(wait=True)
    print("New joint values:", group.get_current_joint_values())



def close_gripper(group):
    group.set_named_target("Close")
    group.go(wait=True)

def open_gripper(group):
    group.set_named_target("Open")
    group.go(wait=True)
    
 

def main():


    moveit_commander.roscpp_initialize(sys.argv)
    rospy.init_node('move_jaco_test', anonymous=True)

    arm_group = MoveGroupCommander("arm")
    gripper_group = MoveGroupCommander("gripper")

    # Home position
    arm_group.set_named_target("Home")
    arm_group.go(wait=True)

    wait_for_key()

    # Move to position (0, 0.45, 0) pointing along the Y-axis
    move_to_position(arm_group, 0, -0.5, 0)

    wait_for_key()

    # Close gripper
    close_gripper(gripper_group)

    wait_for_key()

    # Move to position (1, 0, 0)
    move_to_position(arm_group, 1, 0, 0)

    wait_for_key()

    # Open gripper
    open_gripper(gripper_group)

    wait_for_key()

    # Return to Home position
    arm_group.set_named_target("Home")
    arm_group.go(wait=True)

    moveit_commander.roscpp_shutdown()

if __name__ == '__main__':
    main()
