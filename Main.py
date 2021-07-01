import time

from DataBridge.BasicDataStreams import create_streams
from DataBridge.DataBridge import Bridge
from DataBridge.Konnection import Konnection


def main():
    konnection = Konnection()
    konnection.connect()

    streams = create_streams(konnection)
    keys = streams.keys()
    print(", ".join(keys))
    while (True):
        time.sleep(2)
        # print("engine info: " + str(streams['engine_info']()))
        entry = str(konnection.met_stream()) + ": "
        entry_values = []
        for key in keys:
            entry_values.append(str(streams[key]()))
        print_vals = ', '.join(entry_values)
        print(entry + print_vals)

if __name__ == '__main__':
    d_bridge = Bridge('192.168.1.11', 4283, 4284,
                           2, [], './t.txt')
    d_bridge.start()
