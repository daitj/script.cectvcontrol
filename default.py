from tv import Television, TelevisionRemoteCode
import xbmcaddon
import urlparse
import sys
import xbmc

addonID = 'script.cectvcontrol'
addon = xbmcaddon.Addon(id=addonID)


def log(msg, level=xbmc.LOGERROR):
    xbmc.log(msg="{}: {}".format(addonID, msg), level=level)


def check_result(result):
    if not result == "ok":
        if result == "not":
            log("TV Not Found")
        else:
            log("Error occurred {}".format(result))


def default_function():
    log("Sending Activate Source and StandyBy to CEC", xbmc.LOGINFO)
    #xbmc.executebuiltin("CECActivateSource")
    xbmc.executebuiltin("CECStandby")


def on_function():
    log("Sending Activate Source to CEC", xbmc.LOGINFO)
    xbmc.executebuiltin("CECActivateSource")


def off_function():
    timeout = int(float(addon.getSetting('timeout')))
    retries = int(float(addon.getSetting('retries')))
    device_ip = addon.getSetting('forceIP')
    tv = Television(device_ip, timeout, retries)
    if tv.errors <> "":
        log(tv.errors)
    else:
        log("Sending off code to TV", xbmc.LOGINFO)
        Codes = TelevisionRemoteCode
        result = tv.send(Codes.TR_KEY_POWER)
        check_result(result)


def app_exit_sequence():
    timeout = int(float(addon.getSetting('timeout')))
    retries = int(float(addon.getSetting('retries')))
    device_ip = addon.getSetting('forceIP')
    tv = Television(device_ip, timeout, retries)
    if tv.errors <> "":
        log(tv.errors)
    else:
        log("Sending app exit code to TV", xbmc.LOGINFO)
        Codes = TelevisionRemoteCode
        result = tv.send(Codes.TR_KEY_EXIT)
        check_result(result)
        xbmc.sleep(500)
        result = tv.send(Codes.TR_KEY_DOWN)
        check_result(result)
        xbmc.sleep(500)
        result = tv.send(Codes.TR_KEY_OK)
        check_result(result)

to_parse = ""

if len(sys.argv) >= 2:
    to_parse = sys.argv[1]

args = urlparse.parse_qs(to_parse)
mode = args.get('mode', 'other')

if mode[0] == 'on':
    log("Turning on", xbmc.LOGINFO)
    on_function()
elif mode[0] == 'off':
    log("Turning off", xbmc.LOGINFO)
    off_function()
elif mode[0] == 'app_exit':
    log("Exiting Smart App like Netflix", xbmc.LOGINFO)
    app_exit_sequence()
else:
    log("No action defined, doing default action", xbmc.LOGINFO)
    default_function()
