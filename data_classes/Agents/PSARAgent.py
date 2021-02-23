from .Agent import Agent
import ta.trend as trend


class PSARAgent(Agent):
    def __init__(self, step=0.02, max_step=0.2):
        self.step = step
        self.max_step = max_step

        self.column_name = f"psar_{step}_{max_step}"

    def prepare_data(self, data):
        psar = trend.PSARIndicator(data["High"], data["Low"], data["Close"], self.step, self.max_step)
        pasr_up = psar.psar_up_indicator()
        pasr_up = pasr_up.apply(lambda x: x * 2)
        psar_down = psar.psar_down_indicator()
        psar_indicator = pasr_up + psar_down
        data[self.column_name] = psar_indicator

    def get_signal(self, prepared_data):
        return prepared_data[self.column_name].iloc[-1].item()  # 2 if psar_up, 1 if psar_down, 0 otherwise

    def id(self):
        return self.column_name


