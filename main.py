# -*- coding: utf-8 -*-
import sys
import xbmc
import xbmcgui
import xbmcplugin
import urllib.parse

try:
    ADDON_HANDLE = int(sys.argv[1])
    BASE_URL = sys.argv[0]
except Exception as e:
    xbmcgui.Dialog().notification("Hroch Cinema", f"CHYBA INIT: {str(e)}", xbmcgui.NOTIFICATION_ERROR)
    raise

def build_url(query):
    return BASE_URL + '?' + urllib.parse.urlencode(query)

def show_search_dialog():
    query = xbmcgui.Dialog().input("Hledat film na TMDb", type=xbmcgui.INPUT_ALPHANUM)
    if query:
        xbmc.log(f"[HROCH CINEMA] Vyhledávání přes TMDb Helper: {query}", xbmc.LOGINFO)
        encoded_query = urllib.parse.quote_plus(query)
        url = f'plugin://plugin.video.themoviedb.helper/?action=search&query={encoded_query}'
        xbmc.executebuiltin(f'RunPlugin("{url}")')

def router(paramstring):
    xbmcplugin.setPluginCategory(ADDON_HANDLE, "Hroch Cinema")
    xbmcplugin.setContent(ADDON_HANDLE, 'videos')

    params = dict(urllib.parse.parse_qsl(paramstring))
    xbmc.log(f"[HROCH CINEMA] Routing params: {params}", xbmc.LOGINFO)

    if params.get('action') == 'search':
        show_search_dialog()
    else:
        list_item = xbmcgui.ListItem(label="🔍 Hledat film")
        url = build_url({'action': 'search'})
        xbmcplugin.addDirectoryItem(handle=ADDON_HANDLE, url=url, listitem=list_item, isFolder=True)
        xbmcplugin.endOfDirectory(ADDON_HANDLE)

if __name__ == '__main__':
    try:
        param_string = sys.argv[2][1:] if len(sys.argv) > 2 else ''
        router(param_string)
    except Exception as e:
        xbmc.log(f"[HROCH CINEMA] CHYBA: {str(e)}", xbmc.LOGERROR)
        xbmcgui.Dialog().notification("CHYBA MAIN", f"{str(e)}", xbmcgui.NOTIFICATION_ERROR)
