from extronlib.device import ProcessorDevice, UIDevice
from extronlib import event, Version
from extronlib.interface import EthernetClientInterface, SerialInterface
from extronlib.ui import Button, Label, Level
from extronlib.system import Clock, MESet, Wait

from csco_vtc_Touch_10_v1_1_6_1 import SerialClass, SSHClass
from LogicalConnectionHandler import LogicalConnection
from PollingEngine import PollingEngine
from PhilipsEnvision_Manager_v_1_0 import EnvisionManager_https
Processor = ProcessorDevice('ProcessorAlias')

#dvInterface = SerialClass(Processor, 'COM1', Baud=115200, Model='Touch 10 Custom')
dvInterface = SSHClass('10.113.110.177', Credentials=('extron', 'cisco123'), Model='Touch 10 Custom')
dvInterface.deviceUsername = 'extron'
dvInterface.devicePassword = 'cisco123'
dvLights = EnvisionManager_https('philips2.mea.cisco-demos.com')

currentLevel_linear = 0
currentLevel_down = 0
currentLevel_cove1 = 0
currentLevel_cove2 = 0
areaID = 1002
Scale_Factor = 2.55
Widget_lists = [
                 None,
                'widget_1',
                'widget_2',
                'widget_3',
                'widget_4',
                'widget_5',
                'widget_6',
                'widget_7',
                'widget_8',
                ]

def ConnectionStatusState(value):    
    if 'Logical:Connected' in value:
        @Wait(2)
        def resyncPanel():
            dvInterface.Set('Button','Inactive', {'Widget ID' : 'widget_1'})
            dvInterface.Set('Button','Inactive', {'Widget ID' : 'widget_2'})
            dvInterface.Set('Button','Inactive', {'Widget ID' : 'widget_3'})
            dvInterface.Set('Button','Inactive', {'Widget ID' : 'widget_4'})
            dvInterface.Set('Button','Inactive', {'Widget ID' : 'widget_5'})
            dvInterface.Set('Button','Inactive', {'Widget ID' : 'widget_6'})
            dvInterface.Set('Button','Inactive', {'Widget ID' : 'widget_7'})
            dvInterface.Set('Button','Inactive', {'Widget ID' : 'widget_8'})
            dvInterface.Set('Button','Inactive', {'Widget ID' : 'widget_11'})
            dvInterface.Set('Slider',currentLevel_linear, {'Widget ID' : 'widget_20'})
            dvInterface.Set('Slider',currentLevel_down, {'Widget ID' : 'widget_21'})
            dvInterface.Set('Slider',currentLevel_cove1, {'Widget ID' : 'widget_22'})
            dvInterface.Set('Slider',currentLevel_cove2, {'Widget ID' : 'widget_23'})

#Connection Handler Engine  
connectStatus = LogicalConnection(dvInterface, ConnectionStatusState, 5)

#Polling Engine            
CiscoTouch10 = PollingEngine(dvInterface, [{'Update': 'FirmwareVersion', 'Qualifier': None}])


def initialize():
    print('system started')
    CiscoTouch10.start()

def GetFirmwareCheck(command, value, qualifier):
    print(value)
def applyWidgetState(WidgetID=None):
        #dvInterface.Set('Button','Inactive', {'Widget ID' : 'widget_1'})
        #dvInterface.Set('Button','Inactive', {'Widget ID' : 'widget_2'})
        #dvInterface.Set('Button','Inactive', {'Widget ID' : 'widget_3'})
        #dvInterface.Set('Button','Inactive', {'Widget ID' : 'widget_4'})
        #dvInterface.Set('Button','Inactive', {'Widget ID' : 'widget_5'})
        #dvInterface.Set('Button','Inactive', {'Widget ID' : 'widget_6'})
        #dvInterface.Set('Button','Inactive', {'Widget ID' : 'widget_7'})
        #dvInterface.Set('Button','Inactive', {'Widget ID' : 'widget_8'})
        #dvInterface.Set('Button','Inactive', {'Widget ID' : 'widget_11'})
        for widget in Widget_lists:
            dvInterface.Set('Button','Inactive', {'Widget ID' : widget})
        if WidgetID is not None:
            dvInterface.Set('Button','Active', {'Widget ID' : WidgetID})
        @Wait(1)
        def updateactivewidget():
            currentStatus = dvLights.getCurrentStatus(areaID)
            active_widget = 'widget_{}'.format(currentStatus['areaLevel'])
            if WidgetID is None:
                dvInterface.Set('Button','Active', {'Widget ID' : active_widget})
            for i in range (0,4):
                level = currentStatus['luminaireLevels'][i]['luminaireLevel']
                level = int(level) * Scale_Factor
                Widget_ID = 'widget_2{}'.format(i)
                dvInterface.Set('Slider',level, {'Widget ID' : Widget_ID})
                
                
def GetButtonEvent(command, value, qualifier):
    Selected_widget = qualifier['Widget ID']
    if Selected_widget in Widget_lists:
        areaLevel = Widget_lists.index(Selected_widget)
        lights_fb = dvLights.applyAreaLevel(areaID,areaLevel)
        if lights_fb:
            applyWidgetState(Selected_widget)
    else:
        print('not a valid widget ID')

def GetSlider(command, value, qualifier):
    value = int(value)/Scale_Factor
    if qualifier['Widget ID'] == 'widget_20':
        dvLights.applyLuminaireLevel(areaID,1,int(value))
    elif qualifier['Widget ID'] == 'widget_21':
        dvLights.applyLuminaireLevel(areaID,2,int(value))
    elif qualifier['Widget ID'] == 'widget_22':
        dvLights.applyLuminaireLevel(areaID,3,int(value))
    elif qualifier['Widget ID'] == 'widget_23':
        dvLights.applyLuminaireLevel(areaID,4,int(value))

def GetPageEvent(command, value, qualifier):
    print(command, value, qualifier)

def GetPanelEvent(command, value, qualifier):
    applyWidgetState()


dvInterface.SubscribeStatus('FirmwareVersion', None, GetFirmwareCheck)
dvInterface.SubscribeStatus('ButtonEvent', None, GetButtonEvent)
dvInterface.SubscribeStatus('PageEvent', None, GetPageEvent)
dvInterface.SubscribeStatus('PanelEvent', None, GetPanelEvent)
dvInterface.SubscribeStatus('Slider', None, GetSlider)
###Lighting control Scripts goes here





initialize()


