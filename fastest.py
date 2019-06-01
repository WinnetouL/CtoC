# https://docs.python.org/3/library/threading.html#threading.Thread.join

import threading
import time


class test:
        
    def run(self):
        while True:
            print('run')
            time.sleep(1)

    def fun(self):
        while True:
            print("fun2")
            time.sleep(2)

    def main(self):
        t0 = threading.Thread(target = self.run)
        t1 = threading.Thread(target = self.fun)
        # t0.daemon = True
        # t1.daemon = True
        t0.start()
        t1.start()

        while True:
            a = threading.active_count()
            # b = threading.enumerate()
            print(a)
            # print(b)
            time.sleep(2)



testOb = test()
testOb.main()







# class ThreadingExample(object):
#     """ Threading example class
#     The run() method will be started and it will run in the background
#     until the application exits.
#     """

#     def __init__(self, interval=1):
#         """ Constructor
#         :type interval: int
#         :param interval: Check interval, in seconds
#         """
#         self.interval = interval

#         thread = threading.Thread(target=self.run, args=())
#         print("aaa")
#         thread.daemon = True                            # Daemonize thread
#         thread.start()                                  # Start the execution

#     def run(self):
#         """ Method that runs forever """
#         while True:
#             # Do something
#             print('Doing something imporant in the background')

#             time.sleep(self.interval)

# example = ThreadingExample()
# time.sleep(3)
# print('Checkpoint')
# while True:
#     time.sleep(2)
#     print('Bye')
        # a = threading.active_count()
        # b = threading.enumerate()
        # print(a)
        # print(b)

# if __name__ == "__main__":











# join()?
# lock?







# f = open("asyncio.txt", "w+")


# def func2(lul):
#     while True:
#         print('Echo', lul)
#         time.sleep(3)





































'''
from time import sleep
import multiprocessing
import io

f = open("asyncio.txt", "w+")


def blocking(to):
    print("ECHO:", to)
    # while True:
    #     
    #     print("ECHO: ", a)


def writingToFile():
    while True:
        f.write("This is Spandau\n")
        sleep(1)


def main():
    p2 = multiprocessing.Process(target = writingToFile)
    p2.start()
    while True:
        a = input("something? ")
        p1 = multiprocessing.Process(target = blocking(a))
        p1.start()


if __name__ == '__main__':
    main()
    print('last line')

'''