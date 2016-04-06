import threading
import queue
import time

mq = queue.Queue(maxsize=-1)

class Mythread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        time.sleep(5)
        mq.put('5')
        print('put')

mq.put('sd')
t = Mythread()
t.start()
print(mq.get())
print('waite put')
print(mq.get())