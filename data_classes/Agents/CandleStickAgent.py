from candlestick import candlestick
from .Agent import Agent

SIGNAL_MAPPING = {
    "BEARISH_PATTERNS": [
        "BearishEngulfing",
        "BearishHarami",
        "DarkCloudCover",
        "EveningStar",
        "EveningStarDoji",
        "GravestoneDoji",
        "HangingMan",
        "ShootingStar"
    ],
    "BULLISH_PATTERNS": [
        "BullishEngulfing",
        "BullishHarami",
        "DragonflyDoji",
        "Hammer",
        "InvertedHammer",
        "MorningStar",
        "MorningStarDoji",
        "PiercingPattern"
    ]
}

AGENT_TYPE = "CandleStick"


class CandleStickAgent(Agent):
    TYPE = AGENT_TYPE

    def __init__(self):
        super().__init__(AGENT_TYPE)
        self.signals = {
            0: "NOTHING",
            1: "BULLISH",
            2: "BEARISH"
        }
        self.n_outputs = 3

    @staticmethod
    def get_signal(prepared_data):
        for key in SIGNAL_MAPPING.keys():
            for pattern in SIGNAL_MAPPING[key]:
                if prepared_data.iloc[-1][pattern]:
                    if key == "BEARISH_PATTERNS":
                        return 2
                    elif key == "BULLISH_PATTERNS":
                        return 1

        return 0

    def prepare_data(self, data):
        for key in SIGNAL_MAPPING.keys():
            for pattern in SIGNAL_MAPPING[key]:
                candlestick.search_pattern(pattern, data, target=pattern)


    def id(self):
        return "candlestick_id"
