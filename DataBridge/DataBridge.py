"""
This file establishes an RPC connection, and bridges data from the streams to the listeners
Used for plotting and saving live data
"""
import time

from DataBridge.BasicDataStreams import create_streams
from DataBridge.Konnection import Konnection


class Bridge:
    def __init__(self, ip, rpc_port, stream_port, update_time, listeners=None, save_file=None):
        if listeners is None:
            listeners = []
        self.k = Konnection()
        self.k.connect(ip, rpc_port, stream_port)
        self.listeners = listeners
        self.save_file = save_file
        self.update_time = update_time
        self.streams = create_streams(self.k)
        self.file = None
        self.cont = True
        if save_file:
            self.file = open(save_file, 'a+')

    def write_to_file(self, line):
        if not self.file:
            return
        self.file.write(line+"\n")

    def start(self):
        # read in file and send it to listeners
        keys = self.streams.keys()
        self.write_to_file(','.join(keys))
        while self.cont:
            time.sleep(self.update_time)
            entry_values = []
            entry_dict = {}
            for key in keys:
                val = self.streams[key]()
                entry_values.append(str(val))
                entry_dict[key] = val
            print_vals = ','.join(entry_values)
            self.write_to_file(print_vals)
            for l in self.listeners:
                l.receive_entry(entry_dict)

    def tear_down(self):
        self.cont = False
        if self.file:
            self.file.close()
            self.file = None
