#!/usr/bin/env python
from vrep_common.srv import *
import rospy

class invpen():
	def __init__(self):
		rospy.wait_for_service('/vrep/simRosStartSimulation')
		try:
			dummy = rospy.ServiceProxy('/vrep/simRosStartSimulation', simRosStartSimulation)
			resp = dummy()

			if resp!=-1:
				print "Simulation Started Successfully"
				self.consoleDisplay = rospy.ServiceProxy('/vrep/simRosAddStatusbarMessage', simRosAddStatusbarMessage)
				self.consoleDisplay("Connection with ROS established")
			

		except rospy.ServiceException, e:
			print "Service call failed: %s"%e

	def handles(self):
		rospy.wait_for_service('/vrep/simRosGetObjectHandle')
		try:
			dummy = rospy.ServiceProxy('/vrep/simRosGetObjectHandle', simRosGetObjectHandle)
			self.joint1 = dummy('selbie_lj')
			self.joint2 = dummy('selbie_rj')

			if self.joint1.handle and self.joint2.handle != -1:
				print "Joint information obtained", self.joint1, self.joint2
				self.consoleDisplay("Joint information was provided to ROS")

		except rospy.ServiceException, e:
			print "Service call failed: %s"%e

	def setVelocities(self,vel1,vel2):
		rospy.wait_for_service('/vrep/simRosSetJointTargetVelocity')
		try:
			dummy = rospy.ServiceProxy('/vrep/simRosSetJointTargetVelocity', simRosSetJointTargetVelocity)
			result1=dummy(self.joint1.handle,vel1)
			result2=dummy(self.joint2.handle,vel2)

			#if result1.result and result2.result != -1:
			#	print "Joint velocities set"
			#	self.consoleDisplay("Joint velocities obtained from ROS")
	
		except rospy.ServiceException, e:
			print "Service call failed: %s"%e


#HOW TO USE THIS FUNCTION:
#Open VREP/programming/include/v_repConst.h and convert the OCTAL given there to integer. Append a 1 to the octal number and find the corresponding integer
	def getSensorReadings(self):
		rospy.wait_for_service('/vrep/simRosEnablePublisher')
		try:
			
			dummy = rospy.ServiceProxy('/vrep/simRosEnablePublisher', simRosEnablePublisher)
			dummy('accelerometer',10,8199,12,14,'')
			dummy('gyroScope',10,8199,4,18,'')      
			dummy('jointStates',10,4102,-2,-1,'')			           

			print "Publishers Enabled for topics "
			self.consoleDisplay("Publishers enabled")

		except rospy.ServiceException, e:
			print "Service call failed: %s"%e

	def enableSubscibers(self):
		rospy.wait_for_service('/vrep/simRosEnableSubscriber')
		try:
			
			dummy = rospy.ServiceProxy('/vrep/simRosEnableSubscriber', simRosEnableSubscriber)
			print dummy('targetVelocityJ1',10,6153,self.joint1.handle,-1,'') #6145 for Torque 6153 for velocity
			print dummy('targetVelocityJ2',10,6153,self.joint2.handle,-1,'')

		except rospy.ServiceException, e:
			print "Service call failed: %s"%e
			
	'''def getSensorReadings(self):
		#rospy.wait_for_service('/vrep/simRosGetFloatSignal')
		try:
			dummy = rospy.ServiceProxy('/vrep/simRosGetFloatSignal', simRosGetFloatSignal)
			self.accel ={'x': dummy('accelerometerX').signalValue,'y': dummy('accelerometerY').signalValue,'z': dummy('accelerometerZ').signalValue}
			self.gyro  ={'x': dummy('gyroX').signalValue,'y': dummy('gyroY').signalValue,'z': dummy('gyroZ').signalValue}
			self.jointState1 = rospy.ServiceProxy('/vrep/simRosGetJointState',simRosGetJointState)(self.joint1.handle)
			self.jointState2 = rospy.ServiceProxy('/vrep/simRosGetJointState',simRosGetJointState)(self.joint2.handle)			
	
		except rospy.ServiceException, e:
			print "Service call failed: %s"%e'''

	def stopSimulation(self):
		rospy.wait_for_service('/vrep/simRosStopSimulation')
		try:
			dummy = rospy.ServiceProxy('/vrep/simRosStopSimulation', simRosStopSimulation)
			resp = dummy()

			if resp!=-1:
				print "Simulation Stopped Successfully"
				self.consoleDisplay = rospy.ServiceProxy('/vrep/simRosAddStatusbarMessage', simRosAddStatusbarMessage)
				self.consoleDisplay("Connection with ROS cancelled")
			

		except rospy.ServiceException, e:
			print "Service call failed: %s"%e
