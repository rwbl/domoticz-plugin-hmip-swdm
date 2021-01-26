# Domoticz Home Automation - homematicIP Window and Door Contact with Magnet (HMIP-SWDM)
# Get the state open|closed of the contact.
# Dependencies:
# RaspberryMatic XML-API CCU Addon (https://github.com/hobbyquaker/XML-API)
# Library ElementTree (https://docs.python.org/3/library/xml.etree.elementtree.html#)
# Notes:
# 1. After every change: delete the hardware using the plugin homematicIP Thermostat
# 2. After every change: restart domoticz by running from terminal the command: sudo service domoticz.sh restart
# 3. Domoticz Python Plugin Development Documentation (https://www.domoticz.com/wiki/Developing_a_Python_plugin)
# 4. Only two adevice attributes are used. The plugin is flexible to add more attributes as required (examples LOW_BAT)
#
# Author: Robert W.B. Linn
# Version: See plugin xml definition

"""
<plugin key="HmIP-SWDM" name="homematicIP Window and Door Contact with Magnet (HmIP-SWDM)" author="rwbL" version="1.1.1 (Build 20210125)">
    <description>
        <h2>homematicIP Window and Door Contact with Magnet (HmIP-SWDM) v1.1.1</h2>
        <ul style="list-style-type:square">
            <li>Get the state of the contact Open (1) or Closed (0).</li>
        </ul>
        <h3>Domoticz Devices (Type,SubType) [XML-API Device Datapoint Type]</h3>
        <ul style="list-style-type:square">
            <li>State (General,Alert) [STATE]</li>
        </ul>
        <h3>Configuration</h3>
        <ul style="list-style-type:square">
            <li>CCU IP address (default: 192.168.1.225)</li>
            <li>Device ID (default: 3597, get via XML-API script http://ccu-ip-address/addons/xmlapi/statelist.cgi)</li>
        </ul>
    </description>
    <params>
        <param field="Address" label="CCU IP" width="200px" required="true" default="192.168.1.225"/>
        <param field="Mode1" label="Device ID" width="75px" required="true" default="3597"/>
        <param field="Mode5" label="Check Interval (sec)" width="75px" required="true" default="60"/>
        <param field="Mode6" label="Debug" width="75px">
            <options>
                <option label="True" value="Debug" default="true"/>
                <option label="False" value="Normal"/>
            </options>
        </param>
    </params>
</plugin>
"""

# Set the plugin version
PLUGINVERSION = "v1.1.1"
PLUGINSHORTDESCRIPTON = "HMIP-SWDM"

## Imports
import Domoticz
import urllib
import urllib.request
from datetime import datetime
import json
import xml.etree.ElementTree as etree

## Domoticz device units used for creating & updating devices
## And the RaspberryMatic XMLAPI datapoint type
## Each of the devices have a self variable defined in function init
UNIT_STATE = 1               # TypeName: Alert
TYPE_STATE = "STATE"        

## For testing in debug mode only
TYPE_OPERATING_VOLTAGE = "OPERATING_VOLTAGE"

# User Messages - Change as required
MSGSTATECLOSED = "Closed"
MSGSTATEOPEN = "Open"

class BasePlugin:

    def __init__(self):

        # HTTP Connection
        self.httpConn = None
        self.httpConnected = 0

        # State as string as the datapoint value defined 
        self.State = "unknown"
        self.OperatingVoltage = 0
        
        # The Domoticz heartbeat is set to every 60 seconds. Do not use a higher value as Domoticz message "Error: hardware (N) thread seems to have ended unexpectedly"
        # The Soil Moisture Monitor is read every Parameter.Mode5 seconds. This is determined by using a hearbeatcounter which is triggered by:
        # (self.HeartbeatCounter * self.HeartbeatInterval) % int(Parameter.Mode5) = 0
        self.HeartbeatInterval = 60
        self.HeartbeatCounter = 0
        return

    def onStart(self):
        Domoticz.Debug(PLUGINSHORTDESCRIPTON + " " + PLUGINVERSION)
        Domoticz.Debug("onStart called")
        Domoticz.Debug("Debug Mode:" + Parameters["Mode6"])

        if Parameters["Mode6"] == "Debug":
            self.debug = True
            Domoticz.Debugging(1)
            DumpConfigToLog()

        # if there no  devices, create these
        if (len(Devices) == 0):
            Domoticz.Debug("Creating new devices ...")
            ## 1 - STATE - TypeName: Alert (Type=243, Subtype=22)
            Domoticz.Device(Name="State", Unit=UNIT_STATE, Type=243, Subtype=22, Used=1).Create()
            Devices[UNIT_STATE].Update( nValue=1, sValue=MSGSTATECLOSED )
            Domoticz.Debug("Device created: "+Devices[UNIT_STATE].Name)
            Domoticz.Debug("Creating new devices: OK")

        # Heartbeat
        Domoticz.Debug("Heartbeat set: "+Parameters["Mode5"])
        Domoticz.Heartbeat(self.HeartbeatInterval)
        return

    def onStop(self):
        Domoticz.Debug("Plugin is stopping.")

    # Send the url parameter (GET request)
    # If task = energy then to obtain device state information in xml format
    # If task = switch then switch using the self.switchstate
    # The http response is parsed in onMessage()
    def onConnect(self, Connection, Status, Description):
        Domoticz.Debug("onConnect called. Status: " + str(Status) + ", Description:" + Description)
        if (Status == 0):
            Domoticz.Debug("CCU connected successfully.")
            self.httpConnected = 1

            # request device id datapoints to get the device state
            ## url example = 'http://192.168.1.225/addons/xmlapi/state.cgi?device_id=3597'
            url = '/addons/xmlapi/state.cgi?device_id=' + Parameters["Mode1"]
                       
            Domoticz.Debug(url)
            sendData = {'Verb' : 'GET',
                        'URL' : url,
                        'Headers' : { 'Content-Type': 'text/xml; charset=utf-8', \
                                        'Connection': 'keep-alive', \
                                        'Accept': 'Content-Type: text/html; charset=UTF-8', \
                                        'Host': Parameters["Address"], \
                                        'User-Agent':'Domoticz/1.0' }
                       }
            self.httpConn.Send(sendData)
            self.httpConn.Disconnect
            return
        else:
            self.httpConnected = 0
            Domoticz.Error("HTTP connection faillure ("+str(Status)+") to: "+Parameters["Address"]+":"+Parameters["Port"]+" with error: "+Description)
            return

    # Parse the http xml response and update the domoticz devices
    def onMessage(self, Connection, Data):
        Domoticz.Debug("onMessage called")
        
        # If not conected, then leave
        if self.httpConnected == 0:
            return

        # Parse the JSON Data Object with keys Status (Number) and Data (ByteArray)
        ## 200 is OK
        responseStatus = int(Data["Status"])
        Domoticz.Debug("STATUS=responseStatus:" + str(responseStatus) + " ;Data[Status]="+Data["Status"])

        ## decode the data using the encoding as given in the xml response string
        responseData = Data["Data"].decode('ISO-8859-1')
        ## Domoticz.Debug("DATA=" + responseData)

        if (responseStatus != 200):
            Domoticz.Error("XML-API response faillure: " + str(responseStatus) + ";" + resonseData)
            return

        # Parse the xml string 
        # Get the xml tree - requires several conversions
        tree = etree.fromstring(bytes(responseData, encoding='utf-8'))
       
        # STATE
        # Get the value for the state 0 = closed, 1 = open
        # <datapoint name="HmIP-RF.001558A99D5A78:1.STATE" type="STATE" ise_id="3622" value="0" valuetype="16" valueunit="""" timestamp="1611044101"/>
        statevalue = tree.find(".//datapoint[@type='" + TYPE_STATE + "']").attrib['value']
        Domoticz.Debug(TYPE_STATE + "=" + statevalue)

        ## update the alert device if raspmatic value not equal domoticz value
        if statevalue != self.State:
            if statevalue == "0":
                Devices[UNIT_STATE].Update( nValue=1, sValue=MSGSTATECLOSED )
            if statevalue == "1":
                Devices[UNIT_STATE].Update( nValue=4, sValue=MSGSTATEOPEN )
            Domoticz.Log(PLUGINSHORTDESCRIPTON + ": State changed to " + Devices[UNIT_STATE].sValue)
            # Domoticz.Debug("S Update=" + Devices[UNIT_STATE].sValue)
        self.State = statevalue

        # OPERATING_VOLTAGE
        operatingvoltagevalue = tree.find(".//datapoint[@type='" + TYPE_OPERATING_VOLTAGE + "']").attrib['value']
        Domoticz.Log(TYPE_OPERATING_VOLTAGE + "=" + operatingvoltagevalue)
        return
        
    def onCommand(self, Unit, Command, Level, Hue):
        Domoticz.Debug("onCommand called for Unit " + str(Unit) + ": Parameter '" + str(Command) + "', Level: " + str(Level))
        return

    def onNotification(self, Name, Subject, Text, Status, Priority, Sound, ImageFile):
        Domoticz.Debug("Notification: " + Name + "," + Subject + "," + Text + "," + Status + "," + str(Priority) + "," + Sound + "," + ImageFile)

    def onDisconnect(self, Connection):
        Domoticz.Debug("onDisconnect called")

    # Check the hearbeat counter and setup the http connection to the ccu
    # After connection, there url parameter are send - see onConnect()
    def onHeartbeat(self):
        self.HeartbeatCounter = self.HeartbeatCounter + 1
        Domoticz.Debug("onHeartbeat called. Counter=" + str(self.HeartbeatCounter * self.HeartbeatInterval) + " (Heartbeat=" + Parameters["Mode5"] + ")")
        # check the heartbeatcounter against the heartbeatinterval
        if (self.HeartbeatCounter * self.HeartbeatInterval) % int(Parameters["Mode5"]) == 0:
            try:
                # Create IP connection and connect
                self.httpConn = Domoticz.Connection(Name="CCU-"+Parameters["Address"], Transport="TCP/IP", Protocol="HTTP", Address=Parameters["Address"], Port="80")
                self.httpConn.Connect()
                self.httpConnected = 0
            except:
                Domoticz.Error("IP connection failed. Check settings and restart Domoticz.")
        return
        
global _plugin
_plugin = BasePlugin()

def onStart():
    global _plugin
    _plugin.onStart()

def onStop():
    global _plugin
    _plugin.onStop()

def onConnect(Connection, Status, Description):
    global _plugin
    _plugin.onConnect(Connection, Status, Description)

def onMessage(Connection, Data):
    global _plugin
    _plugin.onMessage(Connection, Data)

def onCommand(Unit, Command, Level, Hue):
    global _plugin
    _plugin.onCommand(Unit, Command, Level, Hue)

def onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile):
    global _plugin
    _plugin.onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile)

def onDisconnect(Connection):
    global _plugin
    _plugin.onDisconnect(Connection)

def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()

#
## Generic helper functions
#

def DumpConfigToLog():
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Debug( "'" + x + "':'" + str(Parameters[x]) + "'")
    Domoticz.Debug("Device count: " + str(len(Devices)))
    for x in Devices:
        Domoticz.Debug("Device:           " + str(x) + " - " + str(Devices[x]))
        Domoticz.Debug("Device ID:       '" + str(Devices[x].ID) + "'")
        Domoticz.Debug("Device Name:     '" + Devices[x].Name + "'")
        Domoticz.Debug("Device nValue:    " + str(Devices[x].nValue))
        Domoticz.Debug("Device sValue:   '" + Devices[x].sValue + "'")
        Domoticz.Debug("Device LastLevel: " + str(Devices[x].LastLevel))
    return

