from tkinter import Frame, Label, Button
from tkinter.filedialog import askopenfilename

from DataBridge.FileBridge import FileBridge


class FileView(Frame):
    def __init__(self, master, view):
        Frame.__init__(self, master)
        self.view = view
        self.setup_frame = Frame(self.master)
        self.setup_frame.grid(row=0, column=0, rowspan=3, columnspan=2)

        self.selection_label = Label(self.setup_frame, text='Select a data source')
        self.selection_label.grid(column=0, row=0)

        self.open_file_btn = Button(self.setup_frame, text="Open File", command=self.select_file)
        self.open_file_btn.grid(column=1, row=0)

    def select_file(self):
        data = askopenfilename()
        if not data:
            return
        dv = self.view.input_set()
        FileBridge(data, dv)
