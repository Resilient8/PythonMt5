import MetaTrader5 as mt5
import pandas as pd
import os
import time
from myclass import Bot
from threading import Thread


os.chdir(r"C:\Users\ASUS\495\grid_strategy")
key = open("key.txt","r").read().split()
path = r"C:\Program Files\MetaTrader 5 IC Markets Global\terminal64.exe"
# establish MetaTrader 5 connection to a specified trading account
if mt5.initialize(path=path,login=int(key[0]), password=key[1], server=key[2]):
 print("ICMarkets connection established")

time.sleep(2)
#---------------------------------------------------------------------------------
bot1 = Bot(25,"EURUSD",0.01,2,1)
bot2 = Bot(5,"GBPUSD",0.01,2,1)
bot3 = Bot(3,"USDCAD",0.01,2,1)
def b1():
 bot1.run()
def b2():
 bot2.run()
def b3():
 bot3.run()

thread1 = Thread(target=b1)
thread2 = Thread(target=b2)
thread3 = Thread(target=b3)

thread1.start()
thread2.start()
thread3.start()