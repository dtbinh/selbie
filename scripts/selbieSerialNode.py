#!/usr/bin/env python
import serial, time, rospy, tf

_port=raw_input("Enter Port: ")
_baud=9600
rospy.init_node('mpu6050TfBroadcaser')
br = tf.TransformBroadcaster()
ser = serial.Serial(_port,_baud)
pt = time.time()
while 1:	
	s = ser.readline()
	ct = time.time()
	print s
	if ct-pt >=5:
		ypr=[float(i) for i in s.split()]
		br.sendTransform((0.0,0.0,0.0),(ypr[2],ypr[1],ypr[0],1.0),rospy.Time.now(),"odom","selbie_body")
