import sys
from tkinter import Frame, Label, Entry, Button, END, messagebox, BooleanVar, Checkbutton
from tkinter.filedialog import asksaveasfilename

from DataBridge.DataBridge import Bridge


class ConnectionView(Frame):
    def __init__(self, master, view):
        Frame.__init__(self, master)
        self.view = view
        self.bridge_thread = None
        self.d_bridge = None
        self.grid()

        self.use_save_file = BooleanVar()
        self.use_save_file.set(True)

        ip_label = Label(self, text='IP: ')
        ip_label.grid(column=0, row=0)

        self.ip_entry = Entry(self, width=12)
        self.ip_entry.insert(END, '192.168.1.11')
        self.ip_entry.grid(column=1, row=0, columnspan=3)

        rpc_lab = Label(self, text='rpc port: ')
        rpc_lab.grid(column=0, row=1)
        self.rpc_port = Entry(self, width=5)
        self.rpc_port.insert(END, 4283)
        self.rpc_port.grid(column=1, row=1)

        stream_lab = Label(self, text='stream port: ')
        stream_lab.grid(column=0, row=2)
        self.stream_port = Entry(self, width=5)
        self.stream_port.insert(END, 4284)
        self.stream_port.grid(column=1, row=2)

        update_label = Label(self, text="update delay (sec)")
        update_label.grid(column=0, row=3)
        self.update_time = Entry(self, width=2)
        self.update_time.insert(END, 2)
        self.update_time.grid(column=1, row=3)

        self.use_save_file_chk = Checkbutton(self, text='use file', var=self.use_save_file)
        self.use_save_file_chk.grid(row=4, column=0, columnspan=2)

        self.setBtn = Button(self, text="Set", command=self.set_and_connect)
        self.setBtn.grid(row=5, column=1)

    def set_and_connect(self):
        print(self.use_save_file.get())
        print(self.rpc_port.get())
        print(self.stream_port.get())
        save_file = None
        if self.use_save_file.get():
            save_file = asksaveasfilename(title="Save data stream")
            print(save_file)
            if not save_file:
                save_file = None
        try:
            dv = self.view.input_set()
            self.d_bridge = Bridge(self.ip_entry.get(), int(self.rpc_port.get()), int(self.stream_port.get()),
                                   int(self.update_time.get()), [dv], save_file)
        except:
            e = (sys.exc_info()[0])
            print(e)
            messagebox.showinfo('Connection error', 'Error connecting to KRPC. Check ip, and ports')
            return
        # self.bridge_thread = threading.Thread(target=self.d_bridge.start)
        # self.bridge_thread.start()
        self.d_bridge.start()
        self.disable()

    def disable(self):
        self.ip_entry.config(state='disabled')
        self.rpc_port.config(state='disabled')
        self.stream_port.config(state='disabled')
        self.update_time.config(state='disabled')
        self.use_save_file_chk.config(state='disabled')
        self.setBtn.config(state='disabled')

    def tear_down(self):
        if not self.d_bridge:
            return
        self.d_bridge.tear_down()
        print('waiting on join')
        self.bridge_thread.join()
        print('joined')
