import threading
import time
import random
import queue
from tkinter import ttk

class ModifiedSemaphore:
    def __init__(self, initial):
        self.signal_count = initial
        self.condition = threading.Condition() 

    def wait(self):
        with self.condition: 
            while self.signal_count <= 0:
                self.condition.wait() 
            self.signal_count -= 1 

    def signal(self):
        with self.condition:
            self.signal_count += 1 
            self.condition.notify()
    
    def signaln(self,n):
        with self.condition:
            self.signal_count+=n
            for _ in range(n):
                self.condition.notify()
            
    def value(self):
        return self.signal_count 

# Dosyaya yazma işlemleri atomik olmazsa açma okuma ve yazma işlemleri çakışacaktır
# O yüzden dosyayı açıp ekleme yapma işlemleri atomik olmalı ve bir thread yazma işini bitirip kapatmadan diğeri açmamalı
with open('log.txt', 'w') as f:
    f.write("Daemon Started \n")
    f.close()


willTakedOrderCount=0

waiterSleep = 2
checkoutSleep = 1
cookmealSleep = 3
eatmealSleep = 3

writeLogMutex = threading.Semaphore()

def writeToLog(textToWrite):
    global writeLogMutex

    writeLogMutex.acquire()
    with open('log.txt', 'a') as f:
        f.write('{} \n'.format(textToWrite))
        f.close()
    writeLogMutex.release()

sMutex =  threading.Semaphore()


orderqueue = queue.Queue()
waiterQueue = queue.Queue()
readymealsqueue = queue.Queue()
eatedMeals = queue.Queue()
checkoutDonequeue = queue.Queue()

waiterThreads = []
checoutThreads = []
chefThreads = []
clientThreads=[]

waiterSemaphore = ModifiedSemaphore(0)
orderSemaphore = ModifiedSemaphore(0)

checkoutcameQueue = ModifiedSemaphore(0)
checkoutQueue = ModifiedSemaphore(0)

orderTook = ModifiedSemaphore(0)
checkoutDone = ModifiedSemaphore(0)

chefSemaphore = ModifiedSemaphore(0)
chefWaiterSemaphore = ModifiedSemaphore(0)

clientCount=10
primaryClientCount=2
deskCount=6
checkoutC=0

"""bariyer 6 kişi gelene kadar bekler"""
clientsId = [[0 for x in range(2)] for y in range(clientCount)]

barrier = None
e= threading.Event()
semaphore= threading.Semaphore()

customercount=0
deskQueue = queue.Queue()


takeOrderSemaphore=ModifiedSemaphore(0)
foodCount=0
def waiterBtn(showOrderCount):
    global willTakedOrderCount,foodCount
    #takeOrderSemaphore.signaln(waiterC)
    if willTakedOrderCount>=waiterC:
        takeOrderSemaphore.signaln(waiterC)
        willTakedOrderCount-=waiterC
        foodCount+=waiterC
    elif willTakedOrderCount<waiterC:
        takeOrderSemaphore.signaln(willTakedOrderCount)
        foodCount+=willTakedOrderCount
        willTakedOrderCount=0
    
    showOrderCount.config(text="alinacak siparis sayisi:"+str(willTakedOrderCount))



sendOrderToChefSemaphore=ModifiedSemaphore(0)
def sendOrderToChefBtn(showFoodCount):
    global foodCount
    sendOrderToChefSemaphore.signaln(chefC*2)
    showFoodCount.config(text="hazirlanacak siparis sayisi"+str(foodCount))


startCookSemaphore=ModifiedSemaphore(0)
def chefCookBtn(showFoodCount):
    global foodCount
    print(foodCount)

    if foodCount>=chefC:
        startCookSemaphore.signaln(chefC)
        foodCount-=chefC
    elif foodCount<chefC:
        startCookSemaphore.signaln(foodCount)
        foodCount=0
        
    showFoodCount.config(text="hazirlanacak siparis sayisi"+str(foodCount))



startPaymentSemaphore=ModifiedSemaphore(0)
def paymentBtn():
    startPaymentSemaphore.signaln(checkoutC)


def createcustomer(clientC, primaryClientCount,desklabels):
    global customercount, clientsId, clientCount,willTakedOrderCount
    e.clear()
    customercount = 0
    clientCount = clientC
    willTakedOrderCount=clientC

    clientsId = [[0 for x in range(2)] for y in range(clientCount)]
    for id in range(clientCount-primaryClientCount):#8 kez dönecek(8 tane thread oluşacak)
        clientsId[id][0]=id

    for id in range(primaryClientCount):#2 tane öncelikli thread oluşuyor
        clientsId[id+clientCount-primaryClientCount][0]=id+clientCount-primaryClientCount
        clientsId[id+clientCount-primaryClientCount][1]=1,

    for clientId in range(len(clientsId)):
        t=threading.Thread(target=calistir, args=(clientsId[clientId][0],desklabels))
        t.start()
        clientThreads.append(t)
        time.sleep(0.1)

def getmeal(target_data):
    global readymealsqueue
    while 1:
        my_queue = readymealsqueue
        temp_queue = queue.Queue()

        found = False
    # Dequeue elements until finding the target data or reaching the end of the queue
        while not my_queue.empty():
            item = my_queue.get()
            print("getted : ", item)

            if int(item) == int(target_data):
                print(f"Found {target_data} in the queue!")
                found = True
                break
            else:
                temp_queue.put(item)

        # Enqueue back the elements to the original queue
        while not temp_queue.empty():
            my_queue.put(temp_queue.get())

        if not found:
            print(f"{target_data} not found in the queue.")
        else:
            break

def getpayment(target_data):
    global checkoutDonequeue
    while 1:
        my_queue = checkoutDonequeue
        temp_queue = queue.Queue()

        found = False
    # Dequeue elements until finding the target data or reaching the end of the queue
        while not my_queue.empty():
            item = my_queue.get()
            print("getted : ", item)

            if int(item) == int(target_data):
                print(f"Found {target_data} in the queue!")
                found = True
                break
            else:
                temp_queue.put(item)

        # Enqueue back the elements to the original queue
        while not temp_queue.empty():
            my_queue.put(temp_queue.get())

        if not found:
            print(f"{target_data} not found in the queue.")
        else:
            break

def siparişVer(clientNo):
    writeToLog(f"{clientNo}. Waiter calling")
    orderSemaphore.signal()
    waiterSemaphore.wait()
    orderqueue.put(clientNo)
    writeToLog(f"{clientNo}. order created in queue -{clientNo}-")
    #yemeği yemeli
    writeToLog(f"{clientNo}. meal tooked and started to eat -{clientNo}-")
    getmeal(clientNo)
    orderTook.wait()
    time.sleep(eatmealSleep)
    writeToLog(f"{clientNo}. meal eated -{clientNo}-")
    eatedMeals.put(clientNo)
    pay(clientNo)

def pay(clientNo):
    writeToLog(f"{clientNo}. paymanet waiting client")
    """burada ödeme butonu fonksiyonu"""
    startPaymentSemaphore.wait()
    checkoutcameQueue.signal()
    checkoutQueue.wait()
    writeToLog(f"{clientNo}. paymanet done from client")
    getpayment(clientNo)
    checkoutDone.wait()
    customerDie(clientNo)

def customerDie(clientNo):
    writeToLog(f"{clientNo}. thread Leaving")

def oncelikli_masaya_yerlestir(clientNo):
    global barrier
    global customercount
    desk = False
    if clientsId[clientNo][1]!=0:
        waitBarrierTime = time.time() 
        barrier.acquire()
        getintoBarrierTime = time.time()
        timeout = getintoBarrierTime - waitBarrierTime
        print("timeout is here : ", timeout)
        if timeout > 20:
            print("this thread will be dead")
            writeToLog(f" client {clientNo} : thread dead")

            barrier.release()
            return
        desk = deskQueue.get()
        style = ttk.Style()
        style.configure("deskfull.TLabel", background="green", foreground='blue')
        desk.config(text= f"masa görevde no : {clientNo}",style="deskfull.TLabel")
        writeToLog(f"{clientNo}. thread sitted to Desk Primer")

    semaphore.acquire()
    customercount+=1
    if customercount==clientCount:#9+1==10 
        e.set()
    
    semaphore.release()

    if clientsId[clientNo][1]!=0:
        siparişVer(clientNo)
    if desk != False:
        deskQueue.put(desk)
        style = ttk.Style()
        style.configure("deskfree.TLabel", background="gray", foreground='blue')
        desk.config(text= "masa görevde değil",style="deskfree.TLabel")
        barrier.release()

def rastgele_masaya_yerlestir(clientNo):
    global barrier
    e.wait()
    if e.is_set():
        if clientsId[clientNo][1]==0:
            waitBarrierTime = time.time() 
            barrier.acquire()
            getintoBarrierTime = time.time()
            timeout = getintoBarrierTime - waitBarrierTime
            print("timeout is here : ", timeout)
            if timeout > 20:
                print("this thread will be dead")
                writeToLog(f"Timeout : client {clientNo} : thread dead")
                barrier.release()
                return
            desk = deskQueue.get()
            style = ttk.Style()
            style.configure("deskfull.TLabel", background="green", foreground='blue')
            desk.config(text= f"masa görevde no : {clientNo}",style="deskfull.TLabel")
            writeToLog(f"{clientNo}. thread sitted to Desk")
            siparişVer(clientNo)
            deskQueue.put(desk)
            style = ttk.Style()
            style.configure("deskfree.TLabel", background="gray", foreground='blue')
            desk.config(text= "masa görevde değil",style="deskfree.TLabel")
            barrier.release()

def calistir(thread_id,desklabel):
    writeToLog("customer Created ID : " + str(thread_id))

    time.sleep(0.5)
    oncelikli_masaya_yerlestir(thread_id)
    rastgele_masaya_yerlestir(thread_id)


waiterC=0
chefC=0

def start(deskC, waiterCount, checkoutCount, chefCount,desklabels,waiterLabels, checkoutLabels, chefLabels):
        global barrier
        global deskCount
        global waiterC
        global chefC
        global checkoutC
        waiterC=waiterCount
        chefC=chefCount 
        checkoutC=checkoutCount

        deskCount = deskC

        barrier = threading.Semaphore(value=deskCount)

        for i in desklabels:
            deskQueue.put(i)

        for waiterIndex in range(int(waiterCount)):
            waiterThread = threading.Thread(target=waiterstart, args=([waiterLabels[waiterIndex]]))
            waiterThreads.append(waiterThread)
            waiterThread.start()
        writeToLog('{} waiter thread created \n'.format(waiterCount))

        for checkoutIndex in range(int(checkoutCount)):
            checoutThread = threading.Thread(target=checkoutstart, args=([checkoutLabels[checkoutIndex]]))
            checoutThreads.append(checoutThread)
            checoutThread.start()
        writeToLog('{} checout thread created \n'.format(checkoutCount))

        for chefIndex in range(int(chefCount)):
            chefThread = threading.Thread(target=chefstart, args=([chefLabels[chefIndex]]))
            chefThreads.append(chefThread)
            chefThread.start()
        writeToLog('{} chef thread created \n'.format(chefCount))

        for waiter in waiterThreads:
            waiter.join()

        for checoutThread in checoutThreads:
            checoutThread.join()

        for chefThread in chefThreads:
            chefThread.join()

def waiterstart(waiterLabels):
    global waiterSleep
    id = threading.get_ident()
    isEnd = False
    writeToLog(f"waiter {id} : Waiter Started and waiting for call")
    while not isEnd:
        """burada siparis almak için butonu beklemeli"""
        takeOrderSemaphore.wait()
        waiterSemaphore.signal()
        orderSemaphore.wait()
        data = orderqueue.get()
        writeToLog(f"waiter {id} : order tooked order given no : {data}")
        #
        style = ttk.Style()
        style.configure("waitertask.TLabel", background="green", foreground='blue')
        waiterLabels[1].config(text= f" {id} garson görevde müşteri no : {data}",style="waitertask.TLabel")

        #
        time.sleep(waiterSleep)
        sendOrderToChefSemaphore.wait()
        writeToLog(f"waiter {id} :  chef will be called after that")
        style.configure("waiterfree.TLabel", background="gray", foreground='blue')
        waiterLabels[1].config(text= "garson görevde değil",style="waiterfree.TLabel")
        #
        waiterQueue.put(data)
        writeToLog("chef calling")
        """chefe sipariş gönderme butonu"""
        chefWaiterSemaphore.signal()
        chefSemaphore.wait()
        writeToLog("here")

def checkoutstart(checkoutLabels):
    global checkoutSleep
    id = threading.get_ident()
    isEnd = False
    writeToLog(f"checkout {id} :  Started")
    while not isEnd:
        checkoutQueue.signal()
        checkoutcameQueue.wait()
        data = eatedMeals.get()
        writeToLog(f"checkout {id} : payment tooking client : {data}")
        style = ttk.Style()
        style.configure("checkoutTask.TLabel", background="green", foreground='blue')
        checkoutLabels[1].config(text= f" {id} kasa görevde müşteri no : {data}",style="checkoutTask.TLabel")
        time.sleep(checkoutSleep)
        checkoutDonequeue.put(data)
        writeToLog(f"checkout {id} : payment tooked client : {data}")
        style.configure("checoutfree.TLabel", background="gray", foreground='blue')
        checkoutLabels[1].config(text= "kasa görevde değil",style="checoutfree.TLabel")
        checkoutDone.signal()


"""
def chefstart(chefLabels):
    id=threading.get_ident()
    writeToLog(f"Chef {id} started and waiting for order") 
    while True:
        chefSemaphore.signal()
        chefWaiterSemaphore.wait()
        data= str(waiterQueue.get())
        print("chef tooked the order from waiter")

        writeToLog(f"chef {id}:tooked the order given no: {data}")
        #BURADA TUTUNCU OLACAK
        #HAZIRLAMAYA BAŞLA BUTONU BURADA ÇAĞIRILACAK
        style = ttk.Style()
        style.configure("cheforder.TLabel", background="orange", foreground='blue')
        chefLabels[1].config(text= "asci siparisi aldi",style="cheforder.TLabel")
        startCookSemaphore.wait()
        ########################################
        style.configure("cheftask.TLabel", background="green", foreground='blue')
        chefLabels[1].config(text= "asci görevde",style="cheftask.TLabel")
        time.sleep(5)
        writeToLog(f"chef {id}: order no {data} ready")
        style.configure("cheffree.TLabel", background="gray", foreground='blue')
        chefLabels[1].config(text= "aşçı görevde değil",style="cheffree.TLabel")
        orderTook.signal()
"""
furnanceCountM = threading.Semaphore()

def chefstart(chefLabels):
    id=threading.get_ident()
    writeToLog(f"Chef {id} started and waiting for order")
    taskList = []
    while True:
        if(len(taskList) == 0):
            style = ttk.Style()
            style.configure("cheffree.TLabel", background="gray", foreground='blue')
            chefLabels[1].config(text= "aşçı görevde değil",style="cheffree.TLabel")
        if(len(taskList) < 2):
            chefSemaphore.signal()
            style = ttk.Style()
            style.configure("cheffree.TLabel", background="gray", foreground='blue')
            chefLabels[1].config(text= "aşçı görevde değil",style="cheffree.TLabel")
            chefWaiterSemaphore.wait()
            #BURADA TUTUNCU OLACAK
            #HAZIRLAMAYA BAŞLA BUTONU BURADA ÇAĞIRILACAK
            style.configure("cheforder.TLabel", background="orange", foreground='blue')
            chefLabels[1].config(text= "asci siparisi aldi",style="cheforder.TLabel")
            startCookSemaphore.wait()
            ########################################
            style.configure("cheftask.TLabel", background="green", foreground='blue')
            chefLabels[1].config(text= f" {id} aşçı görevde",style="cheftask.TLabel")
            writeToLog(f"Chef {id} : activated furnance {len(taskList)} ")
            t=threading.Thread(target=cookmeal, args=(chefLabels,taskList, id,len(taskList)+3))
            taskList.append(t)
            t.start()
        elif(len(taskList) == 2):
            writeToLog(f"Chef {id} all furnances are full")
            time.sleep(1)

def cookmeal(chefLabels, taskList, id, index):
    global cookmealSleep
    data= str(waiterQueue.get())
    print("chef tooked the order from waiter")
    writeToLog(f"chef {id} , furnance {len(taskList)} : tooked the order given no: {data}")
    style = ttk.Style()
    style.configure("furnanceWorks.TLabel", background="green", foreground='blue')
    chefLabels[index].config(text= f"F {data}",style="furnanceWorks.TLabel")
    writeToLog(f"chef {id} , furnance {len(taskList)} : started to cook order {data}")
    time.sleep(cookmealSleep)
    writeToLog(f"chef {id} , furnance {len(taskList)} : order no {data} is ready")
    print("puttedData : ", data)

    style = ttk.Style()
    style.configure("furnanceFree.TLabel", background="gray", foreground='blue')
    chefLabels[index].config(text= f"F {data}",style="furnanceFree.TLabel")
    furnanceCountM.acquire()
    taskList.pop()
    furnanceCountM.release()
    writeToLog(f"chef {id} , furnance {len(taskList)} : closed")
    readymealsqueue.put(data)
    orderTook.signal()


#createcustomer(6,2)
#start(4,2,1,2)