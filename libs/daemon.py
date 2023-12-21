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

def start(deskCount, waiterCount, checkoutCount, chefCount):
        with open('log.txt', 'w') as f:
            f.write("Daemon Started \n")
            f.close()

        daemonId = threading.get_ident()

        for waiterIndex in range(int(waiterCount)):
            daemonId += 1
            waiterThread = threading.Thread(target=waiterstart, args=(threading.get_ident(),))
            waiterThreads.append([waiterThread,daemonId])
            waiterThread.start()
        writeToLog('{} waiter thread created \n'.format(waiterCount))

        for checkoutIndex in range(int(checkoutCount)):
            daemonId += 1
            checoutThread = threading.Thread(target=checkoutstart, args=(threading.get_ident(),))
            checoutThreads.append([checoutThread,daemonId])
            checoutThread.start()
        writeToLog('{} checout thread created \n'.format(checkoutCount))

        for chefIndex in range(int(chefCount)):
            daemonId += 1
            chefThread = threading.Thread(target=chefstart, args=(threading.get_ident(),))
            chefThreads.append([chefThread,daemonId])
            chefThread.start()
        writeToLog('{} chef thread created \n'.format(chefCount))

        customerThread1 = threading.Thread(target=customerstart, args=(threading.get_ident(),))
        customerThread1.start()
        customerThread = threading.Thread(target=customerstart, args=(threading.get_ident(),))
        customerThread.start()

        for waiter in waiterThreads:
            waiter[0].join()

        for checoutThread in checoutThreads:
            checoutThread[0].join()

        for chefThread in chefThreads:
            chefThread[0].join()

        customerThread.join()
        customerThread1.join()

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

def checkoutstart(id):
    writeToLog("Checkout Started")

def chefstart(id):
    writeToLog("Chef Started")

#start(2,2,2,2)