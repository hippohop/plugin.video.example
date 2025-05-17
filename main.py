# -*- coding: utf-8 -*-
import sys
import xbmc
import xbmcgui
import urllib.parse
import os

def show_search_dialog():
    query = xbmcgui.Dialog().input("Hledat film na TMDb", type=xbmcgui.INPUT_ALPHANUM)
    if query:
        script = xbmcvfs.translatePath("special://home/addons/plugin.video.hrochcinema/search_launcher.py")
        xbmc.executebuiltin(f'RunScript("{script}", "{query}")')

if __name__ == '__main__':
    show_search_dialog()
   
