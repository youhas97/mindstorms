#Requires a camera connected to the EV3s usb
from client import Receiver
import time
import Tkinter
test = Receiver("10.42.0.3", "pygame", (320, 240))
root = Tkinter.Tk()
lmain = Tkinter.Label(root)
lmain.pack()
while True:
    temp = test.get_frame()
    lmain.imgtk = temp
    lmain.configure(image=temp)
    root.update()
    time.sleep(0.1)