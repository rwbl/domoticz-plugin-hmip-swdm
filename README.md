# Domoticz Plugin homematicIP Window and Door Contact with magnet (HMIP-SWDM)
Domoticz plugin for the homematicIP Window and Door Contact with magnet (HMIP-SWDM).

# Objectives
* To monitor the state open / close of windows and doors
* To alert via notification in case state is open using Domoticz dzVents script

![domoticz-plugin-hmip-swdm-o](https://user-images.githubusercontent.com/47274144/105820917-79fb4c00-5fba-11eb-8acc-da71fd4bb98a.png)

## Solution
To monitor the state open / close of windows and doors the homematicIP Window and Door Contact with magnet (HMIP-SWDM) is used.
The HMIP-SWDM is connected to a homematic IP system.
The homematic IP system used is a [RaspberryMatic](https://raspberrymatic.de/) operating system running the Homematic Central-Control-Unit (CCU).
The CCU has the additional software XML-API CCU Addon installed.
Communication between Domoticz and the CCU is via HTTP XML-API requests with HTTP XML response.

In Domoticz, following device(s) is/are created:
(Type,SubType) [XML-API Device Datapoint Type] - Note)
* Alert (General,Alert) [STATE] - closed (green) or open (red)

The device state is updated every 60 seconds (default).

If required, further actions can defined, by for example creating a dzVents script to send a notification / email (see below "dzVents Example").

## Hardware
Hardware subject to change.
* Raspberry Pi 3B+ (RaspberryMatic System)
* homematicIP Window and Door Contact with magnet (HMIP-SWDM)

## Software
Software versions subject to change.
* Raspberry Pi OS ( Raspbian GNU/Linux 10 buster, kernel 5.4.83-v7l+)
* Domoticz 2020.2 (build 12847)
* RaspberryMatic 3.55.5.20201226 [info](https://raspberrymatic.de/)
* XML-API CCU Addon 1.20 [info](https://github.com/jens-maus/XML-API)
* Python 3.7.3
* Python module ElementTree

**Note on the Python Module ElementTree**
The Python Module **ElementTree XML API** is used to parse the XML-API response.
This module is part of the standard package and provides limited support for XPath expressions for locating elements in a tree. 

_Hint_
(Optional)
For full XPath support install the module **ElementPath** from the terminal command-line for Python 2.x and 3.x via pip:
``` 
sudo pip install elementpath
sudo pip3 install elementpath
```

## RaspberryMatic Prepare
The RaspberryMatic system has been setup according [these](https://github.com/jens-maus/RaspberryMatic) guidelines.

The XML-API CCU Addon is required and installed via the HomeMatic WebUI > Settings > Control panel > Additional software (download the latest version from previous URL shared).
**IMPORTANT**
Be aware of the security risk, in case the HomeMatic Control Center can be reached via the Internet without special protection (see XML-API Guidelines).

### XML-API Scripts
The XML-API provides various tool scripts, i.e. devices state list, device state or set new value and many more.
The scripts are submitted via HTTP XML-API requests.
The plugin makes selective use of scripts with device id and datapoint id's.
The device id is required to get the state of the device datapoints. The datapoint id's are required to get the state/value of device attributes.

#### Device ID (statelist.cgi)
Get Device ID (attribute "ise_id") from list of all devices with channels and current values: http://ccu-ip-address/addons/xmlapi/statelist.cgi.

From the HTTP XML-API response, the Device ID ("ise_id") is selected by searching for the
* Device Name (i.e. Garagentor) or 
* Device Channel (HmIP-SWDM 001558A99D5A78:1). 
The data is obtained from the HomeMatic WebUI Home page > Status and control > Devices.
The Device "ise_id" is required for the plugin parameter _Mode1_.
HTTP XML-API response: Device ID = 3597.
```
...
<device name="Garagentor" ise_id="3597" unreach="false" config_pending="false">
	<channel...>
</device>
...
```
This script 
* has to be run once from a browser prior installing the plugin to get the device id as required by the plugin parameter Device ID ("mode1") and the next script.
* is not used in the plugin.

#### Channel Datapoint(s) (state.cgi)
Request the Channel Datapoint(s) for a Device ID to get value(s) for selected attribute(s): http://ccu-ip-address/addons/xmlapi/state.cgi?device_id=DEVICE_ISE_ID
The **Device ID 3597** is used as parameter to get the device state from which the attributes can be selected. 
The HTTP XML-API response lists three Channels from which **Channel HmIP-SWDM 001558A99D5A78:1** (as previous shown in the HomeMatic WebUI) is used.
The datapoint(s) used:
* type="STATE" with ise_id="3622" to get the state of the contact. The value is from valuetype 16, i.e. 1 (open) or 0 (closed).
The datapoint "ise_id" is required for the plugin parameter _Mode2_.
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
This script 
* has to be run once from a browser prior installing the plugin to get the datapoint id as required by the plugin hardware Datapoint ID STATE ("mode2").
* is used in the plugin to get the device state in regular check intervals.
#### Change Value (statechange.cgi)
Change the State or Value for a Datapoint: http://ccu-ip-address/addons/xmlapi/statechange.cgi?ise_id=DATAPOINT_ISE_ID&new_value=NEW_VALUE
This script 
* is not used by the plugin.

#### Summary
The device id "3597" (for the device named "Garagentor") is used to 
* get the state "0" (closed") or "1" (open") of the channel "HmIP-SWDM 001558A99D5A78:1" datapoint type "STATE", ise_id "3622". 

## Domoticz Prepare
Open in a browser, four tabs with the Domoticz GUI Tabs: 
* Setup > Hardware = to add / delete the new hardware
* Setup > Devices = to check the devices created by the new hardware (use button Refresh to get the latest values)
* Setup > Log = to check the installation and check interval cycles for errors
* Active Menu depending Domoticz Devices created/used = to check the devices value
Ensure to have the latest Domoticz version installed: Domoticz GUI Tab Setup > Check for Update

### Domoticz Plugin Installation

### Plugin Folder and File
Each plugin requires a dedicated folder which contains the plugin, mandatory named **plugin.py**.
The folder is named according omematic IP device name. 
``` 
mkdir /home/pi/domoticz/plugins/hmip-swdm
``` 

Copy the file **plugin.py** to the folder.

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
* Device ID: The device datapoint ise_id - taken from the XMLAPI statelist request. Default: 3597.
* Datapoint STATE: The STATE datapoint ise_id - taken from the XMLAPI statelist request. Default: 3622.
* Check Interval (sec): How often the state of the device is checked. Default: 60.
* Debug: Set initially to true. If the plugin runs fine, update to false.

### Add Hardware - Check the Domoticz Log
After adding, ensure to check the Domoticz Log (GUI > Setup > Log)
Example - with hardware name C1 (just a name for testing instead using german name "Garagentor")
```
2021-01-25 13:26:15.675 (Garagentor) Debug logging mask set to: PYTHON PLUGIN QUEUE IMAGE DEVICE CONNECTION MESSAGE ALL
2021-01-25 13:26:15.675 (Garagentor) 'HardwareID':'14'
2021-01-25 13:26:15.675 (Garagentor) 'HomeFolder':'/home/pi/domoticz/plugins/hmip-swdm/'
2021-01-25 13:26:15.675 (Garagentor) 'StartupFolder':'/home/pi/domoticz/'
2021-01-25 13:26:15.675 (Garagentor) 'UserDataFolder':'/home/pi/domoticz/'
2021-01-25 13:26:15.675 (Garagentor) 'Database':'/home/pi/domoticz/domoticz.db'
2021-01-25 13:26:15.675 (Garagentor) 'Language':'en'
2021-01-25 13:26:15.675 (Garagentor) 'Version':'1.1.1 (Build 20210125)'
2021-01-25 13:26:15.675 (Garagentor) 'Author':'rwbL'
2021-01-25 13:26:15.675 (Garagentor) 'Name':'Garagentor'
2021-01-25 13:26:15.675 (Garagentor) 'Address':'192.168.1.225'
2021-01-25 13:26:15.675 (Garagentor) 'Port':'0'
2021-01-25 13:26:15.675 (Garagentor) 'Key':'HmIP-SWDM'
2021-01-25 13:26:15.675 (Garagentor) 'Mode1':'3597'
2021-01-25 13:26:15.675 (Garagentor) 'Mode5':'60'
2021-01-25 13:26:15.675 (Garagentor) 'Mode6':'Debug'
2021-01-25 13:26:15.675 (Garagentor) 'DomoticzVersion':'2020.2 (build 12883)'
2021-01-25 13:26:15.675 (Garagentor) 'DomoticzHash':'1a7e11b7d-modified'
2021-01-25 13:26:15.675 (Garagentor) 'DomoticzBuildTime':'2021-01-24 08:48:01'
2021-01-25 13:26:15.675 (Garagentor) Device count: 0
2021-01-25 13:26:15.675 (Garagentor) Creating new devices ...
2021-01-25 13:26:15.675 (Garagentor) Creating device 'State'.
2021-01-25 13:26:15.676 (Garagentor - State) Updating device from 0:'' to have values 1:'Closed'.
2021-01-25 13:26:15.683 (Garagentor) Device created: Garagentor - State
2021-01-25 13:26:15.683 (Garagentor) Creating new devices: OK
2021-01-25 13:26:15.683 (Garagentor) Heartbeat set: 60
2021-01-25 13:26:15.683 Python Plugin System: (Garagentor) Pushing 'PollIntervalDirective' on to queue
2021-01-25 13:26:15.683 (Garagentor) Processing 'PollIntervalDirective' message
2021-01-25 13:26:15.683 Python Plugin System: (Garagentor) Heartbeat interval set to: 60.
2021-01-25 13:26:15.386 Status: Python Plugin System: (Garagentor) Started.
2021-01-25 13:26:15.673 Status: Python Plugin System: (Garagentor) Entering work loop.
2021-01-25 13:26:15.674 Status: Python Plugin System: (Garagentor) Initialized version 1.1.1 (Build 20210125), author 'rwbL'
```

### Domoticz Device List
Idx, Hardware, Name, Type, SubType, Data
80, Garagentor, State, General, Alert, Closed

### Domoticz Log Entry with Debug=False
The plugin runs every 60 seconds (Heartbeat interval).
```
2021-01-25 13:26:25.829 (Garagentor) HMIP-SWDM: State changed to Closed
2021-01-25 13:26:25.829 (Garagentor) OPERATING_VOLTAGE=2.700000
```

```
2021-01-25 13:29:25.871 (Garagentor) HMIP-SWDM: State changed to Open
2021-01-25 13:29:25.871 (Garagentor) OPERATING_VOLTAGE=2.700000
```

## Domoticz dzVents Script alert_window-door-contact
This is an example on how to alert via email
```
--[[
    alert_window-door-contact.dzvents
    Window-Door-Contact (homematicIP device HmIP-SWDM) Alert Example.
    Send notification if the level of the Alert device changes to 4 (RED).
    20210120 rwbl
]]--

local IDX_WINDOWDOORCONTACT = 80;   -- Type General, SubType Alert

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
            local message = ('Window-Door-Contact Garagentor %s changed to %s.'):format(device.name, device.sValue)
            domoticz.notify(subject, message, domoticz.PRIORITY_HIGH)
        end
	end
}
```

## ToDo
See TODO.md
