"""
This file bridges data from a csv instead of live data for reviewing flights
"""
import csv


class FileBridge:
    def __init__(self, file_path, listener):
        self.listener = listener
        file = open(file_path, 'r')
        self.csv_reader = csv.DictReader(file)
        self.keys_set = False
        self.read_lines_mass()

    def read_lines(self):
        for row in self.csv_reader:
            self.listener.receive_entry(row)

    def read_lines_mass(self):
        data = {}
        for row in self.csv_reader:
            for key in row.keys():
                if not data.get(key, False):
                    data[key] = []
                data[key].append(float(row[key]))
        self.listener.receive_mass(data)
