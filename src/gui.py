import tkinter as tk
from unit import *
from thread import GuardDog

import follow_tape
import idle
import patrol

class App():
    """Root frame of GUI."""

    def __init__(self, master):
        self.gd = GuardDog()
        self.master = master

        container= tk.Frame(master, width=500, height=300)
        container= tk.Frame(master, width=300, height=500)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for Frame in (Start, Build, Live):
            page_name = Frame.__name__
            frame = Frame(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame(Start.__name__)

    def show_frame(self, page_name):
        """Raise a frame to the top."""
        self.frames[page_name].tkraise()

    def create_buttons(frame, buttons, cols=1):
        """Create buttons in a grid pattern.

        Parameters:
            frame -- tk frame to place buttons inside.
            buttons -- list of titles and commands for buttons.
            cols -- the amount of colums in the grid.
        """
        for index, button in enumerate(buttons):
            row = index // cols
            col = index % cols
            tk_btn = tk.Button(frame,
                               text=button[0],
                               command=button[1])
            tk_btn.grid(sticky=tk.W+tk.E, row=row, column=col)


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
        test = tk.Label(self, text=controller.gd.actual_speed)
        test.pack()
        test.place(relx=.7,rely=.125)
       # ip_entry.grid(sticky=tk.W+tk.E, row=4)

        """buttons = [
            ['Live state', lambda: controller.show_frame(Live.__name__)],
            ['Building state', lambda: controller.show_frame(Build.__name__)],
            ['connect', lambda: controller.gd.connect(ip_entry.get())],
        ]
        App.create_buttons(self, buttons)"""


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
        

        """buttons = [
            ['Patrol', lambda: controller.gd.set_mode(patrol.Patrol)],
            ['Follow tape', lambda: controller.gd.set_mode(follow_tape.FollowTape)],
            ['Follow me', lambda: controller.gd.set_mode(lazyaf.GetOverHere())],
            ['Idle', lambda: controller.gd.set_mode(idle.IdleMode)],
        ]
        App.create_buttons(self, buttons, 2)"""

        speak_entry = tk.Entry(self)
        speak_entry.grid(sticky=tk.W+tk.E, row=3)
        speak_button = tk.Button(self,
            text='Speak', 
            command=lambda: controller.gd.unit.speak(speak_entry.get()))
        speak_button.grid(sticky=tk.W+tk.E, column=1, row=3)

        go_back_btn = tk.Button(self,
            text='Go back',
            command=lambda: controller.show_frame(Start.__name__))
        go_back_btn.grid(sticky=tk.W+tk.E, row=4)


class Build(tk.Frame):
     def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        back_btn = tk.Button(self, text='Go back', fg='white',
                                command=lambda: controller.show_frame('Start'))
        back_btn.grid(sticky=tk.W+tk.E, row=2)
        

        """buttons = [
            ['Go back', lambda: controller.show_frame(Start.__name__)],
        ]
        App.create_buttons(self, buttons)"""


if (__name__ == '__main__'):
    root = tk.Tk()
    root.geometry('500x300+350+70')
    app = App(root)
    root.mainloop()
    app.gd.kill()
