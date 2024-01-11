#!/usr/bin/env python3

import rospy
from Eyetracking.msg import BoolStateEyetracking
from BCI.msg import BoolStateBCI
import sys
import moveit_commander
from moveit_commander import MoveGroupCommander


bool_state_a = False
bool_state_b = False
int_state_b = 0

def move_to_pickup():
    moveit_commander.roscpp_initialize(sys.argv)

    # Create a MoveGroupCommander for the arm
    arm_group = MoveGroupCommander("arm")

    # Move to the "Home" position
    arm_group.set_named_target("PickupOne")
    arm_group.go(wait=True)

    moveit_commander.roscpp_shutdown()

def move_to_pickup2():
    moveit_commander.roscpp_initialize(sys.argv)

    # Create a MoveGroupCommander for the arm
    arm_group = MoveGroupCommander("arm")

    # Move to the "Home" position
    arm_group.set_named_target("PickupTwo")
    arm_group.go(wait=True)

    moveit_commander.roscpp_shutdown()



def subscribing_node():
    rospy.init_node('subscribing_node', anonymous=True)

    rospy.Subscriber('bool_state_topic_BCI', BoolStateBCI, callback_a)
    rospy.Subscriber('bool_state_topic_Eyetracking', BoolStateEyetracking, callback_b)

    rospy.spin()

def callback_a(data):
    global bool_state_a
    bool_state_a = data.data
    check_both_states()

def callback_b(data):
    global bool_state_b
    global int_state_b
    bool_state_b = data.bool_data
    int_state_b = data.int_data    
    check_both_states()

def check_both_states():
    global bool_state_a, bool_state_b
    # Check if both states are True
    if bool_state_a and bool_state_b:
        print("Both states are True!")
        if int_state_b == 1:
            move_to_pickup()
            
        elif int_state_b == 2:
            move_to_pickup2()

        elif int_state_b == 0:
            print("Error no integer state sent")





if __name__ == '__main__':
    subscribing_node()
