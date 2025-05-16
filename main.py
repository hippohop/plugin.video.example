import sys
import urllib.parse
import xbmcplugin
import xbmcgui
import xbmcaddon
import xbmc

addon_handle = int(sys.argv[1])
args = sys.argv[2]
addon = xbmcaddon.Addon()

def log(msg):
    xbmc.log(f"[HROCH CINEMA] {msg}", xbmc.LOGNOTICE)

def build_url(query):
    return sys.argv[0] + '?' + urllib.parse.urlencode(query)

def router(params):
    log(f"Routing parametry: {params}")

    action = params.get("action")
    if action == "search" or not action:
        keyboard = xbmcgui.Dialog().input("Zadej název filmu", type=xbmcgui.INPUT_ALPHANUM)
        if keyboard:
            log(f"Zadán hledaný výraz: {keyboard}")
            xbmcgui.Dialog().ok("Hledání", f"Zadal jsi: {keyboard}")
        else:
            log("Uživatel zrušil hledání.")
        return

log("Startuji main.py")
params = dict(urllib.parse.parse_qsl(args[1:]))
router(params)
