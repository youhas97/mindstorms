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
        
        self.add_subframes()
        self.create_mode_frames()

        self.show_frame(Start.__name__)

    def add_subframes(self):
        """Add container and data side pane."""
        self.container = tk.Frame(self.master, width=150, height=500)
        self.container.pack(side='left', fill='both', expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        data = Data(self.master, controller=self)
        data.pack(side='right', fill='both', expand=True)
        data.grid_rowconfigure(0, weight=1)

    def create_mode_frames(self):
        """Create objects for mode frames."""
        self.frames = {}
        for Frame in (Start, Live, Patrol):
            page_name = Frame.__name__
            frame = Frame(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky='nsew')

    def show_frame(self, page_name):
        """Raise a frame to the top."""
        frame = self.frames[page_name]
        frame.tkraise()
        frame.show()

    def create_buttons(frame, buttons, width=0):
        """Create button objects.

        Parameters:
            frame -- tk frame to place buttons inside.
            buttons -- list of titles and commands for buttons.
            width -- the width of all the buttons.

        Returns:
            buttons_dict -- a dictionary of all buttons
                            with the title as key.
        """
        button_dict = {}
        for index, button in enumerate(buttons):
            tk_btn = tk.Button(
                frame,
                text=button[0],
                command=button[1],
                width=width
            )
            button_dict[button[0]] = tk_btn
        return button_dict


class Data(tk.Frame):
    """Side pane for data."""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.create_data_field('Speed', controller.gd.actual_speed_str, (0,0.05))
        self.create_data_field('Distance', controller.gd.distance_str, (0,0.35))

    def create_data_field(self, title, variable, pos):
        """Create a label with a title and data output."""
        title_lbl = tk.Label(self, text=title)
        data_lbl = tk.Label(
            self,
            textvariable=variable,
            font=('Helvetica', 40)
        )
        title_lbl.pack()
        data_lbl.pack()
        title_lbl.place(relx=pos[0], rely=pos[1])
        data_lbl.place(relx=pos[0], rely=pos[1]+0.05)


class ModeFrame(tk.Frame):
    """Parent class for all mode frames."""
    
    def __init__(self, parent, controller):
        """Init frame and add back button."""
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        if self.__class__ != Start:
            back_btn = tk.Button(
                self,
                text='Back',
                command=lambda: controller.show_frame(Start.__name__),
                width=10
            )
            back_btn.place(relx=0.05, rely=0.85)

    def show(self):
        """Is run when frame is raised to top."""
        pass


class Start(ModeFrame):
    """Starting frame for GUI."""

    def __init__(self, parent, controller):
        """Add widgets."""
        super().__init__(parent, controller)

        ip_entry = tk.Entry(self)
        ip_entry.place(relx=.05 , rely=.9)

        buttons = [
            ['Live state', lambda: controller.show_frame(Live.__name__)],
            ['Patrol', lambda: controller.show_frame(Patrol.__name__)],
            ['connect', lambda: controller.gd.connect(ip_entry.get())],
        ]
        dir_btns = App.create_buttons(self, buttons, width=10)
        dir_btns['Live state'].place(relx=.05, rely=.05)
        dir_btns['Patrol'].place(relx=.05, rely=.15)
        dir_btns['connect'].place(relx=.05 , rely=.8)


class Live(ModeFrame):
    """Live mode frame."""

    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        self.add_buttons()

    def add_buttons(self):
        dir_btns_commands = [
            ['Forward', lambda: print('Up')],
            ['Left', lambda: print('Left')],
            ['Right', lambda: print('Right')],
            ['Back', lambda: print('Down')],
        ]
        
        dir_btns = App.create_buttons(self, dir_btns_commands, width=6)
        dir_btns['Forward'].place(relx=0.35, rely=0.1)
        dir_btns['Left'].place(relx=0.05,rely=.3)
        dir_btns['Right'].place(relx=0.65, rely=0.3)
        dir_btns['Back'].place(relx=0.35, rely=0.5)

    def show(self):
        """Start live mode and bind keys."""
        gd = self.controller.gd
        if gd.unit:
            self.controller.gd.set_mode(live.LiveMode)
            self.controller.gd.queue_command(
                command=lambda: gd.mode.bind_keys(self.controller.master),
                condition=lambda: isinstance(gd.mode, live.LiveMode)
            )


class Patrol(ModeFrame):
    """Patrol mode frame."""

    def __init__(self, parent, controller):
        """Add widgets."""
        super().__init__(parent, controller)
        
        self.add_radio_buttons()

    def add_radio_buttons(self):
        mode = tk.IntVar()
        radio_peace = tk.Radiobutton(
            self,
            text="Peaceful",
            command=lambda: self.controller.gd.queue_command(
                command=lambda: self.controller.gd.mode.set_mode(patrol.Patrol.PEACEFUL),
                condition=lambda: isinstance(self.controller.gd.mode, patrol.Patrol)
            ),
            variable=mode,
            value=0,
        ).pack()
        radio_peace = tk.Radiobutton(
            self,
            text="Guard",
            command=lambda: self.controller.gd.queue_command(
                command=lambda: self.controller.gd.mode.set_mode(patrol.Patrol.GUARD),
                condition=lambda: isinstance(self.controller.gd.mode, patrol.Patrol)
            ),
            variable=mode,
            value=1
        ).pack()

    def show(self):
        """Start patrol mode."""
        if self.controller.gd.unit:
            self.controller.gd.set_mode(patrol.Patrol)


if (__name__ == '__main__'):
    root = tk.Tk()
    root.geometry('500x300+350+70')
    app = App(root)
    root.mainloop()
