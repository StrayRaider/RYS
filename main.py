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
        self.waiterS = 0
        self.checkoutS = 0
        self.cookmealS = 0
        self.eatmealS = 0
        self.clientTimeout = 0
         
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
        self.deskentery.insert(0, 6)

        cheflabel = ttk.Label(self, text="Enter Chef Number")
        cheflabel.grid(row = 2, column = 2, padx = 10, pady = 10)

        self.chefentery =ttk.Entry(self, width=35)
        self.chefentery.grid(row = 2, column = 3, padx = 10, pady = 10)
        self.chefentery.insert(0, 2)

        waiterlabel = ttk.Label(self, text="Enter Waiter Number")
        waiterlabel.grid(row = 3, column = 2, padx = 10, pady = 10)

        self.waiterentery =ttk.Entry(self, width=35)
        self.waiterentery.grid(row = 3, column = 3, padx = 10, pady = 10)
        self.waiterentery.insert(0, 3)

        checkoutlabel = ttk.Label(self, text="Enter Checkout Number")
        checkoutlabel.grid(row = 4, column = 2, padx = 10, pady = 10)

        self.checkoutentery =ttk.Entry(self, width=35)
        self.checkoutentery.grid(row = 4, column = 3, padx = 10, pady = 10)
        self.checkoutentery.insert(0, 1)

        waiterSlabel = ttk.Label(self, text="Enter Waiter Sleep Time")
        waiterSlabel.grid(row = 5, column = 2, padx = 10, pady = 10)

        self.waiterSentery =ttk.Entry(self, width=35)
        self.waiterSentery.grid(row = 5, column = 3, padx = 10, pady = 10)
        self.waiterSentery.insert(0, 2)

        checkoutSlabel = ttk.Label(self, text="Enter Checkout Sleep Time")
        checkoutSlabel.grid(row = 6, column = 2, padx = 10, pady = 10)

        self.checkoutSentery =ttk.Entry(self, width=35)
        self.checkoutSentery.grid(row = 6, column = 3, padx = 10, pady = 10)
        self.checkoutSentery.insert(0, 1)

        cookmealSlabel = ttk.Label(self, text="Enter Cook Meal Sleep Time")
        cookmealSlabel.grid(row = 7, column = 2, padx = 10, pady = 10)

        self.cookmealSentery =ttk.Entry(self, width=35)
        self.cookmealSentery.grid(row = 7, column = 3, padx = 10, pady = 10)
        self.cookmealSentery.insert(0, 3)

        eatmealSlabel = ttk.Label(self, text="Enter Eat Meal Sleep Time")
        eatmealSlabel.grid(row = 8, column = 2, padx = 10, pady = 10)

        self.eatmealSentery =ttk.Entry(self, width=35)
        self.eatmealSentery.grid(row = 8, column = 3, padx = 10, pady = 10)
        self.eatmealSentery.insert(0, 3)

        clientTimeoutlabel = ttk.Label(self, text="Enter Client Timeout")
        clientTimeoutlabel.grid(row = 9, column = 2, padx = 10, pady = 10)

        self.clientTimeoutentery =ttk.Entry(self, width=35)
        self.clientTimeoutentery.grid(row = 9, column = 3, padx = 10, pady = 10)
        self.clientTimeoutentery.insert(0, 20)


        button1 = ttk.Button(self, text ="Start",
                            command = lambda : self.startProblem1(controller))
     
        # putting the button in its place 
        # by using grid
        button1.grid(row = 10, column = 2, padx = 10, pady = 10)

    def startProblem1(self,controller):
        controller.deskCount = self.deskentery.get()
        controller.chefCount = self.chefentery.get()
        controller.waiterCount = self.waiterentery.get()
        controller.checkoutCount = self.checkoutentery.get()
        controller.waiterS = self.waiterSentery.get()
        controller.checkoutS = self.checkoutSentery.get()
        controller.cookmealS = self.cookmealSentery.get()
        controller.eatmealS = self.eatmealSentery.get()
        controller.clientTimeout = self.clientTimeoutentery.get()
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
            
            furnance1 = ttk.Label(self,text="f1")
            furnance1.grid(row = chefIndex+2, column = 16, padx = 10, pady = 10)

            furnance2 = ttk.Label(self,text="f2")
            furnance2.grid(row = chefIndex+2, column = 17, padx = 10, pady = 10)

            button= ttk.Button(self,text="+")
            button.grid(row = chefIndex+2, column = 18, padx = 10, pady = 10)

            self.chef.append([label,label2,button,furnance1,furnance2])




        showOrderCount= ttk.Label(self,text="alinacak siparis sayisi")
        showOrderCount.grid(row = 1, column = 6, padx = 10, pady = 10)
        showFoodCount= ttk.Label(self,text="hazirlacak siparis sayisi")
        showFoodCount.grid(row = 1, column = 14, padx = 10, pady = 10)
        ################
        waiterTakeTheOrderBtn= ttk.Button(self,text="siparis al",command = lambda : daemon.waiterBtn(showOrderCount))
        waiterTakeTheOrderBtn.grid(row = int(self.controller.waiterCount)+4, column = 6, padx = 10, pady = 10)
        waiterSendOrderToChefBtn=ttk.Button(self,text="siparisi asciya ilet",command = lambda : daemon.sendOrderToChefBtn(showFoodCount))
        waiterSendOrderToChefBtn.grid(row = int(self.controller.waiterCount)+4, column = 7, padx = 10, pady = 10)
        startCookBtn=ttk.Button(self,text="siparisi hazirlamaya basla",command = lambda : daemon.chefCookBtn(showFoodCount))
        startCookBtn.grid(row = int(self.controller.chefCount)+4, column = 15, padx = 10, pady = 10)
        startPaymentBtn=ttk.Button(self,text="odemeleri al",command = lambda : daemon.paymentBtn())
        startPaymentBtn.grid(row = int(self.controller.checkoutCount)+4, column = 11, padx = 10, pady = 10)
        ##################

        labelClient = ttk.Label(self,text="musteri sayisini giriniz")
        labelClient.grid(row =  int(self.controller.waiterCount)+6, column = 3, padx = 10, pady = 10)
        clientEntery =ttk.Entry(self, width=15)
        clientEntery.grid(row =int(self.controller.waiterCount)+6, column = 4, padx = 10, pady = 10)
        labelPrimClient = ttk.Label(self,text="öncelikli musteri sayisini giriniz")
        labelPrimClient.grid(row = int(self.controller.waiterCount)+6, column = 5, padx = 10, pady = 10)
        primClientEntery =ttk.Entry(self, width=15)
        primClientEntery.grid(row = int(self.controller.waiterCount)+6, column = 6, padx = 10, pady = 10)
        clientButton= ttk.Button(self,text="müşteri giris",command = lambda : daemon.createcustomer(int(clientEntery.get()),int(primClientEntery.get()),self.desk))
        clientButton.grid(row = int(self.controller.waiterCount)+6, column = 7, padx = 10, pady = 10)

        daemonThread = threading.Thread(target=daemon.start, args=(int(self.controller.deskCount), int(self.controller.waiterCount),
                                                                   int(self.controller.checkoutCount), int(self.controller.chefCount),
                                                                   self.desk,self.waiter,self.checkout,self.chef, int(self.controller.waiterS),
                                                                   int(self.controller.checkoutS) ,int(self.controller.cookmealS) ,
                                                                   int(self.controller.eatmealS), int(self.controller.clientTimeout)))
        daemonThread.start()

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
        #app.after(500, self.updateStates)

  
# Driver Code
app = tkinterApp()
app.mainloop()
