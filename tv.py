import socket
import ssdp
import urllib2
import xml.etree.ElementTree as elemtree
import sys
import re

class TelevisionRemoteCode:
    TR_KEY_1="TR_KEY_1"
    TR_KEY_2="TR_KEY_2"
    TR_KEY_3="TR_KEY_3"
    TR_KEY_4="TR_KEY_4"
    TR_KEY_5="TR_KEY_5"
    TR_KEY_6="TR_KEY_6"
    TR_KEY_7="TR_KEY_7"
    TR_KEY_8="TR_KEY_8"
    TR_KEY_9="TR_KEY_9"
    TR_KEY_0="TR_KEY_0"
    TR_KEY_UP="TR_KEY_UP"
    TR_KEY_DOWN="TR_KEY_DOWN"
    TR_KEY_LEFT="TR_KEY_LEFT"
    TR_KEY_RIGHT="TR_KEY_RIGHT"
    TR_KEY_OK="TR_KEY_OK"
    TR_KEY_BACK="TR_KEY_BACK"
    TR_KEY_3D="TR_KEY_3D"
    TR_KEY_SUBMENU="TR_KEY_SUBMENU"
    TR_KEY_MAINMENU="TR_KEY_MAINMENU"
    TR_KEY_POWER="TR_KEY_POWER"
    TR_KEY_VOL_UP="TR_KEY_VOL_UP"
    TR_KEY_VOL_DOWN="TR_KEY_VOL_DOWN"
    TR_KEY_MUTE="TR_KEY_MUTE"
    TR_KEY_EPG="TR_KEY_EPG"
    TR_KEY_DISPLAY="TR_KEY_DISPLAY"
    TR_KEY_PLAYBACK="TR_KEY_PLAYBACK"
    TR_KEY_CH_UP="TR_KEY_CH_UP"
    TR_KEY_CH_DOWN="TR_KEY_CH_DOWN"
    TR_KEY_SOURCE="TR_KEY_SOURCE"
    TR_KEY_SCALE="TR_KEY_SCALE"
    TR_KEY_PICTURE="TR_KEY_PICTURE"
    TR_KEY_FAVORITE="TR_KEY_FAVORITE"
    TR_KEY_SEARCH="TR_KEY_SEARCH"
    TR_KEY_RED="TR_KEY_RED"
    TR_KEY_GREEN="TR_KEY_GREEN"
    TR_KEY_YELLOW="TR_KEY_YELLOW"
    TR_KEY_BLUE="TR_KEY_BLUE"
    TR_KEY_BACKSPACE="TR_KEY_BACKSPACE"
    TR_KEY_MOUSELEFT="TR_KEY_MOUSELEFT"
    TR_KEY_MOUSERIGHT="TR_KEY_MOUSERIGHT"
    TR_KEY_INFOWINDOW="TR_KEY_INFOWINDOW"
    TR_KEY_VOICEINPUT="TR_KEY_VOICEINPUT"
    TR_KEY_VOICEREAD="TR_KEY_VOICEREAD"
    TR_KEY_VOICESEARCH="TR_KEY_VOICESEARCH"
    TR_KEY_SMARTTV="TR_KEY_SMARTTV"
    TR_KEY_HOME="TR_KEY_HOME"
    TR_KEY_EXIT="TR_KEY_EXIT"
    TR_KEY_USB="TR_KEY_USB"
    TR_KEY_ZOOM_UP="TR_KEY_ZOOM_UP"
    RE_KEY_ZOOM_DOWN="RE_KEY_ZOOM_DOWN"
    TR_KEY_PRE_CH="TR_KEY_PRE_CH"
    TR_KEY_LIST="TR_KEY_LIST"
    TR_KEY_OPTION="TR_KEY_OPTION"
    TR_KEY_TV="TR_KEY_TV"
    TR_KEY_NETFLIX="TR_KEY_NETFLIX"
    TR_KEY_YOUTUBE="TR_KEY_YOUTUBE"
    TR_KEY_LANG="TR_KEY_LANG"
    TR_KEY_TEXT="TR_KEY_TEXT"
    TR_KEY_PREVIOUS="TR_KEY_PREVIOUS"
    TR_KEY_NEXT="TR_KEY_NEXT"
    TR_KEY_SUSPEND="TR_KEY_SUSPEND"
    TR_KEY_PLAYPAUSE="TR_KEY_PLAYPAUSE"
    TR_KEY_REW="TR_KEY_REW"
    TR_KEY_FF="TR_KEY_FF"
    TR_KEY_REC="TR_KEY_REC"
    TR_KEY_SUBTITLE="TR_KEY_SUBTITLE"
    TR_KEY_ZOOM_DOWN="TR_KEY_ZOOM_DOWN"
    TR_KEY_MEDIA="TR_KEY_MEDIA"
    TR_KEY_GUIDE="TR_KEY_GUIDE"
    TR_KEY_ECO="TR_KEY_ECO"
    TR_KEY_SOUND="TR_KEY_SOUND"
    TR_KEY_FREEZE="TR_KEY_FREEZE"
    TR_KEY_MTS="TR_KEY_MTS"
    TR_KEY_INPUT="TR_KEY_INPUT"
    TR_KEY_DOT="TR_KEY_DOT"
    TR_KEY_AMAZON="TR_KEY_AMAZON"
    TR_KEY_MGO="TR_KEY_MGO"
    TR_KEY_HULU="TR_KEY_HULU"
    TR_KEY_SLEEP_UP="TR_KEY_SLEEP_UP"
    TR_KEY_SLEEP_DOWN="TR_KEY_SLEEP_DOWN"
    TR_KEY_VUDU="TR_KEY_VUDU"
    TR_KEY_TUNER="TR_KEY_TUNER"
    TR_KEY_CC="TR_KEY_CC"
    TR_KEY_SLEEP="TR_KEY_SLEEP"
    TR_KEY_APP="TR_KEY_APP"
    TR_KEY_AT="TR_KEY_AT"
    TR_KEY_AIRCABLE="TR_KEY_AIRCABLE"
    TR_KEY_I="TR_KEY_I"
    TR_KEY_FORMAT="TR_KEY_FORMAT"
    TR_KEY_PLAY="TR_KEY_PLAY"
    TR_KEY_PAUSE="TR_KEY_PAUSE"
    TR_KEY_APPSTORE="TR_KEY_APPSTORE"
    TR_KEY_ALLAPP="TR_KEY_ALLAPP"


class Television:
    def send(self, key_code):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.ip, 4123))
            s.send('<?xml version="1.0" encoding="utf-8"?><root><action name="setKey" eventAction="TR_PRESS" keyCode="{}" /></root>'.format(key_code))
            s.close()
            return "ok"
        except socket.error:
            return "not"
        except:
            return sys.exc_info()[0]

    def get_and_parse_xml(self, location):
        try:
            u = urllib2.urlopen(location)
            try:
                xmlstring = u.read()
                xmlstring = re.sub('\\sxmlns="[^"]+"', '', xmlstring, count=1)
                root = elemtree.fromstring(xmlstring)
                return root
            except:
                print sys.exc_info()[0]
                return None
        except:
            print sys.exc_info()[0]
            return None

    def __init__(self, fallback_ip, timeout, retries):
        tv_ip = ""
        error_text = ""
        if fallback_ip <> "":
            tv_ip = fallback_ip
        else:
            response = ssdp.discover("urn:schemas-upnp-org:device:MediaRenderer:1",timeout,retries)
            if response:
                for r in response:
                    if r.location:
                        xml = self.get_and_parse_xml(r.location)
                        for device in xml.findall('./device/friendlyName'):
                            if "THOMSON" in device.text:
                                tv_ip = r.location.replace("http://","").replace("/dmr.xml","").split(":")[0]
                        if tv_ip == "":
                            error_text = "TV not found"
                    else:
                        error_text += "No ssdp location"
            else:
                error_text += "No ssdp response"
            if tv_ip == "":
                tv_ip = fallback_ip
        self.ip = tv_ip
        self.errors = error_text

