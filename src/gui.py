import tkinter as tk

class App():
    
    def __init__(self, master):
        frame = tk.Frame(master, width=300, height=300)
        frame.grid()
        
        self.build = tk.Button(
            frame, text="Building state", fg="blue", command=self.building_state)
        self.build.grid(column = 0, row = 0)

        self.live = tk.Button(frame, text="Live state", fg="green", command=self.live_state)
        self.live.grid(row=0, column=1)

        self.exit = tk.Button(frame, text="Exit program", fg="red", command=frame.quit)
        self.exit.grid(sticky=tk.S, column = 2, row = 0)

    def live_state(self):
        print("LIVE STATE INITIALIZED")
    def building_state(self):
        print("BUILDING STATE INITALIZED")

root = tk.Tk()


app = App(root)

root.mainloop()
root.destroy()
