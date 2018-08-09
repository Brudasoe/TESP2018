#!/usr/bin/env python

import rospy
from std_msgs.msg import UInt16
from joy_feedback_ros.msg import Rumble
import time
from sensor_msgs.msg import Imu

prev = 10

def talker(msg):
    global prev

    #print(msg.linear_acceleration.z)
    difference = abs(msg.linear_acceleration.z - prev)
    prev = msg.linear_acceleration.z
    
    print(difference)


    #high = min(difference*7 * 18000,18000)
    #weak = min(difference*7 * 18000,18000)

    pub = rospy.Publisher('/rumble', Rumble, queue_size=10)
    pub2 = rospy.Publisher('/play', UInt16, queue_size=10)
    
    #rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz

    ###rostopic pub -1 /rumble joy_feedback_ros/Rumble 18000 18000
    rumble = Rumble()
    rumble.strong_magnitude = 18000
    rumble.weak_magnitude = 18000
    

    ###rostopic pub /play std_msgs/UInt16 1
    #pub2.publish()
    play = UInt16()
    play.data = 1
    

    
    #pub.publish(rumble)
    if difference > 1:
        pub.publish(rumble)
        pub2.publish(play)
        #time.sleep(4.5)
        rate.sleep()
    

if __name__ == '__main__':
    try:
        rospy.init_node('talker')
        sub=rospy.Subscriber('/imu', Imu, talker)
        rospy.spin()
        #talker()

    except rospy.ROSInterruptException:
        pass
