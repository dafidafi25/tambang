
 
from __future__ import print_function 
from threading import Thread, Event 
from time import sleep 
import traceback 

from smartcard.Observer import Observer 
from smartcard.Observer import Observable 

from smartcard.CardRequest import CardRequest 

_START_ON_DEMAND_ = False

# CardObserver interface 
class CardObserver(Observer): 
    """ 
    CardObserver is a base abstract class for objects that are to be notified 
    upon smart card insertion / removal. 
    """ 
 
    def __init__(self): 
        pass 
 
    def update(self, observable, handlers): 
        """Called upon smart card insertion / removal. 
 
        @param observable: 
        @param handlers: 
          - addedcards: list of inserted smart cards causing notification 
          - removedcards: list of removed smart cards causing notification 
        """ 
        pass 
 
 
class CardMonitor(object): 
    """Class that monitors smart card insertion / removals. 
    and notify observers 
 
    note: a card monitoring thread will be running 
    as long as the card monitor has observers, or CardMonitor.stop() 
    is called. Do not forget to delete all your observers by 
    calling deleteObserver, or your program will run forever... 
 
    Uses the singleton pattern from Thinking in Python 
    Bruce Eckel, http://mindview.net/Books/TIPython to make sure 
    there is only one CardMonitor. 
    """ 
 
    class __CardMonitorSingleton(Observable): 
        """The real smart card monitor class. 
 
        A single instance of this class is created 
        by the public CardMonitor class. 
        """ 
 
        def __init__(self): 
            Observable.__init__(self) 
            if _START_ON_DEMAND_: 
                self.rmthread = None 
            else: 
                self.rmthread = CardMonitoringThread(self) 
 
        def addObserver(self, observer): 
            """Add an observer. 
 
            We only start the card monitoring thread when 
            there are observers. 
            """ 
            Observable.addObserver(self, observer) 
            if _START_ON_DEMAND_: 
                if self.countObservers() > 0 and self.rmthread == None: 
                    self.rmthread = CardMonitoringThread(self) 
            else: 
                observer.update(self, (self.rmthread.cards, [])) 
 
        def deleteObserver(self, observer): 
            """Remove an observer. 
 
            We delete the CardMonitoringThread reference when there 
            are no more observers. 
            """ 
            Observable.deleteObserver(self, observer) 
            if _START_ON_DEMAND_: 
                if self.countObservers() == 0: 
                    if self.rmthread != None: 
                        self.rmthread = None 
 
        def __str__(self): 
            return 'CardMonitor' 
 
    # the singleton 
    instance = None 
 
    def __init__(self): 
        if not CardMonitor.instance: 
            CardMonitor.instance = CardMonitor.__CardMonitorSingleton() 
 
    def __getattr__(self, name): 
        return getattr(self.instance, name) 
 
 
class CardMonitoringThread(object): 
    """Card insertion thread. 
    This thread waits for card insertion. 
    """ 
 
    class __CardMonitoringThreadSingleton(Thread): 
        """The real card monitoring thread class. 
 
        A single instance of this class is created 
        by the public CardMonitoringThread class. 
        """ 
 
        def __init__(self, observable): 
            Thread.__init__(self) 
            self.observable = observable 
            self.stopEvent = Event() 
            self.stopEvent.clear() 
            self.cards = [] 
            self.setDaemon(True) 
 
        # the actual monitoring thread 
        def run(self): 
            """Runs until stopEvent is notified, and notify 
            observers of all card insertion/removal. 
            """ 
            self.cardrequest = CardRequest(timeout=0.1) 
            while self.stopEvent.isSet() != 1: 
                try: 
                    currentcards = self.cardrequest.waitforcardevent() 
 
                    addedcards = [] 
                    for card in currentcards: 
                        if not self.cards.__contains__(card): 
                            addedcards.append(card) 
 
                    removedcards = [] 
                    for card in self.cards: 
                        if not currentcards.__contains__(card): 
                            removedcards.append(card) 
 
                    if addedcards != [] or removedcards != []: 
                        self.cards = currentcards 
                        self.observable.setChanged() 
                        self.observable.notifyObservers( 
                            (addedcards, removedcards)) 
 
                # when CardMonitoringThread.__del__() is invoked in 
                # response to shutdown, e.g., when execution of the 
                # program is done, other globals referenced by the 
                # __del__() method may already have been deleted. 
                # this causes ReaderMonitoringThread.run() to except 
                # with a TypeError or AttributeError 
                except TypeError: 
                    pass 
                except AttributeError: 
                    pass 
 
                except: 
                    # FIXME Tighten the exceptions caught by this block 
                    traceback.print_exc() 
                    # Most likely raised during interpreter shutdown due 
                    # to unclean exit which failed to remove all observers. 
                    # To solve this, we set the stop event and pass the 
                    # exception to let the thread finish gracefully. 
                    self.stopEvent.set() 
 
        # stop the thread by signaling stopEvent 
        def stop(self): 
            self.stopEvent.set() 
 
    # the singleton 
    instance = None 
 
    def __init__(self, observable): 
        if not CardMonitoringThread.instance: 
            CardMonitoringThread.instance = CardMonitoringThread.__CardMonitoringThreadSingleton(observable) 
            CardMonitoringThread.instance.start() 
 
    def __getattr__(self, name): 
        if self.instance: 
            return getattr(self.instance, name) 
 
    # commented to avoid bad clean-up sequence of python where __del__ 
    # is called when some objects it uses are already gargabe collected 
    #def __del__(self): 
    #    if CardMonitoringThread.instance!=None: 
    #        CardMonitoringThread.instance.stop() 
    #        CardMonitoringThread.instance = None 
 
 
if __name__ == "__main__": 
    print('insert or remove cards in the next 10 seconds') 
 
    # a simple card observer that prints added/removed cards 
    class printobserver(CardObserver): 
 
        def __init__(self, obsindex): 
            self.obsindex = obsindex 
 
        def update(self, observable, handlers): 
            addedcards, removedcards = handlers 
            print("%d - added:   %s" % (self.obsindex, str(addedcards))) 
            print("%d - removed: %s" % (self.obsindex, str(removedcards))) 
 
    class testthread(Thread): 
 
        def __init__(self, obsindex): 
            Thread.__init__(self) 
            self.readermonitor = CardMonitor() 
            self.obsindex = obsindex 
            self.observer = None 
 
        def run(self): 
            # create and register observer 
            self.observer = printobserver(self.obsindex) 
            self.readermonitor.addObserver(self.observer) 
            sleep(10) 
            self.readermonitor.deleteObserver(self.observer) 
 
    t1 = testthread(1) 
    t1.start() 