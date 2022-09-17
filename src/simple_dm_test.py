#!/usr/bin/env python3

import rospy
import smach
import smach_ros
from std_msgs.msg import String
import responses

pub = rospy.Publisher('face_listener', String, queue_size=10, latch=True)


# define state Foo
class Greet(smach.State):
    def __init__(self):
        #self.pub = rospy.Publisher('facelistner', String, queue_size=10, latch=True)
        rospy.Subscriber('asr_string', String, self.asr_updater)
        smach.State.__init__(self, outcomes=['valerie','crochet','end','greet'])
        self.counter = 0
        self.first = True
        self.utterance = ""
        self.next_utterance = ""

    def asr_updater(self, data):
        
        self.utterance = self.next_utterance
        self.next_utterance = data

    def execute(self, userdata):
        rospy.loginfo('Executing state GREET')
        if self.first:
            rospy.loginfo('Greet: First time')

            pub.publish('say::Hello, my name is Valerie. How can I help you?')
            self.first=False
        #text = str(input())
        if self.utterance != self.utterance:
#        if text == 'valerie':
#            return 'valerie'
#        elif text =='crochet':
#            return 'crochet'
#        elif text =='end':
#            return 'end'
#        else:
#            pub.publish("say::I'm sorry, I didn't understand that.")
#            return 'greet'
            if self.next_utterance == 'valerie':
                return 'valerie'
            elif self.next_utterance =='crochet':
                return 'crochet'
            elif self.next_utterance =='end':
                return 'end'
            else:
                pub.publish("say::I'm sorry, I didn't understand that")
                return 'greet'
        else:
                return 'greet'
        



# define state Bar
class Valerie(smach.State):
    def __init__(self):
        #pub = rospy.Publisher('facelistner', String, queue_size=10)
        smach.State.__init__(self, outcomes=['greet'])

    def execute(self, userdata):
        rospy.loginfo('Executing state Valerie')
        pub.publish("say::My name is Valerie and I'm a robot")
        return 'greet'
        

class Crochet(smach.State):
    def __init__(self):
        #self.pub = rospy.Publisher('facelistner', String, queue_size=10)

        smach.State.__init__(self, outcomes=['greet'])

    def execute(self, userdata):
        rospy.loginfo('Executing state Crochet')
        outtext = responses.crochet_text()
        pub.publish(outtext)
        return 'greet'

class End(smach.State):
    def __init__(self):
        #self.pub = rospy.Publisher('facelistner', String, queue_size=10)

        smach.State.__init__(self, outcomes=['final'])

    def execute(self, userdata):
        rospy.loginfo('Executing state End')
        pub.publish("say::Goodbye")
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
