import xbmcaddon
from urllib.parse import parse_qs
import sys
import xbmc
import json

addonID = 'script.cectvcontrol'
addon = xbmcaddon.Addon(id=addonID)

class CecCommands():
    AVR_ON = "1f:82:11:00"
    AVR_OFF = "15:36"
    TV_ON ="10:04"
    TV_OFF = "10:36"

def log(msg, level=xbmc.LOGERROR):
    xbmc.log(msg="{}: {}".format(addonID, msg), level=level)

def jsonrpc_cec(command):
    rpccmd = {'jsonrpc': '2.0', 'method': 'System.CECSend', 'id': 1, 'params': {"command": command}}
    rpccmd = json.dumps(rpccmd)
    return xbmc.executeJSONRPC(rpccmd)

def default_function():
    jsonrpc_cec(CecCommands.TV_ON)
    jsonrpc_cec(CecCommands.TV_OFF)
    xbmc.executebuiltin('CECToggleState')

to_parse = ""

if len(sys.argv) >= 2:
    to_parse = sys.argv[1]

args = parse_qs(to_parse)
mode = args.get('mode', 'other')

if mode[0] == 'on':
    log("Turning on", xbmc.LOGINFO)
    jsonrpc_cec(CecCommands.TV_ON)
    xbmc.executebuiltin('CECActivateSource')
elif mode[0] == 'off':
    log("Turning off", xbmc.LOGINFO)
    jsonrpc_cec(CecCommands.TV_OFF)
    xbmc.executebuiltin('CECStandby')
elif mode[0] == 'avr_on':
    log("Turning on avr", xbmc.LOGINFO)
    jsonrpc_cec(CecCommands.AVR_ON)
    xbmc.executebuiltin('CECActivateSource')
elif mode[0] == 'avr_off':
    log("Turning off avr", xbmc.LOGINFO)
    jsonrpc_cec(CecCommands.AVR_OFF)
    xbmc.executebuiltin('CECStandby')
else:
    log("No action defined, doing default action", xbmc.LOGINFO)
    default_function()
