import datetime
import time
import threading
startingtime = time.perf_counter() #returns time in sec
endtime = time.perf_counter()+180
print(startingtime)
print(endtime)
print(endtime-startingtime)
def fun():
    print("Hey you called me")

startingtime = threading.Timer(5, fun)
startingtime.start()
print("end")    
