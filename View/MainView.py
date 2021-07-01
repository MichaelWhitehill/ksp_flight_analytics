import tkinter as tk

import matplotlib
import matplotlib.pyplot as plt
from View.ConnectionView import ConnectionView
from View.DataView import DataView
from View.FileView import FileView

matplotlib.use('TkAgg')


def main():
    MainView()


class MainView:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("2500x2500")

        # setup matplot
        self.fig = plt.figure(figsize=[30, 20])
        plt.ion()

        self.file_frame = tk.Frame(self.window, highlightbackground="black", highlightthickness=1)
        self.file_frame.grid(row=0, column=0, rowspan=2, columnspan=2)
        self.file_view = FileView(self.file_frame, self)

        self.connection_frame = tk.Frame(self.window, highlightbackground="black", highlightthickness=1)
        self.connection_frame.grid(row=0, column=3, rowspan=3, columnspan=2)
        self.cv = ConnectionView(self.connection_frame, self)

        self.data_frame = tk.Frame(self.window, highlightbackground="black", highlightthickness=1)
        self.data_frame.grid(row=4, column=0, rowspan=11, columnspan=20)
        self.dv = None

        self.window.protocol("WM_DELETE_WINDOW", self.tear_down)
        self.window.mainloop()

    def tear_down(self):
        if self.cv:
            self.cv.tear_down()
        plt.close()

    def input_set(self):
        self.dv = DataView(self.data_frame, self, self.fig)
        return self.dv


if __name__ == '__main__':
    main()
