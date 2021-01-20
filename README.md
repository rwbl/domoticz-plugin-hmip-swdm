# Domoticz Plugin homematicIP (HMIP-SWDM)

# Objectives
* To monitor the state open / close of windows and doors

_Abbreviations_: GUI=Domoticz Web UI, CCU=HomeMatic Central-Control-Unit

## Solution
To monitor the state open / close of windows and doors the homematicIP Window and Door Contact with magnet (HMIP-SWDM) is used.
The HMIP-SWDM is connected to a homematic IP system.
The homematic IP system used is a [RaspberryMatic](https://raspberrymatic.de/) operating system running the Homematic Central-Control-Unit (CCU).
The CCU has the additional software XML-API CCU Addon installed.
Communication between Domoticz and the CCU is via HTTP XML-API requests with HTTP XML response.

In Domoticz, an Alert device shows the state closed (green) or open (red). The state is updated every 60 seconds (default).
If required, further actions can defined, by for example creating a dzVents script to send a notification / email (see below "dzVents Example").

## Hardware
* Raspberry Pi 3B+ (RaspberryMatic System)
* homematicIP Window and Door Contact with magnet (HMIP-SWDM)

## Software
Versions for developing & using this plugin.
* Raspberry Pi OS ( Raspbian GNU/Linux 10 buster, kernel 5.4.83-v7l+)
* Domoticz 2020.2 (build 12847)
* RaspberryMatic 3.55.5.20201226 [info](https://raspberrymatic.de/)
* XML-API CCU Addon 1.20 [info](https://github.com/jens-maus/XML-API)
* Python 3.7.3
* Python module ElementTree

## Prepare
The RaspberryMatic system has been setup according [these](https://github.com/jens-maus/RaspberryMatic) guidelines.
The XML-API CCU Addon is required and installed via the HomeMatic WebUI > Settings > Control panel > Additional software (download the latest version from previous URL shared).

### Python Module ElementTree
The Python Module **ElementTree XML API** is used to parse the XML-API response.
This module is part of the standard package and provides limited support for XPath expressions for locating elements in a tree. 

_Hint_
(Optional)
For full XPath support install the module **ElementPath** from the terminal command-line for Python 2.x and 3.x via pip:
``` 
sudo pip install elementpath
sudo pip3 install elementpath
```

## Installation Plugin

### Plugin Folder and File
Each plugin requires a dedicated folder which contains the plugin, mandatory named plugin.py.
``` 
mkdir /home/pi/domoticz/plugins/hmip-swdm
``` 

Copy plugin.py to the folder.

### Restart Domoticz
``` 
sudo service domoticz.sh restart
``` 

### Domoticz Add Hardware
**IMPORTANT**
Prior adding the hardware, set in Domoticz GUI > Settings the option to allow new hardware.
If this option is not enabled, no new devices are created.
Check the GUI > Setup > Log as error message Python script at the line where the new device is used
(i.e. Domoticz.Debug("Device created: "+Devices[1].Name))

In the GUI > Setup > Hardware add the new hardware **homematicIP Window and Door Contact with Magnet (HmIP-SWDM)**.
Define the hardware parameter:
* CCU IP: The IP address of the homematic CCU. Default: 192.168.1.225.
* Device: The device datapoint ise_id - taken from the XMLAPI statelist request (see below "Get Device Datapoints"). Default: 3597.
* Datapoint STATE: The STATE datapoint ise_id - taken from the XMLAPI statelist request (see below). Default: 3622.
* Check Interval (sec): How often the state of the device is checked. Default: 60.
* Debug: Set initially to true. If the plugin runs fine, update to false.

### Add Hardware - Check the Domoticz Log
After adding, ensure to check the Domoticz Log (GUI > Setup > Log)
Example - with hardware name C1 (just a name for testing instead using german name "Garagentor")
```
2021-01-19 10:25:36.952 Status: Python Plugin System: (C1) Started.
2021-01-19 10:25:37.208 (C1) Debug logging mask set to: PYTHON PLUGIN QUEUE IMAGE DEVICE CONNECTION MESSAGE ALL
2021-01-19 10:25:37.208 (C1) 'HardwareID':'13'
2021-01-19 10:25:37.208 (C1) 'HomeFolder':'/home/pi/domoticz/plugins/hmip-swdm/'
2021-01-19 10:25:37.208 (C1) 'StartupFolder':'/home/pi/domoticz/'
2021-01-19 10:25:37.208 (C1) 'UserDataFolder':'/home/pi/domoticz/'
2021-01-19 10:25:37.208 (C1) 'Database':'/home/pi/domoticz/domoticz.db'
2021-01-19 10:25:37.208 (C1) 'Language':'en'
2021-01-19 10:25:37.208 (C1) 'Version':'1.0.0 (Build 20210119)'
2021-01-19 10:25:37.208 (C1) 'Author':'rwbL'
2021-01-19 10:25:37.208 (C1) 'Name':'C1'
2021-01-19 10:25:37.208 (C1) 'Address':'192.168.1.225'
2021-01-19 10:25:37.208 (C1) 'Port':'0'
2021-01-19 10:25:37.208 (C1) 'Key':'HmIP-SWDM'
2021-01-19 10:25:37.208 (C1) 'Mode1':'3597'
2021-01-19 10:25:37.208 (C1) 'Mode2':'3622'
2021-01-19 10:25:37.208 (C1) 'Mode5':'60'
2021-01-19 10:25:37.208 (C1) 'Mode6':'Debug'
2021-01-19 10:25:37.208 (C1) 'DomoticzVersion':'2020.2 (build 12847)'
2021-01-19 10:25:37.208 (C1) 'DomoticzHash':'815e12372-modified'
2021-01-19 10:25:37.208 (C1) 'DomoticzBuildTime':'2021-01-16 14:57:39'
2021-01-19 10:25:37.208 (C1) Device count: 0
2021-01-19 10:25:37.208 (C1) Creating new devices ...
2021-01-19 10:25:37.208 (C1) Creating device 'State'.
2021-01-19 10:25:37.209 (C1 - State) Updating device from 0:'' to have values 1:'Closed'.
2021-01-19 10:25:37.215 (C1) Device created: C1 - State
2021-01-19 10:25:37.215 (C1) Creating new devices: OK
2021-01-19 10:25:37.215 (C1) Heartbeat set: 60
2021-01-19 10:25:37.216 Python Plugin System: (C1) Pushing 'PollIntervalDirective' on to queue
2021-01-19 10:25:37.216 (C1) Datapoints:3622
2021-01-19 10:25:37.216 (C1) Processing 'PollIntervalDirective' message
2021-01-19 10:25:37.216 Python Plugin System: (C1) Heartbeat interval set to: 60.
2021-01-19 10:25:37.207 Status: Python Plugin System: (C1) Entering work loop.
2021-01-19 10:25:37.207 Status: Python Plugin System: (C1) Initialized version 1.0.0 (Build 20210119), author 'rwbL'
```

### Domoticz Log Entry with Debug=False
The plugin runs every 60 seconds (Heartbeat interval).
```
2021-01-19 15:54:52.571 (C1) State changed to Open
2021-01-19 15:55:52.606 (C1) State changed to Closed
```

## Development Setup
Information about the plugin development setup and process.
Development Device:
* A shared drive Z: pointing to /home/pi/domoticz
* GUI > Setup > Log
* GUI > Setup > Hardware
* GUI > Setup > Devices
* WinSCP session connected to the Domoticz server (upload files)
* Putty session connected to the Domoticz server (restarting Domoticz during development)

The various GUI's are required to add the new hardware with its devices and monitor if the plugin code is running without errors.

## Development Iteration
The development process step used are:
1. Develop z:\plugins\hmip-swdm\plugin.py
2. Make changes and save plugin.py
3. Restart Domoticz from a terminal: sudo service domoticz.sh restart
4. Wait a moment and refresh GUI > Log
5. Check the log and fix as required

!IMPORTANT!
In the **GUI > Setup > Settings**, enable accepting new hardware.
This is required to add new devices created by the plugin.

## Datapoints
To communicate between the CCU and Domoticz vv, the ise_id's for devices, channels and datapoint are used (id solution).
Another option could be to use the name (i.e. name="HmIP-RF.001558A99D5A78:1.STATE") but this requires to obtain the full device state list for every action.
Tested the name solution, but the communication was rather slow.
The id soltion is much faster and also more flexible in defining and obtaning information for devices, channels and datapoints.

## Device Datapoint ID
Steps to obtain the device datapoint id to be able to switch or read the meter data.
The device datapoint id will be used in the plugin parameter _Mode1_.

### Get Device Channels
Get the device channels from the HomeMatic WebUI > Status and control > Devices > select name HmIP-SWDM 001558A99D5A78.
There is one channel:
* HmIP-SWDM 001558A99D5A78:1

### Get All Devices Statelist
Submit in a webbrowser the HTTP URL XMLAPI request:
``` 
http://ccu-ip/addons/xmlapi/statelist.cgi
``` 
The HTTP response is an XML string with the state list for all devices used (can be rather large depending number of devices connected).

### Get Device Datapoints
In the XML response, search options are either by device name or channel as taken from the Homematic WebUI (Home page > Status and control > Devices).
* Device Name - the device is named "Garagentor". 
* Device Channel - there is only one channel HmIP-SWDM 001558A99D5A78:1 which shows the device state open or closed

From the XML-Tree, the datapoints (attribute ise_id) used for the plugin are:
* 3597 - the device name
```
<device name="Garagentor" ise_id="3597" unreach="false" config_pending="false">
```
* 3622 - the state of the contact defined in the channel HmIP-SWDM 001558A99D5A78:1
```
<datapoint name="HmIP-RF.001558A99D5A78:1.STATE" type="STATE" ise_id="3622" value="0" valuetype="16" valueunit="""" timestamp="1611044101" operations="5"/>
```
The full device information with the channels 0 and 1 - channel 1 holds the device state by attribute value "0" = closed, "1"= open.
```
<device name="Garagentor" ise_id="3597" unreach="false" config_pending="false">
	<channel name="Garagentor:0" ise_id="3598" index="0" visible="true" operate="true">
		<datapoint name="HmIP-RF.001558A99D5A78:0.CONFIG_PENDING" type="CONFIG_PENDING" ise_id="3599" value="false" valuetype="2" valueunit="" timestamp="1611044101" operations="5"/>
		<datapoint name="HmIP-RF.001558A99D5A78:0.DUTY_CYCLE" type="DUTY_CYCLE" ise_id="3603" value="false" valuetype="2" valueunit="" timestamp="1611044101" operations="5"/>
		<datapoint name="HmIP-RF.001558A99D5A78:0.LOW_BAT" type="LOW_BAT" ise_id="3605" value="false" valuetype="2" valueunit="" timestamp="1611044101" operations="5"/>
		<datapoint name="HmIP-RF.001558A99D5A78:0.OPERATING_VOLTAGE" type="OPERATING_VOLTAGE" ise_id="3609" value="2.800000" valuetype="4" valueunit="" timestamp="1611044101" operations="5"/>
		<datapoint name="HmIP-RF.001558A99D5A78:0.OPERATING_VOLTAGE_STATUS" type="OPERATING_VOLTAGE_STATUS" ise_id="3610" value="0" valuetype="16" valueunit="" timestamp="1611044101" operations="5"/>
		<datapoint name="HmIP-RF.001558A99D5A78:0.RSSI_DEVICE" type="RSSI_DEVICE" ise_id="3611" value="178" valuetype="8" valueunit="" timestamp="1611044101" operations="5"/>
		<datapoint name="HmIP-RF.001558A99D5A78:0.RSSI_PEER" type="RSSI_PEER" ise_id="3612" value="0" valuetype="8" valueunit="" timestamp="0" operations="5"/>
		<datapoint name="HmIP-RF.001558A99D5A78:0.UNREACH" type="UNREACH" ise_id="3613" value="false" valuetype="2" valueunit="" timestamp="1611044101" operations="5"/>
		<datapoint name="HmIP-RF.001558A99D5A78:0.UPDATE_PENDING" type="UPDATE_PENDING" ise_id="3617" value="false" valuetype="2" valueunit="" timestamp="1610968122" operations="5"/>
	</channel>
	<channel name="HmIP-SWDM 001558A99D5A78:1" ise_id="3621" index="1" visible="true" operate="true">
		<datapoint name="HmIP-RF.001558A99D5A78:1.STATE" type="STATE" ise_id="3622" value="0" valuetype="16" valueunit="""" timestamp="1611044101" operations="5"/>
	</channel>
	<channel name="HmIP-SWDM 001558A99D5A78:2" ise_id="3623" index="2" visible="true" operate="true"/>
</device>
```
The datapoint type="STATE" is used to get the state of the contact via the XML-API script statechange.cgi using the ise_id (i.e. 3622).
This datapoint id will be used in the plugin parameter _Mode2_.
The value is from valuetype 16, i.e. 1 or 0.

### Get Device State
The url to request the device id datapoints to get the device state uses the XMLAPI scrip state.cgi.
This url is used in the plugin to get the device state from datapoint ise_id=3622.
Example url to get the device state:
``` 
http://192.168.1.225/addons/xmlapi/state.cgi?device_id=3597
``` 

## Domoticz Devices
The **Homematic IP Window / Door Contact with magnet** device(s) created.
Name (TypeName)
* Alert (Alert)
Example:
Idx: 87, Hardware: C1, Name: C1 - State, Type: General, SubType: Alert, Data: Open

## Plugin Pseudo Code
Source code (well documented): plugin.py in folder /home/pi/domoticz/plugins/hmip-swdm
__INIT__
* set self vars to handle http connection, heartbeat count, datapoints list
	
__FIRST TIME__
* _onStart_ to create the Domoticz Devices
	
__NEXT TIME(S)__
* _onHeardbeat_
	* create ip connection http with the raspberrymatic szstem
* _onConnect_
	* define the data (get,url,headers) to send to the ip connection
	* send the data and disconnect
* _onMessage_
	* parse the xml response
	* update the alert device with state green (closed) or red (open)
* _onCommand_
	* create ip connection which is handled by onConnect

If required, add the devices manually to the Domoticz Dashboard or create a roomplan / floorplan.

## Restart Domoticz
Restart Domoticz to find the plugin:
```
sudo systemctl restart domoticz.service
```

**Note**
When making changes to the Python plugin code, ensure to restart Domoticz and refresh any of the Domoticz Web UI's.
This is the iteration process during development - build the solution step-by-step.

## dzVents Example
```
--[[
    alert_window-door-contact.dzvents
    Window-Door-Contact (homematicIP device HmIP-SWDM) Alert Example.
    Send notification if the level of the Alert device changes to 4 (RED).
    Domoticz log example for the Alert device name "C1":
        2021-01-20 09:26:28.773 Notification sent (browser) => Success
        2021-01-20 09:26:28.736 Status: dzVents: Info: Handling events for: "C1 - State", value: "Open"
        2021-01-20 09:26:28.736 Status: dzVents: Info: ------ Start internal script: alert_window-door-contact: Device: "C1 - State (C1)", Index: 87
        2021-01-20 09:26:28.736 Status: dzVents: Info: Device C1 - State state changed to Open (4).
        2021-01-20 09:26:28.736 Status: dzVents: Info: ------ Finished alert_window-door-contact
        2021-01-20 09:26:28.736 Status: EventSystem: Script event triggered: /home/pi/domoticz/dzVents/runtime/dzVents.lua
        2021-01-20 09:26:28.772 Status: Notification: SECURITY ALERT
        2021-01-20 09:26:29.546 Notification sent (email) => Success
    20210120 rwbl
]]--

local IDX_WINDOWDOORCONTACT = 87;   -- Type General, SubType Alert

local STATE_CLOSED = 1;             -- Alert level 1 GREEN
local STATE_OPEN = 4;               -- Alert level 4 RED

return {
	on = {
		devices = {
			IDX_WINDOWDOORCONTACT
		}
	},
	execute = function(domoticz, device)
	    domoticz.log(('Device %s state changed to %s (%d).'):format(device.name, device.sValue, device.nValue), domoticz.LOG_INFO)
		if device.nValue == STATE_OPEN then
            -- Send notification via email
            local subject = ('SECURITY ALERT'):format()
            local message = ('Window-Door-Contact %s state changed to %s.'):format(device.name, device.sValue)
            domoticz.notify(subject, message, domoticz.PRIORITY_HIGH)
        end
	end
}
```

## ToDo
See TODO.md
