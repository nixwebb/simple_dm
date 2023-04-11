#!/usr/bin/env python3

import rospy
import smach
import smach_ros
from std_msgs.msg import String

# define state Foo
class Greet(smach.State):
    def __init__(self):
        self.pub = rospy.Publisher('facelistner', String, queue_size=10)
        smach.State.__init__(self, outcomes=['valerie','crochet','end','greet'])
        self.counter = 0

    def execute(self, userdata):
        rospy.loginfo('Executing state GREET')
        self.pub.publish("How can I help you?")
        text = str(input())
        if text == 'valerie':
            return 'valerie'
        elif text =='crochet':
            return 'crochet'
        elif text =='end':
            return 'end'
        else:
            return 'greet'


# define state Bar
class Valerie(smach.State):
    def __init__(self):
        self.pub = rospy.Publisher('facelistner', String, queue_size=10)
        smach.State.__init__(self, outcomes=['greet'])

    def execute(self, userdata):
        rospy.loginfo('Executing state Valerie')
        self.pub.publish("My name is Valerie and I'm a robot")
        return 'greet'
        

class Crochet(smach.State):
    def __init__(self):
        self.pub = rospy.Publisher('facelistner', String, queue_size=10)

        smach.State.__init__(self, outcomes=['greet'])

    def execute(self, userdata):
        rospy.loginfo('Executing state Crochet')
        self.pub.publish("Crochet is a lab in the CS Department")
        return 'greet'

class End(smach.State):
    def __init__(self):
        self.pub = rospy.Publisher('facelistner', String, queue_size=10)

        smach.State.__init__(self, outcomes=['final'])

    def execute(self, userdata):
        rospy.loginfo('Executing state End')
        self.pub.publish("Goodbye")
        return 'final'                

# main
def main():
    rospy.init_node('simple_dm')

    # Create a SMACH state machine
    sm = smach.StateMachine(outcomes=['final'])

    # Open the container
    with sm:
        # Add states to the container
        smach.StateMachine.add('GREET', Greet(), 
                               transitions={'valerie':'VALERIE', 
                                            'crochet':'CROCHET',
                                            'greet':'GREET',
                                            'end':'END'
                                            })
  
        smach.StateMachine.add('VALERIE', Valerie(), 
                               transitions={'greet':'GREET'})

        smach.StateMachine.add('CROCHET', Crochet(), 
                               transitions={'greet':'GREET'})
    
        smach.StateMachine.add('END', End(), 
                               transitions={'final':'final'})   
    # Execute SMACH plan
    outcome = sm.execute()
    
    # Wait for ctrl-c to stop the application
    rospy.spin()

if __name__ == '__main__':
    main()
