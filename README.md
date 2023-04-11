# simple_dm
ROS DM

A simple finite state machine that controls dialogue, plus an NLU component that uses tf-idf to select 
the appropriate action based on matching between user queries and a corpus of sample utterances. The state
data (and state transition triggers) are stored as text files in the state_data directory.
