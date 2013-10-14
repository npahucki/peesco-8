import Queue
import threading

class Pololu:
    
    def __init__(self, serial):
         self.__ser=serial 
         self.__q = Queue.Queue()
         t = threading.Thread(target=self.__worker)
         t.daemon = True
         t.start()
    
    def send_cmd(self, cmd):
        self.__q.put_nowait(cmd)
    
    def __worker(self):
        while True:
            cmd = self.__q.get()
            self.__ser.write(cmd)
            print [ord(c) for c in cmd]
            self.__q.task_done()
    
    def wait_done(self):
        self.__q.join()
                
    	
    	
    
         