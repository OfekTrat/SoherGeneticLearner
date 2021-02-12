
class Agent(object):
    def __init__(self, type):
        self.type = type

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

