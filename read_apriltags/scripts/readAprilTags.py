#!/usr/bin/env python

import rospy


from apriltags.msg import AprilTagDetections
from read_apriltags.msg import readMessage
from read_apriltags.msg import readMessages
from read_apriltags.msg import rpy

import geometry_msgs.msg 
import std_msgs.msg

import numpy as np
import tf

def callback(data):
    i = 0
    readMessages_from_data = readMessages();
    for single_data in data.detections:
	readMessage_from_data = readMessage();
	readMessage_from_data.TagID = single_data.id
	quaternion = (single_data.pose.orientation.x,single_data.pose.orientation.y,single_data.pose.orientation.z,single_data.pose.orientation.w)
	euler = tf.transformations.euler_from_quaternion(quaternion)
	data_rpy = rpy(euler[0],euler[1],euler[2])
	readMessage_from_data.euler_rpy = data_rpy
	readMessage_from_data.corners_array = single_data.corners2d
	readMessage_from_data.tag_size = single_data.tag_size
	readMessage_from_data.position_xyz = single_data.pose.position
        readMessages_from_data.messages.append(readMessage_from_data)
    pub = rospy.Publisher("AprilTagsInfo", readMessages,queue_size=10)
    pub.publish(readMessages_from_data)

def readAprilTags():
    rospy.init_node("readAprilTagsInfo", anonymous=True)
    #sub = rospy.Subscriber("secrets", AprilTagDetection, callback)
    sub = rospy.Subscriber("apriltags/detections", AprilTagDetections, callback)   
    rospy.spin() 
   

if __name__ == "__main__":
    readAprilTags()
