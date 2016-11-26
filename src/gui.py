import tkinter as tk
from thread import GuardDog
import follow_tape
import idle

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

        self.show_frame(Start.__name__)

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def create_buttons(frame, buttons, cols):
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
        ip_entry.grid(sticky=tk.W+tk.E, row=4)

        buttons = [
            ['Live state', lambda: controller.show_frame(Live.__name__)],
            ['Building state', lambda: controller.show_frame(Build.__name__)],
            ['connect', lambda: controller.gd.connect(ip_entry.get())],
        ]
        App.create_buttons(self, buttons, 1)


class Live(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        buttons = [
            ['Patrol', lambda: controller.gd.set_mode(patrol.Patrol)],
            ['Follow Tape', lambda: controller.gd.set_mode(follow_tape.FollowTape)],
            ['Idle', lambda: controller.gd.set_mode(idle.IdleMode)],
            ['Go back', lambda: controller.show_frame(Start.__name__)],
        ]
        App.create_buttons(self, buttons, 1)


class Build(tk.Frame):
     def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        buttons = [
            ['Go back', lambda: controller.show_frame(Start.__name__)],
        ]
        App.create_buttons(self, buttons, 1)


if (__name__ == '__main__'):
    root = tk.Tk()
    app = App(root)
    root.mainloop()
    app.gd.kill()
