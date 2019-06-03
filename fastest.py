import sys
import threading 
import time 





class test:

    stop_threads = False
        

    def run(self): 
        
        try:
            while True:
                print('thread running') 
                a = threading.active_count()
                print("nr", a) 
                time.sleep(1)
                # input("w")
                testob.stop_threads = True
                print("this,", testob.stop_threads)
        except KeyboardInterrupt as e:
            print("MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM")

    def main(self): 
            testob.stop_threads = False
            t1 = threading.Thread(target = self.run) 
            t1.daemon = True
            t1.start()

            while True:
                if testob.stop_threads == True:
                    # time.sleep(5)
                    testob.stop_threads = True
                    print("Done")
                    sys.exit(0)
                elif testob.stop_threads == False:
                    print("ey nobody can tell me nothing")
                    print(testob.stop_threads)
                    time.sleep(1)

            # time.sleep(1) 
            # t1.join() 
            # print('thread killed') 

testob = test()
testob.main() 






'''
import sys
import threading
import time
def do_something_with_exception():
    # exc_type, exc_value = sys.exc_info()[:2]
    #print("HHHHHHHHHHHHHHHHHHHHHHHandling {} exception with message '{}' in {}").format(exc_type.__name__, exc_value, threading.current_thread().name)
    print("HHHHHHHHHHHHHHHHHHHHHHHHHHHHHH")

def cause_exception(delay):
    print("started")
    time.sleep(delay)
    # raise RuntimeError('This is the error message')
    print("finished")
    main(False)
    # q = False
    # return q

def main(q):

            
    t1 = threading.Thread(target= cause_exception, args=(3, ))
    t2 = threading.Thread(target= cause_exception, args=(1, ))
    t1.daemon = True
    t2.daemon = True
    t1.start()
    t2.start()
    
    while True:
        if q == False:
            print("q = False, so bye!")
            a = threading.active_count()
            print("alive", a)
            sys.exit(0)
        else:
            a = threading.active_count()
            print(a)
            time.sleep(1)
            break
    # q = True



main(True)
'''























# import threading
# import time


# class test:
        
#     def run(self):
#         while True:
#             print('run')
#             time.sleep(1)

#     def fun(self):
#         # while True:
#             print("fun2")
#             time.sleep(2)

#     def main(self):
#         t0 = threading.Thread(target = self.run)
#         t1 = threading.Thread(target = self.fun)
#         t0.daemon = True
#         t1.daemon = True
#         t0.start()
#         t1.start()
#         threading.Thread._exc_info

#         while True:
#             a = threading.active_count()
#             # b = threading.enumerate()
#             print(a)
#             # print(b)
#             time.sleep(2)



# testOb = test()
# testOb.main()




































'''
import sys
import threading
import time

def do_something_with_exception():
    # exc_type, exc_value = sys.exc_info()[:2]
    #print("HHHHHHHHHHHHHHHHHHHHHHHandling {} exception with message '{}' in {}").format(exc_type.__name__, exc_value, threading.current_thread().name)
    print("HHHHHHHHHHHHHHHHHHHHHHHHHHHHHH")

def cause_exception(delay):
    time.sleep(delay)
    raise RuntimeError('This is the error message')
    # print("namoin")

def thread_target(delay):
    try:
        cause_exception(delay)
    except:
        do_something_with_exception()

threads = [threading.Thread(target=thread_target, args=(0.3,)), threading.Thread(target=thread_target, args=(0.1,)),]

for t in threads:
    t.start()
for t in threads:
    t.join()


'''