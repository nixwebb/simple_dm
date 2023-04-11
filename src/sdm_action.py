#!/usr/bin/env python3

import rospy
import smach
import smach_ros
from std_msgs.msg import String
import dialog_tfidf as da

from smach_ros import SimpleActionState
#import dialog_action.msg
import google_asr_action.msg


facepub = rospy.Publisher('face_listener', String, queue_size=10)
nlu = da.Vectorize('/home/nick/catkin_ws/src/simple_dm/src/state_data/')


class SimpleGreet(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['hcihy'])

    def execute(self, userdata):
        rospy.loginfo('Executing state GREET')
        facepub.publish("say::Good day. My name is Valerie. I'm a robot")
        print("say::Good day. My name is Valerie. I'm a robot")
        return('hcihy')


class HCIHY(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['asr'])

    def execute(self, userdata):
        rospy.loginfo('Executing state HCIHY')
        facepub.publish("say::How can I help you?")
        print("say::How can I help you?")
        return('asr')        


class Process(smach.State):
    def __init__(self):
        #self.pub = rospy.Publisher('facelistner', String, queue_size=10)
        smach.State.__init__(self, outcomes=['valerie','crochet','end','hcihy'],
                                    input_keys=['response'])

    def execute(self, userdata):
        rospy.loginfo('Executing state PROCESS')
        text = userdata.response
        print('TEXT is:',text)
        answer = nlu.do_query(text)
        print(text,answer)
        return answer
        #if text == 'valerie':
        #    return 'valerie'
        #elif text =='crochet':
        #    return 'crochet'
        #elif text =='end':
        #    return 'end'
        #else:
        #    return 'hcihy'


# define state Bar
class Valerie(smach.State):
    def __init__(self):
        #self.pub = rospy.Publisher('facelistner', String, queue_size=10)
        smach.State.__init__(self, outcomes=['hcihy'])

    def execute(self, userdata):
        rospy.loginfo('Executing state Valerie')
        facepub.publish("say::My name is Valerie and I'm a robot")
        print("say::My name is Valerie and I'm a robot")
        return 'hcihy'
        

class Crochet(smach.State):
    def __init__(self):
        #self.pub = rospy.Publisher('facelistner', String, queue_size=10)

        smach.State.__init__(self, outcomes=['hcihy'])

    def execute(self, userdata):
        rospy.loginfo('Executing state Crochet')
        facepub.publish("say::Crochet is a lab in the CS Department")
        print("say::Crochet is a lab in the CS Department")
        return 'hcihy'

class End(smach.State):
    def __init__(self):
        #self.pub = rospy.Publisher('facelistner', String, queue_size=10)

        smach.State.__init__(self, outcomes=['final'])

    def execute(self, userdata):
        rospy.loginfo('Executing state End')
        facepub.publish("say::Goodbye")
        print("say::Goodbye")
        return 'final'                

# main
def main():
    rospy.init_node('simple_dm')

    # Create a SMACH state machine
    sm = smach.StateMachine(outcomes=['final','aborted','preempted'])

    # Open the container
    with sm:
        # Add states to the container
        smach.StateMachine.add('SIMPLEGREET', SimpleGreet(), 
                               transitions={'hcihy':'HCIHY'})
  
        smach.StateMachine.add('HCIHY', HCIHY(), 
                               transitions={'asr':'ASR'})

#        smach.StateMachine.add('ASR', 
#                            smach_ros.SimpleActionState('dialog', dialog_action.msg.DialogAction,result_slots=['response']), 
#                            {'succeeded':'PROCESS'})


        smach.StateMachine.add('ASR', 
                            smach_ros.SimpleActionState('ASR_Node', google_asr_action.msg.GoogleASRAction,result_slots=['response']), 
                            {'succeeded':'PROCESS'})


        smach.StateMachine.add('PROCESS', Process(), 
                               transitions={'valerie':'VALERIE', 
                                            'crochet':'CROCHET',
                                            'hcihy':'HCIHY',
                                            'end':'END'
                                            })

        smach.StateMachine.add('VALERIE', Valerie(), 
                               transitions={'hcihy':'HCIHY'})



        smach.StateMachine.add('CROCHET', Crochet(), 
                               transitions={'hcihy':'HCIHY'})
    
        smach.StateMachine.add('END', End(), 
                               transitions={'final':'final'})   
    # Execute SMACH plan
    outcome = sm.execute()
    
    # Wait for ctrl-c to stop the application
    rospy.spin()

if __name__ == '__main__':
    main()
