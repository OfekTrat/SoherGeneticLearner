
class Agent(object):
    def __init__(self, agent_type):
        self.type = agent_type

    def prepare_data(self, data):
        print("Expecting an Implementation of child agent")
        raise

    def get_signal(self, prepared_data):
        print("Expecting an implementation of child agent")
        raise

    def id(self):
        print("Expecting and implementation of child agent")
        raise
