import tkinter as tk
from tkinter import ttk
from libs import client, daemon
import time
import threading

#waiter
#chef
#checkout

class tkinterApp(tk.Tk):
    def __init__(self, *args, **kwargs): 
        tk.Tk.__init__(self, *args, **kwargs)
        self.deskCount = 0
        self.chefCount = 0
        self.waiterCount = 0
        self.checkoutCount = 0
         
        # creating a container
        width= self.winfo_screenwidth()               
        height= self.winfo_screenheight()               
        self.geometry("%dx%d" % (width, height))
        container = tk.Frame(self)  
        container.pack(side = "top", fill = "both", expand = True) 
  
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
  
        # initializing frames to an empty array
        self.frames = {}  
  
        # iterating through a tuple consisting
        # of the different page layouts
        for F in (StartPage, Problem1, Problem2,P1Entery):
  
            frame = F(container, self)
  
            # initializing frame of that object from
            # startpage, page1, page2 respectively with 
            # for loop
            self.frames[F] = frame 
  
            frame.grid(row = 0, column = 0, sticky ="nsew")
  
        self.show_frame(StartPage)
  
    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
  
# first window frame startpage
  
class StartPage(tk.Frame):
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)
         
        # label of frame Layout 2
        label = ttk.Label(self, text ="Startpage")
         
        # putting the grid in its place by using
        # grid
        label.grid(row = 0, column = 2, padx = 10, pady = 10)
  
        button1 = ttk.Button(self, text ="Problem 1",
        command = lambda : controller.show_frame(P1Entery))
     
        # putting the button in its place by
        # using grid
        button1.grid(row = 1, column = 1, padx = 10, pady = 10)
  
        ## button to show frame 2 with text layout2
        button2 = ttk.Button(self, text ="Problem 2",
        command = lambda : controller.show_frame(Problem2))
     
        # putting the button in its place by
        # using grid
        button2.grid(row = 2, column = 1, padx = 10, pady = 10)

  
# second window frame page1 
class P1Entery(tk.Frame):

    def __init__(self, parent, controller):
         
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text ="Page 1")
        label.grid(row = 0, column = 4, padx = 10, pady = 10)
  
        # button to show frame 2 with text
        # layout2
        button1 = ttk.Button(self, text ="StartPage",
                            command = lambda : controller.show_frame(StartPage))
     
        # putting the button in its place 
        # by using grid
        button1.grid(row = 1, column = 1, padx = 10, pady = 10)
        # Create an Entry widget
        desklabel = ttk.Label(self, text="Enter Desk Number")
        desklabel.grid(row = 1, column = 2, padx = 10, pady = 10)

        self.deskentery =ttk.Entry(self, width=35)
        self.deskentery.grid(row = 1, column = 3, padx = 10, pady = 10)

        cheflabel = ttk.Label(self, text="Enter Chef Number")
        cheflabel.grid(row = 2, column = 2, padx = 10, pady = 10)

        self.chefentery =ttk.Entry(self, width=35)
        self.chefentery.grid(row = 2, column = 3, padx = 10, pady = 10)

        waiterlabel = ttk.Label(self, text="Enter Waiter Number")
        waiterlabel.grid(row = 3, column = 2, padx = 10, pady = 10)

        self.waiterentery =ttk.Entry(self, width=35)
        self.waiterentery.grid(row = 3, column = 3, padx = 10, pady = 10)

        checkoutlabel = ttk.Label(self, text="Enter Checkout Number")
        checkoutlabel.grid(row = 4, column = 2, padx = 10, pady = 10)

        self.checkoutentery =ttk.Entry(self, width=35)
        self.checkoutentery.grid(row = 4, column = 3, padx = 10, pady = 10)

        button1 = ttk.Button(self, text ="Start",
                            command = lambda : self.startProblem1(controller))
     
        # putting the button in its place 
        # by using grid
        button1.grid(row = 5, column = 2, padx = 10, pady = 10)

    def startProblem1(self,controller):
        controller.deskCount = self.deskentery.get()
        controller.chefCount = self.chefentery.get()
        controller.waiterCount = self.waiterentery.get()
        controller.checkoutCount = self.checkoutentery.get()
        controller.show_frame(Problem1)
        controller.frames[Problem1].start()
  
# third window frame page2
class Problem2(tk.Frame): 
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text ="Page 2")
        label.grid(row = 0, column = 4, padx = 10, pady = 10)
  
  
        # button to show frame 3 with text
        # layout3
        button2 = ttk.Button(self, text ="Startpage",
                            command = lambda : controller.show_frame(StartPage))
     
        # putting the button in its place by
        # using grid
        button2.grid(row = 2, column = 1, padx = 10, pady = 10)


# third window frame page2
class Problem1(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = ttk.Label(self, text ="Page 2")
        label.grid(row = 0, column = 4, padx = 10, pady = 10)
  
  
        # button to show frame 3 with text
        # layout3
        button2 = ttk.Button(self, text ="Startpage",
                            command = lambda : controller.show_frame(StartPage))
     
        # putting the button in its place by
        # using grid
        button2.grid(row = 2, column = 1, padx = 10, pady = 10)
    
    def start(self):
        #label = ttk.Label(self, text ="Page elif")
        #label.grid(row = 2, column = 5, padx = 10, pady = 10)
        self.desk=[]
        self.waiter=[]
        self.checkout=[]
        self.chef=[]
        print(self.controller.deskCount)
        print(self.controller.waiterCount)
        print(self.controller.checkoutCount)
        print(self.controller.chefCount)

        for deskIndex in range(int(self.controller.deskCount)):
            label = ttk.Label(self,text="masa")
            label.grid(row = deskIndex+2, column = 4, padx = 10, pady = 10)
            self.desk.append(label)
            spacelabel = ttk.Label(self,text=" ")
            spacelabel.grid(row = deskIndex+2, column = 5, padx = 10, pady = 10)
                        
        for waiterIndex in range(int(self.controller.waiterCount)):
            label = ttk.Label(self,text="garson")
            label.grid(row = waiterIndex+2, column = 6, padx = 10, pady = 10)
            label2 = ttk.Label(self,text="........")
            label2.grid(row = waiterIndex+2, column = 7, padx = 10, pady = 10)
            button= ttk.Button(self,text="+")
            button.grid(row = waiterIndex+2, column = 8, padx = 10, pady = 10)
                #command = lambda : controller.show_frame(StartPage))
            spacelabel = ttk.Label(self,text=" ")
            spacelabel.grid(row = waiterIndex+2, column = 9, padx = 10, pady = 10)

            self.waiter.append([label,label2,button])

        for checkoutIndex in range(int(self.controller.checkoutCount)):
            label = ttk.Label(self,text="kasa")
            label.grid(row = checkoutIndex+2, column = 10, padx = 10, pady = 10)
            label2 = ttk.Label(self,text="........")
            label2.grid(row = checkoutIndex+2, column =11 , padx = 10, pady = 10)
            button= ttk.Button(self,text="+")
            button.grid(row = checkoutIndex+2, column = 12, padx = 10, pady = 10)
            self.checkout.append([label,label2,button])

            spacelabel = ttk.Label(self,text=" ")
            spacelabel.grid(row = checkoutIndex+2, column = 13, padx = 10, pady = 10)

        for chefIndex in range(int(self.controller.chefCount)):
            label = ttk.Label(self,text="aşçı")
            label.grid(row = chefIndex+2, column = 14, padx = 10, pady = 10)
            label2 = ttk.Label(self,text="........")
            label2.grid(row = chefIndex+2, column = 15, padx = 10, pady = 10)
            button= ttk.Button(self,text="+")
            button.grid(row = chefIndex+2, column = 16, padx = 10, pady = 10)

            self.chef.append([label,label2,button])

            spacelabel = ttk.Label(self,text=" ")
            spacelabel.grid(row = chefIndex+2, column = 17, padx = 10, pady = 10)

        labelClient = ttk.Label(self,text="musteri sayisini giriniz")
        labelClient.grid(row = 10, column = 3, padx = 10, pady = 10)
        clientEntery =ttk.Entry(self, width=15)
        clientEntery.grid(row = 10, column = 4, padx = 10, pady = 10)
        labelPrimClient = ttk.Label(self,text="öncelikli musteri sayisini giriniz")
        labelPrimClient.grid(row = 10, column = 5, padx = 10, pady = 10)
        primClientEntery =ttk.Entry(self, width=15)
        primClientEntery.grid(row = 10, column = 6, padx = 10, pady = 10)
        clientButton= ttk.Button(self,text="müşteri giris")
        clientButton.grid(row = 10, column = 7, padx = 10, pady = 10,
                        command = lambda : daemon.createcustomer(clientEntery.get(),primClientEntery.get()))

        daemonThread = threading.Thread(target=daemon.start, args=(self.controller.deskCount, self.controller.waiterCount, self.controller.checkoutCount, self.controller.chefCount,))
        daemonThread.start()
        #daemonThread.join()
        #daemon.start(self.controller.deskCount, self.controller.waiterCount, self.controller.checkoutCount, self.controller.chefCount)
        self.updateStates()

    def updateStates(self):
        # get waiter id's
        style = ttk.Style()
        style.configure("waiterfree.TLabel", background="red", foreground='blue')
        style.configure("waiterbusy.TLabel", background="green", foreground='blue')

        index = 0
        for i in self.waiter:
            try:
                i[0].config(text= "garson ID : {}".format(daemon.waiterThreads[index].ident))
            except:
                print("waiter index error")
            index += 1
            i[0].config(style="waiterfree.TLabel")

        # get chef id's
        index = 0
        for i in self.chef:
            try:
                i[0].config(text= "aşçı ID : {}".format(daemon.chefThreads[index].ident))
            except:
                print("waiter index error")
            index += 1

        # get checkout id's
        index = 0
        for i in self.checkout:
            try:
                i[0].config(text= "kasa ID : {}".format(daemon.checoutThreads[index].ident))
            except:
                print("waiter index error")
            index += 1
        app.after(500, self.updateStates)

  
# Driver Code
app = tkinterApp()
app.mainloop()
