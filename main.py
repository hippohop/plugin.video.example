# -*- coding: utf-8 -*-
import xbmc
import xbmcgui
import os

def show_search_dialog():
    query = xbmcgui.Dialog().input("Hledat film na TMDb", type=xbmcgui.INPUT_ALPHANUM)
    if query:
        xbmc.log(f"[HROCH CINEMA] Vyhledávání přes TMDb Helper (výsledky): {query}", xbmc.LOGINFO)
        script_path = os.path.join(xbmc.translatePath("special://home/addons/plugin.video.hrochcinema/"), "search_launcher.py")
        xbmc.executebuiltin(f'RunScript("{script_path}", "{query}")')

if __name__ == '__main__':
    try:
        show_search_dialog()
    except Exception as e:
        xbmc.log(f"[HROCH CINEMA] CHYBA: {str(e)}", xbmc.LOGERROR)
        xbmcgui.Dialog().notification("CHYBA TMDb", f"{str(e)}", xbmcgui.NOTIFICATION_ERROR)
