import tkinter as tk
from thread import GuardDog

class App():
    def __init__(self, master):
        self.gd = GuardDog()
        self.master = master

        container= tk.Frame(master, width=300, height=300)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for Frame in (Start, Build, Live):
            page_name = Frame.__name__
            frame = Frame(parent=container, controller=self)
            self.frames[page_name] = frame
            
            frame.grid(row=0, column=0, sticky='nsew')
        
        self.show_frame('Start')

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class Start(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        ip_entry = tk.Entry(self)
        ip_entry.grid(row=0, column=2)
        connect_button = tk.Button(self, text='connect',
                                   command=lambda: controller.gd.connect(ip_entry.get()))
        connect_button.grid(row=1, column=2)
        live_button = tk.Button(self, text='Live state', fg='green', 
                         command=lambda: controller.show_frame('Live'))
        live_button.grid(row=0, column=1)
        build_button = tk.Button(self, text='Building state', fg='blue',
                          command=lambda: controller.show_frame('Build'))
        build_button.grid(row=0, column=0)


class Live(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        patrol_button = tk.Button(self, text='Patrol', fg='green',
                           command=lambda: print('WOOOOOHOOOOOO'))
        patrol_button.grid(row=0, column=1)
        back_button = tk.Button(self, text='Go back', fg='red',
                         command=lambda: controller.show_frame('Start'))
        back_button.grid(row=0, column=0)

    
class Build(tk.Frame):
     def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        back_button = tk.Button(self, text='Go back', fg='red',
                                command=lambda: controller.show_frame('Start'))
        back_button.grid(row=0, column=1)


if (__name__ == '__main__'):
    root = tk.Tk()
    app = App(root)
    root.mainloop()
