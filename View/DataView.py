from tkinter import Frame

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class DataView(Frame):
    def __init__(self, master, view, figure):
        Frame.__init__(self, master)
        self.view = view
        self.grid()
        self.fig = figure
        canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.plot_widget = canvas.get_tk_widget()
        self.plot_widget.grid(row=0, column=0, rowspan=10, columnspan=10)
        # friendly names to subplots
        self.sub_plots = {}
        # max dynamic pressure
        # max G-force
        # max air intake

    def receive_entry(self, entry):
        for key in entry.keys():
            if key == 'met':
                continue
            self.add_data(key, [float(entry['met'])], float(entry[key]))
        self.fig.canvas.draw()

    def receive_mass(self, entry):
        for key in entry.keys():
            if key == 'met':
                continue
            self.add_data(key, range(0, len(entry[key])), entry[key])
        self.fig.canvas.draw()

    def add_plot(self, plot_name):
        print("Added plot: " + plot_name)
        ax = self.fig.add_subplot(4, 6, len(self.sub_plots.keys())+1)
        ax.set_title(plot_name)
        self.sub_plots[plot_name] = ax
        self.fig.tight_layout()

    def add_data(self, plot_name, x, y):
        if not self.sub_plots.get(plot_name, False):
            self.add_plot(plot_name)
        self.sub_plots[plot_name].scatter(x, y, c=(0, 0, 0), alpha=0.5)
