import tkinter as tk
    

class App():
    def __init__(self, master):
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
       

    def live_state(self):
        print('LIVE STATE')
        print('IM GOING TO KILL MYSELF IF THIS DOES NOT WORK :>')
        self.new_window = tk.Toplevel(self.master)
        self.app = Live(self.new_window)
    def building_state(self):
        print('BUILDING STATE')


class Start(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        #build = tk.Button(frame, text='Building state', fg='blue',
                               #command=lambda: controller.show_frame('Build'))
        #build.grid(column = 0, row = 0)
        live = tk.Button(self, text='Live state', fg='green', 
                         command=lambda: controller.show_frame('Live'))
        live.grid(row=0, column=1)
        build = tk.Button(self, text='Building state', fg='blue',
                          command=lambda: controller.show_frame('Build'))
        build.grid(row=0, column=0)


class Live(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        patrol = tk.Button(self, text='Patrol', fg='green',
                           command=lambda: print('WOOOOOHOOOOOO'))
        patrol.grid(row=0, column=1)
        back = tk.Button(self, text='Go back', fg='red',
                         command=lambda: controller.show_frame('Start'))
        back.grid(row=0, column=0)

    
class Build(tk.Frame):
     def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        back = tk.Button(self, text='Go back', fg='red',
                              command=lambda: controller.show_frame('Start'))
        back.grid(row=0, column=1)


if (__name__ == '__main__'):
    root = tk.Tk()
    app = App(root)
    root.mainloop()
    root.destroy()

