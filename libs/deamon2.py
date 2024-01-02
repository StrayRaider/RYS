"""
Sabit akı¸s modeli: Toplam s¨ure, m¨u¸steri gelme aralı˘gı uygulamada belirlen-
melidir.
∗ ¨Ornek: Her 5 saniyede 4 m¨u¸steri gelmektedir ve 1’i ¨oncelikli olmaktadır.
3 dakikalık s¨urede gelecek m¨u¸steriye g¨ore restoranın maksimum kapasitesi
hesaplanır (masa, garson, a¸s¸cı)."""

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
with open('log2.txt', 'w') as f:
    f.write("Daemon Started \n")
    f.close()

writeLogMutex = threading.Semaphore()

def writeToLog(textToWrite):
    global writeLogMutex

    writeLogMutex.acquire()
    with open('log2.txt', 'a') as f:
        f.write('{} \n'.format(textToWrite))
        f.close()
    writeLogMutex.release()

sMutex =  threading.Semaphore()


orderqueue = queue.Queue()
waiterQueue = queue.Queue()

waiterThreads = []
checoutThreads = []
chefThreads = []
clientThreads=[]

waiterSemaphore = ModifiedSemaphore(0)
orderSemaphore = ModifiedSemaphore(0)

checkoutcameQueue = ModifiedSemaphore(0)
checkoutQueue = ModifiedSemaphore(0)

orderTook = ModifiedSemaphore(0)

chefSemaphore = ModifiedSemaphore(0)
chefWaiterSemaphore = ModifiedSemaphore(0)

clientCount=10
primaryClientCount=2
deskCount=6

"""bariyer 6 kişi gelene kadar bekler"""

barrier = None
e= threading.Event()
semaphore= threading.Semaphore()

customercount=0
deskQueue = queue.Queue()

clients = {}

# toplam zaman, gelme aralığı 2 intager data
def stabilFlow(totalTime, arriveinterval, clientC, primaryClientCount):
    #ayrı bir threadde çalışmalı, yeni threadler oluşturacak
    is_end = False
    passedTime = 0
    while not is_end:
        passedTime += arriveinterval
        createcustomer(clientC, primaryClientCount)
        time.sleep(arriveinterval)
        if(totalTime <= passedTime):
            is_end = True
            break

def createcustomer(clientC, primaryClientCount):
    global customercount, clientsId, clientCount
    e.clear()
    customercount = 0
    clientCount = clientC

    for clientId in range(clientC):
        t=threading.Thread(target=calistir, args=())
        t.start()
        if(clientId < primaryClientCount):
            clients[f"{t.ident}"] = 1
            print(str(t.ident)+"appended as 1")
        else:
            clients[f"{t.ident}"] = 0
            print(str(t.ident)+"appended as 0")
        clientThreads.append(t)
        time.sleep(0.1)
    print(clients)

def calistir():
    thread_id = threading.get_ident()
    #writeToLog("customer Created ID : " + str(thread_id) + "primer : " + clients[f"{threading.get_ident()}"])

    time.sleep(0.5)


stabilFlow(5,1,4,2)
