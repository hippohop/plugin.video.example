import sys
import urllib.parse
import xbmcplugin
import xbmcgui
import xbmcaddon
import xbmc

# Inicializace
addon_handle = int(sys.argv[1])
args = sys.argv[2]
addon = xbmcaddon.Addon()

def log(msg):
    xbmc.log(f"[HROCH CINEMA] {msg}", xbmc.LOGNOTICE)

def build_url(query):
    return sys.argv[0] + '?' + urllib.parse.urlencode(query)

def router(params):
    log(f"Routing parametry: {params}")
    if not params:
        # Hlavní menu – položka pro vyhledávání
        url = build_url({"action": "search"})
        list_item = xbmcgui.ListItem(label="🔍 Vyhledat film")
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=list_item, isFolder=True)
        xbmcplugin.endOfDirectory(addon_handle)
        return

    if params.get("action") == "search":
        # Tady později přidáme vyhledávací dialog
        xbmcgui.Dialog().ok("Hroch Cinema", "Zde bude vyhledávání filmu...")
        return

# Hlavní vstup
log("Startuji main.py")
params = dict(urllib.parse.parse_qsl(args[1:]))
router(params)
