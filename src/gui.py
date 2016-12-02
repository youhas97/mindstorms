import tkinter as tk
from unit import *
from thread import GuardDog

import follow_tape
import idle
import patrol
import live

class App():
    """Root frame of GUI."""

    def __init__(self, master):
        self.gd = GuardDog()
        self.master = master

        container = tk.Frame(master, width=150, height=500)
        container.pack(side='left', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        data = Data(master, controller=self)
        data.pack(side='right', fill='both', expand=True)
        data.grid_rowconfigure(0, weight=1)
        data.grid_columnconfigure(1, weight=1)

        self.frames = {}
        for Frame in (Start, Live):
            page_name = Frame.__name__
            frame = Frame(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame(Start.__name__)

    def show_frame(self, page_name):
        """Raise a frame to the top."""
        frame = self.frames[page_name]
        frame.tkraise()
        frame.show()

    def create_buttons(frame, buttons, width=0, cols=1):
        """Create buttons in a grid pattern.

        Parameters:
            frame -- tk frame to place buttons inside.
            buttons -- list of titles and commands for buttons.
            cols -- the amount of colums in the grid.
        """
        button_dict = {}
        for index, button in enumerate(buttons):
            row = index // cols
            col = index % cols
            tk_btn = tk.Button(frame,
                               text=button[0],
                               command=button[1],
                               width=width)
            tk_btn.grid(sticky=tk.W+tk.E, row=row, column=col)
            button_dict[button[0]] = tk_btn
        return button_dict


class Start(tk.Frame):
    """Starting frame for GUI."""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        ip_entry = tk.Entry(self)
        ip_entry.place(relx=.05 , rely=.9)

        buttons = [
            ['Live state', lambda: controller.show_frame(Live.__name__)],
            ['connect', lambda: controller.gd.connect(ip_entry.get())],
        ]
        buttons_dict = App.create_buttons(self, buttons)
        buttons_dict['Live state'].place(relx=.05, rely=.05)
        buttons_dict['connect'].place(relx=.05 , rely=.8)

    def show(self):
        pass


class Data(tk.Frame):
    """Side pane for data."""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.create_data_field('Speed', controller.gd.actual_speed_str, (0,2))
        self.create_data_field('Distance', controller.gd.distance_str, (1,2))

    def create_data_field(self, title, variable, pos):
        title_lbl = tk.Label(self, text=title)
        title_lbl.place(relx=pos[0], rely=pos[1])
        data_lbl = tk.Label(self,
                            textvariable=variable,
                            font=('Helvetica', 40))
        data_lbl.place(relx=pos[0], rely=pos[1]+0.05)
        title_lbl.pack()
        data_lbl.pack()


class Live(tk.Frame):
    """Live mode frame."""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        buttons =[
            ['Forward', lambda: print('forward')],
            ['Back', lambda: print('back')],
            ['Left', lambda: print('left')],
            ['Right', lambda: print('right')],
        ]
        
        buttons_dict = App.create_buttons(self, buttons, width=6)
        buttons_dict['Left'].place(relx=0.05,rely=.3)
        buttons_dict['Forward'].place(relx=0.35, rely=0.1)
        buttons_dict['Right'].place(relx=0.65, rely=0.3)
        buttons_dict['Back'].place(relx=0.35, rely=0.5)

    def show(self):
        if not self.controller.gd.unit is None:
            self.controller.gd.set_mode(live.LiveMode)
            live_mode.bind_keys(self.controller.master)


if (__name__ == '__main__'):
    root = tk.Tk()
    root.geometry('500x300+350+70')
    app = App(root)
    root.mainloop()
