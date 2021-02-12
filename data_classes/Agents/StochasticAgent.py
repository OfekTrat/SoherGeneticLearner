from .Agent import Agent


AGENT_TYPE = "Stochastic"


class StochasticAgent(Agent):
    TYPE = AGENT_TYPE

    def __init__(self, d_window_size, k_window_size):
        super().__init__(AGENT_TYPE)
        self.mapper = {
            0: "NOTHING",
            1: "BUY",
            2: "SELL"
        }
        self.n_outputs = 3
        self.k_window_size = k_window_size
        self.d_window_size = d_window_size

    def get_signal(self, data):
        results = self._calc_stochastic(data)

        current_k = results["k_fast"].iloc[-1]
        current_slow_d = results["d_slow"].iloc[-1]

        previous_k = results["k_fast"].iloc[-2]
        previous_d = results["d_slow"].iloc[-2]

        if previous_k < previous_d and current_slow_d < current_k < 20:
            return 1
        elif previous_k > previous_d > 80 and current_slow_d > current_k > 80:
            return 2
        else:
            return 0

    def _calc_stochastic(self, data):
        copy = data.copy()

        copy["low_min"] = data['Low'].rolling(self.k_window_size).min()
        copy["high_max"] = data['High'].rolling(self.k_window_size).max()

        copy["k_fast"] = 100 * ((copy["Close"] - copy["low_min"]) / (copy["high_max"] - copy["low_min"]))
        copy["d_fast"] = copy["k_fast"].rolling(self.d_window_size).mean()
        copy["d_slow"] = copy["d_fast"].rolling(self.d_window_size).mean()

        return copy

    def id(self):
        return "stochastic_id_" + str(self.d_window_size) + "-" + str(self.k_window_size)

