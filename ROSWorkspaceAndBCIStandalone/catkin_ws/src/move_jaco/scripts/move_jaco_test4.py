#!/usr/bin/env python3

import sys
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
from tf.transformations import quaternion_from_euler
from math import pi

def move_to_position_with_orientation(target_x, target_y, target_z, joint_6_value):
    moveit_commander.roscpp_initialize(sys.argv)
    rospy.init_node('move_jaco_test', anonymous=True)

    # Disable joint state publisher in MoveIt
    rospy.set_param('/move_group/publish_joint_states', False)
    rospy.set_param('/move_group/publish_planning_scene', True)

    robot = moveit_commander.RobotCommander()
    scene = moveit_commander.PlanningSceneInterface()
    group_name = "arm"
    move_group = moveit_commander.MoveGroupCommander(group_name)

    # Define the target pose
    target_pose = geometry_msgs.msg.Pose()
    target_pose.position.x = target_x
    target_pose.position.y = target_y
    target_pose.position.z = target_z

    roll = 0
    pitch = pi/2
    yaw = 0
    quaternion = quaternion_from_euler(roll, pitch, yaw)
    target_pose.orientation.x = quaternion[0]
    target_pose.orientation.y = quaternion[1]
    target_pose.orientation.z = quaternion[2]
    target_pose.orientation.w = quaternion[3]

    # Get the joint names
    joint_names = move_group.get_active_joints()

    # Set the target joint value for joint 6
    joint_values = move_group.get_current_joint_values()
    joint_values[joint_names.index('j2n6s300_joint_6')] = joint_6_value

    # Plan the motion
    move_group.set_pose_target(target_pose)
    move_group.set_joint_value_target(joint_values)
    plan = move_group.plan()

    # Execute the motion
    move_group.go(wait=True)

if __name__ == '__main__':
    target_x = 0.5
    target_y = 0
    target_z = 0.5
    joint_6_value = 1.3233  # Your desired value for joint 6
    move_to_position_with_orientation(target_x, target_y, target_z, joint_6_value)
