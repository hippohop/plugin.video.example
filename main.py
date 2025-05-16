# -*- coding: utf-8 -*-
import sys
import xbmc
import xbmcgui
import xbmcplugin
import urllib.parse

ADDON_HANDLE = int(sys.argv[1])
BASE_URL = sys.argv[0]

def build_url(query):
    return BASE_URL + '?' + urllib.parse.urlencode(query)

def router(paramstring):
    params = dict(urllib.parse.parse_qsl(paramstring))
    xbmc.log(f"[HROCH CINEMA] Routing params: {params}", xbmc.LOGNOTICE)
    
    if params.get('action') == 'search':
        show_search_dialog()
    else:
        # Defaultní akce: otevřít dialog hledání
        show_search_dialog()

def show_search_dialog():
    keyboard = xbmcgui.Dialog().input("Zadej název filmu", type=xbmcgui.INPUT_ALPHANUM)
    if keyboard:
        # V tuto chvíli vypíšeme pouze zadaný název, později zde bude hledání přes TMDb
        xbmc.log(f"[HROCH CINEMA] Hledání pro: {keyboard}", xbmc.LOGNOTICE)
        list_item = xbmcgui.ListItem(label=f"Hledání: {keyboard}")
        url = build_url({'action': 'search', 'query': keyboard})
        xbmcplugin.addDirectoryItem(handle=ADDON_HANDLE, url=url, listitem=list_item, isFolder=True)
        xbmcplugin.endOfDirectory(ADDON_HANDLE)
    else:
        xbmcplugin.endOfDirectory(ADDON_HANDLE, succeeded=False)

if __name__ == '__main__':
    router(sys.argv[2][1:])
