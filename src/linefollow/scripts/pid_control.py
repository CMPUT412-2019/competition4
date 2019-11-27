#!/usr/bin/env python

import time

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64


class PIDController:
    def __init__(self, kp, ki, kd):
        self.kp, self.ki, self.kd = kp, ki, kd
        self.integral = 0
        self.last_time = None

    def get(self, error):
        if self.last_time is None:
            self.last_time = time.clock()
            return 0

        cur_time = time.clock()
        self.last_time, dt = cur_time, cur_time - self.last_time

        self.integral += error * dt
        derivative = error / dt
        proportional = error

        return -(self.kp * proportional + self.ki * self.integral + self.kd * derivative)


class Main:
    def __init__(self):
        rospy.init_node('pid_controller')

        self.linear_error = 0
        self.angle_error = 0

        self.angle_error_subscriber = rospy.Subscriber('angle_error', Float64, self.angle_error_callback)
        self.linear_error_subscriber = rospy.Subscriber('linear_error', Float64, self.linear_error_callback)
        self.twist_publisher = rospy.Publisher('control/cmd_vel_raw', Twist, queue_size=1)

        self.angle_controller = PIDController(kp=4., ki=1./100000, kd=1./100000)
        self.linear_controller = PIDController(kp=1., ki=0., kd=0.)

        self.rate = rospy.Rate(100)

        self.last_update_time = time.time()

    def spin(self):
        while not rospy.is_shutdown():
            if time.time() - self.last_update_time < 0.5:
                self.publish_twist()
            self.rate.sleep()

    def angle_error_callback(self, msg):
        self.last_update_time = time.time()
        self.angle_error = msg.data

    def linear_error_callback(self, msg):
        self.last_update_time = time.time()
        self.linear_error = msg.data

    def publish_twist(self):
        t = Twist()
        t.linear.x = self.linear_controller.get(self.linear_error)
        t.angular.z = self.angle_controller.get(self.angle_error)
        print(t.linear.x)
        self.twist_publisher.publish(t)


if __name__ == '__main__':
    Main().spin()
