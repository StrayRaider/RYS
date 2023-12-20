import tkinter as tk
from tkinter import ttk

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
        print(self.controller.deskCount)
        print(self.controller.waiterCount)
        print(self.controller.checkoutCount)
        print(self.controller.chefCount)
  
# Driver Code
app = tkinterApp()
app.mainloop()
