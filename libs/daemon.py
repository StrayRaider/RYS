import threading
import time
import random
import queue

# Dosyaya yazma işlemleri atomik olmazsa açma okuma ve yazma işlemleri çakışacaktır
# O yüzden dosyayı açıp ekleme yapma işlemleri atomik olmalı ve bir thread yazma işini bitirip kapatmadan diğeri açmamalı

orderqueue = queue.LifoQueue()

waiterThreads = []
checoutThreads = []
chefThreads = []
clientThreads=[]

clientCount=10
primaryClientCount=2
deskCount=6

"""bariyer 6 kişi gelene kadar bekler"""
clientsId = [[0 for x in range(2)] for y in range(clientCount)]

barrier = threading.Semaphore(value=deskCount)
barrier2=threading.Semaphore(value=deskCount-primaryClientCount)

e= threading.Event()
semaphore= threading.Semaphore()

customercount=0

def createcustomer(clientCount, primaryClientCount):
    global customercount
    customercount = 0
    for id in range(clientCount-primaryClientCount):#8 kez dönecek(8 tane thread oluşacak)
        clientsId[id][0]=id

    for id in range(primaryClientCount):#2 tane öncelikli thread oluşuyor
        clientsId[id+clientCount-primaryClientCount][0]=id+clientCount-primaryClientCount
        clientsId[id+clientCount-primaryClientCount][1]=1,

createcustomer(6,2)

def oncelikli_masaya_yerlestir(clientNo):
    global barrier
    global customercount

    if clientsId[clientNo][1]!=0:
        barrier.acquire()
        # print("here")
        print(f"{clientNo}. thread yerlestirildi   öncelikli")

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
            time.sleep(1)



def calistir(thread_id):
    oncelikli_masaya_yerlestir(thread_id)
    rastgele_masaya_yerlestir(thread_id)

for clientId in range(len(clientsId)):
    t=threading.Thread(target=calistir, args=(clientsId[clientId][0],))
    t.start()
    clientThreads.append(t)
    time.sleep(0.1)


def start(deskC, waiterCount, checkoutCount, chefCount):
        global deskCount
        deskCount = deskC

        with open('log.txt', 'w') as f:
            f.write("Daemon Started \n")
            f.close()


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

writeLogMutex = threading.Semaphore()

def writeToLog(textToWrite):
    global writeLogMutex

    writeLogMutex.acquire()
    with open('log.txt', 'a') as f:
        f.write('{} \n'.format(textToWrite))
        f.close()
    writeLogMutex.release()

callwaiterEvent = threading.Event()
sMutex =  threading.Semaphore()
def customerstart(id):
    print("waiter callling")
    writeToLog("Waiter calling")
    callwaiterEvent.set()
    orderqueue.put("sipariş koyuldu -{}-".format(threading.get_ident()))


def waiterstart(id):
    print("waiter started")
    writeToLog("Waiter Started and waiting for call")
    sMutex.acquire()
    callwaiterEvent.wait()
    callwaiterEvent.clear()
    sMutex.release()
    data = orderqueue.get()
    writeToLog("order tooked : {}".format(data))

    writeToLog("Waiter called")
    print(waiterThreads[0].ident)

def checkoutstart(id):
    writeToLog("Checkout Started")

def chefstart(id):
    writeToLog("Chef Started")

#start(2,2,2,2)