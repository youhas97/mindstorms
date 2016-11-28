import tkinter as tk
from thread import GuardDog
import follow_tape
import idle

class App():
    def __init__(self, master):
        self.gd = GuardDog()
        self.master = master

        container= tk.Frame(master, width=500, height=300)
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
        ip_entry.place(relx=.05 , rely=.9)
        connect_btn = tk.Button(self, text='connect', fg='white',
                                command=lambda: controller.gd.connect(ip_entry.get()))
        connect_btn.place(relx=.05 , rely=.8)
        live_btn = tk.Button(self, text='Live state', fg='white',
                             command=lambda: controller.show_frame('Live'),width=20)
        live_btn.place(relx=.05, rely=.05)
        build_btn = tk.Button(self, text='Building state', fg='white',
                              command=lambda: controller.show_frame('Build'),width=20)
        build_btn.place(relx=.05, rely=.15)
        


class Live(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        patrol_btn = tk.Button(self, text='Patrol', fg='white',
                           command=lambda: print('WOOOOOHOOOOOO'))
        patrol_btn.grid(sticky=tk.W+tk.E, row=1)
        back_btn = tk.Button(self, text='Go back', fg='white',
                         command=lambda: controller.show_frame('Start'))
        back_btn.grid(sticky=tk.W+tk.E, row=4)
        follow_tape_btn = tk.Button(self, text='Follow Tape', fg='white',
                command=lambda: controller.gd.set_mode(follow_tape.FollowTape))
        follow_tape_btn.grid(sticky=tk.W+tk.E, row=2)
        idle_btn = tk.Button(self, text='Idle', fg='white',
                        command=lambda: controller.gd.set_mode(idle.IdleMode))
        idle_btn.grid(sticky=tk.W+tk.E, row=3)
        

class Build(tk.Frame):
     def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        back_btn = tk.Button(self, text='Go back', fg='white',
                                command=lambda: controller.show_frame('Start'))
        back_btn.grid(sticky=tk.W+tk.E, row=2)
        


if (__name__ == '__main__'):
    root = tk.Tk()
    root.geometry('500x300+350+70')
    app = App(root)
    root.mainloop()
    app.gd.kill()
