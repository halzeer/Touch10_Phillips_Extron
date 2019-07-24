'''
This Modules supports Ethernet and Serial Connection status (Logical/Physical)
Also handles the .Connect for Ethernet.

Ver: 1.0
'''
from extronlib.system import Wait

class LogicalConnection:
    # This class takes: Device Obj, CallBack, Reconnect Frequency, Label Obj
    def __init__(self, ModuleObj, CallBackMethod, ReconnectTimer=5, Label=None):
        self.StoredWait = None
        self.Module = ModuleObj
        self.ConnectionStatusLbl = Label
        self.ReconnectTimer = ReconnectTimer
        self.CallBackMethod = CallBackMethod
        self.LogicalMessage = ''
        self.PhysicalMessage = ''
        self.Module.SubscribeStatus('ConnectionStatus',None,self.ModuleStatus)
        if self.Module.ConnectionType == 'Ethernet':
            self.DoConnect()
    
    def UpdateConnectionStatus(self):
        '''
        Calls the CallbackMethod and Updates Label when required
        '''
        value = '{0} {1}'.format(self.LogicalMessage, self.PhysicalMessage)
        self.CallBackMethod(value)
        # if Label exist, Update Label
        if self.ConnectionStatusLbl:
            self.ConnectionStatusLbl.SetText(value)
        
    def ModuleStatus(self, command, value, qualifier):        
        if value == 'Connected':
            self.LogicalMessage = 'Logical:Connected'
            if self.StoredWait:
                self.StoredWait.Cancel()
        else:
            self.LogicalMessage = 'Logical:Disconnected'
            self.Module.Disconnect()
            self.Module.OnDisconnected()
            # Only for Ethernet Communication
            if self.Module.ConnectionType == 'Ethernet':
                if not self.StoredWait:
                    self.StoredWait = Wait(self.ReconnectTimer, self.DoConnect)
                else:
                    self.StoredWait.Restart()
        # When Logical Connections status changes from Extron Module
        self.UpdateConnectionStatus()
                
    def DoConnect(self):
        result = self.Module.Connect(self.ReconnectTimer)
        if result == 'Connected':
            self.PhysicalMessage = 'Physical:Connected'
        elif result == 'TimedOut':
            self.LogicalMessage = 'Logical:Disconnected'
            self.PhysicalMessage = 'Physical:Reconnecting'
        elif result == 'HostError':
            self.LogicalMessage = 'Logical:Disconnected'
            self.PhysicalMessage = 'Physical:Reconnecting'
        self.UpdateConnectionStatus()
        if self.StoredWait:
            self.StoredWait.Restart()