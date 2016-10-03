#Requires a compass conntected to port 3, a color sensor to port 4, a IR sensor to port 2 and a tilt sensor on port 1

import tkinter as tk
from ev3 import Ev3
from client import Receiver
from PIL import Image, ImageTk
import math
import socket
class Interface():
    def __init__(self):
        #everything for ev3 data
        #between 0 and 360
        self.__compass_heading=0
        #between 0 and 100
        self.__distance=100
        #between 0 and 360
        self.__tiltX=0
        #between 0 and 360
        self.__tiltY=0
        #between 0 and 100
        self.__brightness=0
        self.__connected=False
        self.__ev3=None
        self.__camera=None
        self.__image=None
        image = Image.open("picture.jpg")
        self.__image_update=0
        
        #everything for interface
        self.__root=tk.Tk()
        self.__image = ImageTk.PhotoImage(image)
        self.__root.resizable(True, True)
        self.__screenWidth=int(self.__root.winfo_screenwidth()*0.4)
        self.__screenHeight=int(self.__root.winfo_screenheight()*0.6)
        self.__root.minsize(self.__screenWidth,self.__screenHeight)
        self.__root.grid()
        self.__root.title("Ev3 command panel")
        self.__root.config(bg='white')
        self.__root.update()
        self.__window_width=self.__root.winfo_width()
        self.__window_height=self.__root.winfo_height()
        
        self.__root.rowconfigure(0,weight=1)
        self.__root.rowconfigure(1,weight=1)
        self.__root.rowconfigure(2,weight=1)
        self.__root.rowconfigure(3,weight=1)
        self.__root.rowconfigure(4,weight=1)
        self.__root.columnconfigure(0,weight=1)
        self.__root.columnconfigure(1,weight=1)
        self.__root.columnconfigure(2,weight=1)
        
        #frame for displaying video
        self.__videoFrame=tk.Frame(self.__root,bg="white",width=self.__window_width/3,height=self.__window_height/3)
        self.__videoFrame.grid(row = 0, column = 2,columnspan=3)
        
        self.__imageLabel = tk.Label(self.__videoFrame,width=int(self.__window_width/3),height=int(self.__window_height/3))
        self.__imageLabel.place(relx=0.5,rely=0.5,anchor=tk.CENTER)
        
        #frame for connecting
        self.__connectFrame=tk.Frame(self.__root,bg="white",width=self.__window_width/3,height=self.__window_height/3)
        self.__connectFrame.grid(row = 0, column = 0,)
        self.__connect_button=tk.Button(self.__connectFrame, text="connect", width=15, command=self.connectFunction)
        self.__connect_button.place(relx=0.50,rely=0.30,anchor=tk.CENTER)
        
        self.__ip_entry = tk.Entry(self.__connectFrame)
        self.__ip_entry.place(relx=0.50,rely=0.60,anchor=tk.CENTER)
        self.__ip_entry.delete(0, tk.END)
        self.openConfigFile()
        self.__ip_entry.insert(0, self.__ip_adress)
        
        #frame for displaying motorspeed
        self.__motorFrame=tk.Frame(self.__root,bg="white",width=self.__window_width/3,height=self.__window_height/3)
        self.__motorFrame.grid(row = 0, column = 6,)
        
        self.__motorCanvas=tk.Canvas(self.__motorFrame,width=self.__window_width/3,height=self.__window_height/3)
        self.__motorCanvas.place(relx=0.5,rely=0.5,anchor=tk.CENTER)

        #frame for displaying compass
        self.__compassFrame=tk.Frame(self.__root,bg="white",width=self.__window_width/2-2,height=self.__window_height/3-2)
        self.__compassFrame.grid(row = 2, column = 0,columnspan=3)
        
        self.__compassCanvas=tk.Canvas(self.__compassFrame,width=self.__window_width/2-2,height=self.__window_height/3-2)
        self.__compassCanvas.place(relx=0.5,rely=0.5,anchor=tk.CENTER)        
        #frame for displaying distance
        self.__distanceFrame=tk.Frame(self.__root,bg="white",width=self.__window_width/2-2,height=self.__window_height/3-2)
        self.__distanceFrame.grid(row = 2, column = 4,columnspan=3)
        
        self.__distanceCanvas=tk.Canvas(self.__distanceFrame,width=self.__window_width/2-2,height=self.__window_height/3-2)
        self.__distanceCanvas.place(relx=0.5,rely=0.5,anchor=tk.CENTER)
        
        #frame for displaying tilt
        self.__tiltFrame=tk.Frame(self.__root,bg="white",width=self.__window_width/2-2,height=self.__window_height/3-2)
        self.__tiltFrame.grid(row = 4, column = 0,columnspan=3)
        
        self.__tiltCanvas=tk.Canvas(self.__tiltFrame,width=self.__window_width/2-2,height=self.__window_height/3-2)
        self.__tiltCanvas.place(relx=0.5,rely=0.5,anchor=tk.CENTER)
        
        #frame for displaying brightness
        self.__brightnessFrame=tk.Frame(self.__root,bg="white",width=self.__window_width/2-2,height=self.__window_height/3-2)
        self.__brightnessFrame.grid(row = 4, column = 4,columnspan=3)
        
        self.__brightnessCanvas=tk.Canvas(self.__brightnessFrame,width=self.__window_width/2-2,height=self.__window_height/3-2)
        self.__brightnessCanvas.place(relx=0.5,rely=0.5,anchor=tk.CENTER)
        
        #separators
        self.__Separator0=tk.Frame(self.__root,height=2,bd=1,relief=tk.SUNKEN)
        self.__Separator0.grid(row = 1, column = 0,sticky=tk.E+tk.W)
        
        self.__Separator1=tk.Frame(self.__root,height=2,bd=1,relief=tk.SUNKEN)
        self.__Separator1.grid(row = 1, column = 1,sticky=tk.E+tk.W)
        
        self.__Separator2=tk.Frame(self.__root,height=2,bd=1,relief=tk.SUNKEN)
        self.__Separator2.grid(row = 1, column = 2,sticky=tk.E+tk.W)
        
        self.__Separator3=tk.Frame(self.__root,height=2,bd=1,relief=tk.SUNKEN)
        self.__Separator3.grid(row = 3, column = 0,sticky=tk.E+tk.W)
        
        self.__Separator4=tk.Frame(self.__root,height=2,bd=1,relief=tk.SUNKEN)
        self.__Separator4.grid(row = 3, column = 1,sticky=tk.E+tk.W)
        
        self.__Separator5=tk.Frame(self.__root,height=2,bd=1,relief=tk.SUNKEN)
        self.__Separator5.grid(row = 3, column = 2,sticky=tk.E+tk.W)
        
        self.__Separator6=tk.Frame(self.__root,bg="black",height=2,bd=1,relief=tk.SUNKEN)
        self.__Separator6.grid(row = 2, column = 3,sticky=tk.N+tk.S)
        
        self.__Separator7=tk.Frame(self.__root,bg="black",height=2,bd=1,relief=tk.SUNKEN)
        self.__Separator7.grid(row = 3, column = 3,sticky=tk.N+tk.S)

        self.__Separator8=tk.Frame(self.__root,bg="black",height=2,bd=1,relief=tk.SUNKEN)
        self.__Separator8.grid(row = 4, column = 3,sticky=tk.S+tk.N)
        
        self.__Separator9=tk.Frame(self.__root,bg="black",height=2,bd=1,relief=tk.SUNKEN)
        self.__Separator9.grid(row = 0, column = 1,sticky=tk.S+tk.N)
        
        self.__Separator10=tk.Frame(self.__root,bg="black",height=2,bd=1,relief=tk.SUNKEN)
        self.__Separator10.grid(row = 0, column = 5,sticky=tk.S+tk.N)
        
        self.__Separator11=tk.Frame(self.__root,height=2,bd=1,relief=tk.SUNKEN)
        self.__Separator11.grid(row = 1, column = 3,sticky=tk.E+tk.W)
        
        self.__Separator12=tk.Frame(self.__root,height=2,bd=1,relief=tk.SUNKEN)
        self.__Separator12.grid(row = 1, column = 4,sticky=tk.E+tk.W)
        
        self.__Separator13=tk.Frame(self.__root,height=2,bd=1,relief=tk.SUNKEN)
        self.__Separator13.grid(row = 1, column = 5,sticky=tk.E+tk.W)
        
        self.__Separator14=tk.Frame(self.__root,height=2,bd=1,relief=tk.SUNKEN)
        self.__Separator14.grid(row = 1, column = 6,sticky=tk.E+tk.W)
        
        self.__Separator15=tk.Frame(self.__root,height=2,bd=1,relief=tk.SUNKEN)
        self.__Separator15.grid(row = 3, column = 4,sticky=tk.E+tk.W)
        
        self.__Separator16=tk.Frame(self.__root,height=2,bd=1,relief=tk.SUNKEN)
        self.__Separator16.grid(row = 3, column = 5,sticky=tk.E+tk.W)
        
        self.__Separator17=tk.Frame(self.__root,height=2,bd=1,relief=tk.SUNKEN)
        self.__Separator17.grid(row = 3, column = 6,sticky=tk.E+tk.W)
        
        #gives all canvases sizes
        self.__root.update()
        
        self.__compassLine=self.__compassCanvas.create_line(int(self.__compassCanvas.winfo_width()/2.0),int(self.__compassCanvas.winfo_height()/2.0),int(self.__compassCanvas.winfo_width()/2.0),int(self.__compassCanvas.winfo_height()/2.0-80),width=4,fill="black")
        tempx=int(self.__compassCanvas.winfo_width()/2.0)
        tempy=int(self.__compassCanvas.winfo_height()/2.0)
        self.__compassText=self.__compassCanvas.create_text(10,0,text="Compass",fill="black",anchor=tk.NW)
        self.__compassTextN=self.__compassCanvas.create_text(tempx,tempy-80,text="N",fill="black",anchor=tk.NW)
        self.__compassTextS=self.__compassCanvas.create_text(tempx,tempy+80,text="S",fill="black",anchor=tk.NW)
        self.__compassTextW=self.__compassCanvas.create_text(tempx-80,tempy,text="W",fill="black",anchor=tk.NW)
        self.__compassTextE=self.__compassCanvas.create_text(tempx+80,tempy,text="E",fill="black",anchor=tk.NW)
        
        self.__distanceBar=self.__distanceCanvas.create_rectangle(int(self.__distanceCanvas.winfo_width()*0.40),int(self.__distanceCanvas.winfo_height()*0.90),int(self.__distanceCanvas.winfo_width()*0.60),int(self.__distanceCanvas.winfo_height()*0.1),fill="green")
        self.__distanceText=self.__distanceCanvas.create_text(10,0,text="Distance",fill="black",anchor=tk.NW)
        
        self.__tiltLineX=self.__tiltCanvas.create_line(int(self.__tiltCanvas.winfo_width()*0.25-70),int(self.__tiltCanvas.winfo_height()*0.5),int(self.__tiltCanvas.winfo_width()*0.25+70),int(self.__tiltCanvas.winfo_height()*0.5),width=4,fill="black")
        self.__tiltLineY=self.__tiltCanvas.create_line(int(self.__tiltCanvas.winfo_width()*0.75-70),int(self.__tiltCanvas.winfo_height()*0.5),int(self.__tiltCanvas.winfo_width()*0.75+70),int(self.__tiltCanvas.winfo_height()*0.5),width=4,fill="black")
        self.__tiltText=self.__tiltCanvas.create_text(10,0,text="Tilt",fill="black",anchor=tk.NW)
        tempx=int(self.__tiltCanvas.winfo_width()*0.)
        self.__tiltTextX=self.__tiltCanvas.create_text(int(self.__tiltCanvas.winfo_width()*0.25),int(self.__tiltCanvas.winfo_height()*0.25),text="X angle",fill="black",anchor=tk.NW)
        self.__tiltTextY=self.__tiltCanvas.create_text(int(self.__tiltCanvas.winfo_width()*0.75),int(self.__tiltCanvas.winfo_height()*0.25),text="Y angle",fill="black",anchor=tk.NW)
        
        self.__brightnessBar=self.__brightnessCanvas.create_rectangle(int(self.__brightnessCanvas.winfo_width()*0.40),int(self.__brightnessCanvas.winfo_height()*0.90),int(self.__brightnessCanvas.winfo_width()*0.60),int(self.__brightnessCanvas.winfo_height()*0.1),fill="green")
        self.__brightnessText=self.__brightnessCanvas.create_text(10,0,text="Brightness",fill="black",anchor=tk.NW)
        
        self.__root.after(100, self.update_sensors)
        self.__root.mainloop()
        
    def openConfigFile(self):
        try:
            config_file = open("config.txt", "r")
            self.__ip_adress=config_file.read()
            config_file.close()
        except IOError as e:
            self.__ip_adress="0.0.0.0"
            config_file = open("config.txt", "w")
            config_file.write(self.__ip_adress)
            config_file.close()
        
    def connectFunction(self):
        ip_adress=self.__ip_entry.get()
        valid=True
        try:
            socket.inet_aton(ip_adress)
            self.__ip_adress=ip_adress
            config_file=open("config.txt", "w")
            config_file.truncate()
            config_file.write(self.__ip_adress)
            config_file.close()
        except (socket.error,AttributeError):
            valid=False
            self.handleInternalErrors("invalid ip")
        if valid:
            try:
                self.__ev3=Ev3(self.__ip_adress)
                self.__connect_button.config(state=tk.DISABLED)
                # self.__compass=self.__ev3.add_sensor(3,"compass")
                self.__color=self.__ev3.add_sensor(4,"color")
                self.__ir=self.__ev3.add_sensor(2,"IR")
                self.__accelerometer=self.__ev3.add_sensor(1,"accelerometer")
                print("hello")
            except socket.error:
                self.handleInternalErrors("connection refused")
    def disconnect(self):
        pass
    def handleInternalErrors(self,error):
        print(error)
        if error=="broken connection":
            self.__gloria=None
            self.__camera=None
            self.__connect_button.config(text="connect",command=self.connectFunction,state=tk.NORMAL)
    #get all values from ev3 here
    def update_sensor_values(self):
        if not self.__ev3:
            self.__compass_heading+=30
            if self.__compass_heading>360:
                self.__compass_heading=0
            self.__distance+=10
            if self.__distance>100:
                self.__distance=0
            self.__brightness+=10
            if self.__brightness>100:
                self.__brightness=0
            self.__tiltX+=10
            if self.__tiltX>360:
                self.__tiltX=0
            self.__tiltY+=10
            if self.__tiltY>360:
                self.__tiltY=0
        else:
            # self.__compass_heading=self.__compass.get_direction()
            temp=self.__accelerometer.get_tilt()
            self.__tiltX=temp[0]
            self.__tiltY=temp[1]
            self.__distance=self.__ir.get_prox()
            self.__brightness=100-self.__color.get_ambient()
            
        self.__image_update+=1
        if self.__image_update>=20:
            self.__image_update=0
        
    def update_sensors(self):
        self.update_sensor_values()
        self.updata_compass()
        self.update_distance()
        self.update_tilt()
        self.update_brightness()
        self.update_image()
        self.__root.after(100, self.update_sensors)
        self.__root.update()
    def update_tilt(self):
        position=[self.__tiltCanvas.winfo_width()*0.25,self.__tiltCanvas.winfo_height()*0.5]
        temp_list=[]
        temp_list.append(int(position[0]+35*math.cos((self.__tiltX/180.0)*math.pi)))
        temp_list.append(int(position[1]+35*math.sin((self.__tiltX/180.0)*math.pi)))
        temp_list.append(int(position[0]-35*math.cos((self.__tiltX/180.0)*math.pi)))
        temp_list.append(int(position[1]-35*math.sin((self.__tiltX/180.0)*math.pi)))
        self.__tiltCanvas.coords(self.__tiltLineX,tuple(temp_list))
        
        position=[self.__tiltCanvas.winfo_width()*0.75,self.__tiltCanvas.winfo_height()*0.5]
        temp_list=[]
        temp_list.append(int(position[0]+35*math.cos((self.__tiltY/180.0)*math.pi)))
        temp_list.append(int(position[1]+35*math.sin((self.__tiltY/180.0)*math.pi)))
        temp_list.append(int(position[0]-35*math.cos((self.__tiltY/180.0)*math.pi)))
        temp_list.append(int(position[1]-35*math.sin((self.__tiltY/180.0)*math.pi)))
        self.__tiltCanvas.coords(self.__tiltLineY,tuple(temp_list))
    def update_image(self):
        self.__imageLabel.imgtk = self.__image
        self.__imageLabel.configure(image=self.__image)
        
        
    def update_distance(self):
        temp_list=self.__distanceCanvas.coords(self.__distanceBar)
        temp_list[1]=(self.__distance/100.0)*0.9*self.__distanceCanvas.winfo_height()
        self.__distanceCanvas.coords(self.__distanceBar,tuple(temp_list))
    
    def update_brightness(self):
        temp_list=self.__brightnessCanvas.coords(self.__brightnessBar)
        temp_list[1]=(self.__brightness/100.0)*0.9*self.__brightnessCanvas.winfo_height()
        self.__brightnessCanvas.coords(self.__brightnessBar,tuple(temp_list))
    def updata_compass(self):
        temp_list=self.__compassCanvas.coords(self.__compassLine)
        temp_list1=[]
        temp_list1.append(temp_list[0])
        temp_list1.append(temp_list[1])
        temp_list1.append(int(temp_list[0]+80*math.cos((self.__compass_heading/180.0)*math.pi)))
        temp_list1.append(int(temp_list[1]+80*math.sin((self.__compass_heading/180.0)*math.pi)))
        self.__compassCanvas.coords(self.__compassLine,tuple(temp_list1))
        self.__root.update()
temp=Interface()
