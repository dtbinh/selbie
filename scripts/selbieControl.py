#!/usr/bin/env python
import rospy, math
from sensor_msgs.msg import Imu
from std_msgs.msg import Float64
from pid import PID

class controlClass(PID):
	def __init__(self):
		PID.__init__(self)
		self.setKp(0.05)	
		self.setKi(0.003)	
		self.setKd(0.00075)	
		self.setPoint(0)
		self.theta = 0
		self.thetaA = 0
		self.thetaG = 0
		self.lwEffort = 0
		self.rwEffort = 0
		self.Effort = 0
		self.yawEffort = 0
		self.lwEffortPublisher  = rospy.Publisher('selbie/selbie_lj_effort_controller/command', Float64, queue_size=10)	
		self.rwEffortPublisher = rospy.Publisher('selbie/selbie_rj_effort_controller/command', Float64, queue_size=10)
		
	def controlFn(self):
		rospy.init_node("selbie_control_node")
		rospy.Subscriber("selbie/imu/data", Imu, self.controlFnCallback)
		rospy.spin()
	
	def controlFnCallback(self,data):
		#Calculation of Accelerometer pitch angle
		temp = 180 - math.atan2( data.linear_acceleration.x , data.linear_acceleration.z) * (180 / math.pi)
		if temp >180.0 and temp<=360.0:
			self.thetaA = temp -360
		else:
			self.thetaA = temp
		
		#Calculation of Gyroscope pitch angle
		temp = temp + ( - data.angular_velocity.y / 1.788) #1.788 is the offset factor
		self.thetaG = 180 - temp

		#Complimentary filter
		self.theta = 0.95 * (self.thetaG)+ 0.05 * self.thetaA
		
		if self.theta<=45.0 and self.theta>=-45:
			self.Effort = (self.update(self.theta))
			self.lwEffort = 0.5 * self.Effort + 0.5 * self.yawEffort
			self.rwEffort = 0.5 * self.Effort - 0.5 * self.yawEffort
		else:	
			self.Effort = 0
			self.lwEffort = 0
			self.rwEffort = 0

		print self.thetaA, self.thetaG, self.theta, self.Effort
		self.lwEffortPublisher.publish(-self.lwEffort)
		self.rwEffortPublisher.publish(-self.rwEffort)

michaelRoss = controlClass()
michaelRoss.controlFn()
		
