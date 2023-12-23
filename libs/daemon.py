import threading
import time
import random
import queue

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

waiterThreads = []
checoutThreads = []
chefThreads = []
clientThreads=[]

waiterQueue = ModifiedSemaphore(0)
orderQueue = ModifiedSemaphore(0)

clientCount=10
primaryClientCount=2
deskCount=6

"""bariyer 6 kişi gelene kadar bekler"""
clientsId = [[0 for x in range(2)] for y in range(clientCount)]

barrier = None
e= threading.Event()
semaphore= threading.Semaphore()

customercount=0

def createcustomer(clientC, primaryClientCount):
    global customercount, clientsId, clientCount
    customercount = 0
    clientCount = clientC

    clientsId = [[0 for x in range(2)] for y in range(clientCount)]
    for id in range(clientCount-primaryClientCount):#8 kez dönecek(8 tane thread oluşacak)
        clientsId[id][0]=id

    for id in range(primaryClientCount):#2 tane öncelikli thread oluşuyor
        clientsId[id+clientCount-primaryClientCount][0]=id+clientCount-primaryClientCount
        clientsId[id+clientCount-primaryClientCount][1]=1,

    for clientId in range(len(clientsId)):
        t=threading.Thread(target=calistir, args=(clientsId[clientId][0],))
        t.start()
        clientThreads.append(t)
        time.sleep(0.1)

def siparişVer(clientNo):
    print("waiter callling")
    writeToLog("Waiter calling")
    orderQueue.signal()
    waiterQueue.wait()
    orderqueue.put("order created -{}-".format(clientNo))
    writeToLog("order created in queue-{}-".format(clientNo))

def customerDie(clientNo):
    writeToLog(f"{clientNo}. thread Leaving")
    barrier.release()

def oncelikli_masaya_yerlestir(clientNo):
    global barrier
    global customercount

    if clientsId[clientNo][1]!=0:
        barrier.acquire()
        writeToLog(f"{clientNo}. thread sitted to Desk Primer")
        print(f"{clientNo}. thread yerlestirildi   öncelikli")
        siparişVer(clientNo)
        customerDie(clientNo)

    semaphore.acquire()
    customercount+=1
    if customercount==clientCount:#9+1==10 
        # print("e setted",clientCount)
        e.set()
    
    semaphore.release()

def rastgele_masaya_yerlestir(clientNo):
    global barrier
    e.wait()
    if e.is_set():
        if clientsId[clientNo][1]==0:
            barrier.acquire()
            print(f"{clientNo}. thread yerlestirildi")
            writeToLog(f"{clientNo}. thread sitted to Desk")

            siparişVer(clientNo)
            customerDie(clientNo)

def calistir(thread_id):
    writeToLog("customer Created ID : " + str(thread_id))
    time.sleep(0.5)
    oncelikli_masaya_yerlestir(thread_id)
    rastgele_masaya_yerlestir(thread_id)

def start(deskC, waiterCount, checkoutCount, chefCount):
        global barrier
        global deskCount
        deskCount = deskC

        barrier = threading.Semaphore(value=deskCount)

        for waiterIndex in range(int(waiterCount)):
            waiterThread = threading.Thread(target=waiterstart, args=(threading.get_ident(),))
            waiterThreads.append(waiterThread)
            waiterThread.start()
        writeToLog('{} waiter thread created \n'.format(waiterCount))

        for checkoutIndex in range(int(checkoutCount)):
            checoutThread = threading.Thread(target=checkoutstart, args=(threading.get_ident(),))
            checoutThreads.append(checoutThread)
            checoutThread.start()
        writeToLog('{} checout thread created \n'.format(checkoutCount))

        for chefIndex in range(int(chefCount)):
            chefThread = threading.Thread(target=chefstart, args=(threading.get_ident(),))
            chefThreads.append(chefThread)
            chefThread.start()
        writeToLog('{} chef thread created \n'.format(chefCount))

        for waiter in waiterThreads:
            waiter.join()

        for checoutThread in checoutThreads:
            checoutThread.join()

        for chefThread in chefThreads:
            chefThread.join()


def waiterstart(id):
    isEnd = False
    print("waiter started")
    writeToLog("Waiter Started and waiting for call")
    while not isEnd:
        waiterQueue.signal()
        orderQueue.wait()
        data = str(orderqueue.get()).split("-")[1]
        writeToLog("order tooked  order given no : {}".format(data))
        print(waiterThreads[0].ident)
        writeToLog("chef will be called after that")

def checkoutstart(id):
    writeToLog("Checkout Started")

def chefstart(id):
    writeToLog("Chef Started")

#createcustomer(6,2)
#start(2,2,2,2)