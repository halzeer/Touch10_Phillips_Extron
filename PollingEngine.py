"""
Handles polling through a list of statuses for a module
v1.1
"""
from extronlib.system import Wait

# To be used with modules
class PollingEngine:
    
    def __init__(self, deviceObject, queryList=[], interval=1):
    
        # Device object. Instance of SerialClass or EthernetClass from modules
        self._deviceObject = deviceObject
        
        # List of queries
        self._queryList = queryList
        
        # time between each query
        self.interval = float(interval)
                
        # store global Wait object
        self._pollingWait = None
        
        # initial start index
        self.index = 0
            
    
    def _polling_sequence(self):
        if self._pollingWait and len(self._queryList):
        
            # reset index if it is at max
            if self.index >= len(self._queryList):
                self.index = 0
            
            query = self._queryList[self.index]
            self._deviceObject.Update(query['Update'], query['Qualifier'])
            self.index += 1
            
            # if current timer's time is different from self.interval,
            # create new timer with self.interval time
            if self._pollingWait.Time != self.interval:
                self.stop()
                self.start()
            else:
                self._pollingWait.Restart()
            
            
    
    def add_query(self, query):
        # Check to make sure query argument has valid keys and is a dictionary
        if isinstance(query, dict):
            if query.__contains__('Update') and query.__contains__('Qualifier'):
                # Help avoid raise conditions (possibly)
                if self._pollingWait:
                    self.stop()
                    self._queryList.append(query)
                    self.start()
                else:
                    self._queryList.append(query)
            else:
                raise KeyError('query dictionary does not have Update and Qualifier keys')
        else:
            raise TypeError('query argument is not a dictionary')
            
    def remove_query(self, query):
        # Check to make sure query argument has valid keys and is a dictionary
        if isinstance(query, dict):
            if query.__contains__('Update') and query.__contains__('Qualifier'):
                # Help avoid race conditions (possibly)
                if self._pollingWait:
                    self.stop()
                    self._queryList.remove(query)
                    self.start()
                else:
                    self._queryList.remove(query)
            else:
                raise KeyError('query dictionary does not have Update and Qualifier keys')
        else:
            raise TypeError('query argument is not a dictionary')
                
    def start(self):
        # Create Wait object to call polling_sequence
        if not self._pollingWait:
            self._pollingWait = Wait(self.interval, self._polling_sequence)
        else:
            self._pollingWait.Restart()
        
    def stop(self):
        if self._pollingWait:
            self._pollingWait.Cancel()
            self._pollingWait = None
        
    def delay(self, time):
        # stop current timer and create a new one with new time
        self.stop()
        self._pollingWait = Wait(time, self._polling_sequence)