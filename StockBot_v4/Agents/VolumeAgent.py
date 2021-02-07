from Agents.Agent import Agent

class VolumeAgent(Agent):
    def __init__(self, small_interval, large_interval):
        super().__init__("Volume Agent")
        self.n_outputs = 2
        self.small_interval = small_interval
        self.large_interval = large_interval
        self.signals = {
            0: "WeakVolume",
            1: "StrongVolume"
        }
        
        
    def get_signal(self, data) -> int:
        data["SmallVolumeMovingAverage"] = data["Volume"].rolling(self.small_interval).mean()
        data["LargeVolumeMovingAverage"] = data["Volume"].rolling(self.large_interval).mean()
        
        if data["SmallVolumeMovingAverage"].iloc[-1] > data["LargeVolumeMovingAverage"].iloc[-1]:
            return 1
        else:
            return 0
        
