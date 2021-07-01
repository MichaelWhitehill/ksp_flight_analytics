import krpc


class Konnection:
    def __init__(self):
        self.conn = None
        self.vessel = None

    def connect(self, ip='192.168.1.11', rpc_port=4283, stream_port=4284):
        print("attempting connection")
        self.conn = krpc.connect(
            name="flight analytics logger",
            address=ip,
            rpc_port=rpc_port, stream_port=stream_port
        )
        print(self.conn.krpc.get_status().version)
        self.vessel = self.conn.space_center.active_vessel
        print("Successful connection\n Logging data for: " + self.vessel.name)
