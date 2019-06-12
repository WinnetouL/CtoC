import sys
import time
import threading
import _thread



class test:

    def main(self):
        print("moin")
        t0 = threading.Thread(target = self.first)
        t1 = threading.Thread(target = self.second)
        # t0.daemon = True
        # t1.daemon = True
        # t0.start()
        # t1.start()

        while True:
            a = threading.enumerate()
            b = threading.active_count()
            print("which: ", a)
            print("amount: ", b)
            print("t0 alive ", t0.is_alive())
            print("t1 alive ", t1.is_alive())
            # # print("t0 alive ", MainThread.is_alive)
            time.sleep(1)
            # print("tag")
            if t0.is_alive() == False:
                print("whileLoop t0 alive ", t0.is_alive())
                # time.sleep(5)
                t0 = threading.Thread(target = self.first)
                t0.daemon = True
                t0.start()

            elif t1.is_alive() == False:
                print("WWWWWWWWWWWWWWWWwhileLoop t1 alive ", t1.is_alive())
                t1 = threading.Thread(target = self.second)
                t1.daemon = True
                t1.start()
            else:
                pass


    def first(self):
        # while True:
        print("first running\n")
        time.sleep(5)
        print("first bye")
        # _thread.exit()
        # threading._thread.exit_thread()
        sys.exit(0)


    def second(self):
        while True:
            print("second running\n")
            time.sleep(5)



testOb = test()
testOb.main()







'''
import sys
import time
import threading


class test:

    def main(self):
        t0 = threading.Thread(target = self.first)
        t1 = threading.Thread(target = self.second)

        while True:

            if t0.is_alive() == False:
                print("whileLoop t0 alive ", t0.is_alive())
                time.sleep(5)
                t0.daemon = True
                t0.start()

            elif t1.is_alive() == False:
                print("whileLoop t1 alive ", t1.is_alive())
                t1.daemon = True
                t1.start()

            else:
                a = threading.enumerate()
                b = threading.active_count()
                print("which: ", a)
                print("amount: ", b)
                print("t0 alive ", t0.is_alive())
                print("t1 alive ", t1.is_alive())
                # print("t0 alive ", MainThread.is_alive)
                time.sleep(1)


    def first(self):
        # while True:
        print("first running\n")
        time.sleep(5)
        print("first bye\n")
            # sys.exit(0)


    def second(self):
        while True:
            print("second running\n")
            time.sleep(5)



testOb = test()
testOb.main()






























import sys
import time
import threading


class test:

    def main(self):
        t0 = threading.Thread(target = self.first)
        t1 = threading.Thread(target = self.second)


        b = threading.active_count()

        while True:

            if t0.is_alive() == False:
                print("whileLoop t0 alive ", t0.is_alive())
                t0.daemon = True
                t0.start()

            elif t1.is_alive() == False:
                print("whileLoop t1 alive ", t1.is_alive())
                t1.daemon = True
                t1.start()

            else:
                a = threading.enumerate()
                b = threading.active_count()
                print("which: ", a)
                print("amount: ", b)
                print("t0 alive ", t0.is_alive())
                print("t1 alive ", t1.is_alive())
                # print("t0 alive ", MainThread.is_alive)
                time.sleep(1)


    def first(self):
        while True:
            print("first running\n")
            time.sleep(5)
            print("first running\n")
            sys.exit(0)


    def second(self):
        while True:
            print("second running\n")
            time.sleep(5)



testOb = test()
testOb.main()
'''
