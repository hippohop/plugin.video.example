# -*- coding: utf-8 -*-
import xbmc
import xbmcgui
import urllib.parse

def show_search_dialog():
    query = xbmcgui.Dialog().input("Hledat film na TMDb", type=xbmcgui.INPUT_ALPHANUM)
    if query:
        xbmc.log(f"[HROCH CINEMA] Vyhledávání přes TMDb Helper (výsledky): {query}", xbmc.LOGINFO)
        encoded_query = urllib.parse.quote_plus(query)
        url = f'plugin://plugin.video.themoviedb.helper/?action=search_movies&query={encoded_query}'
        xbmc.executebuiltin(f'RunPlugin("{url}")')

if __name__ == '__main__':
    try:
        show_search_dialog()
    except Exception as e:
        xbmc.log(f"[HROCH CINEMA] CHYBA: {str(e)}", xbmc.LOGERROR)
        xbmcgui.Dialog().notification("CHYBA TMDb", f"{str(e)}", xbmcgui.NOTIFICATION_ERROR)
