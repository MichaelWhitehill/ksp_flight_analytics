class FuelConsumption:
    def __init__(self, konnection):
        self.lf_stream = konnection.conn.add_stream(konnection.vessel.resources.amount, 'LiquidFuel')
        self.ox_stream = konnection.conn.add_stream(konnection.vessel.resources.amount, 'Oxidizer')
        self.met_stream = konnection.met_stream
        self.last_ox_val = 0
        self.last_lf_val = 0
        self.last_lf_time = 0
        self.last_ox_time = 0

    def compute_lf_consumption(self):
        current_lf = self.lf_stream()
        current_time = self.met_stream()
        if current_time == 0:
            return 0
        ret = abs((current_lf - self.last_lf_val) / (current_time - self.last_lf_time))
        self.last_lf_val = current_lf
        self.last_lf_time = current_time
        return ret

    def compute_ox_consumption(self):
        current_ox = self.lf_stream()
        current_time = self.met_stream()
        if current_time == 0:
            return 0
        ret = abs((current_ox - self.last_ox_val) / (current_time - self.last_ox_time))
        self.last_ox_val = current_ox
        self.last_ox_time = current_time
        return ret