
class Agent(object):
    def __init__(self, type):
        self.type = type

    def prepare_data(self, data):
        print("Expecting an Implementation of child agent")
        raise

    def get_signal(self):
        print("Expecting an implementation of child agent")

    @classmethod
    def get_types(cls):
        types = {
            "require_input": [  # Requires small window and then large window
                "Volume",
                "MACA",
                "Stochastic"
            ],
            "simple": [  # Does not require any input
                "ADX",
                "CandleStick",
                "Trend"
            ]
        }

