# -*- coding: utf-8 -*-
import sys
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import urllib.parse

addon = xbmcaddon.Addon()
addon_handle = int(sys.argv[1])

def log(msg):
    xbmc.log(f"[HROCH CINEMA] {msg}", xbmc.LOGNOTICE)

def build_url(query):
    return sys.argv[0] + '?' + urllib.parse.urlencode(query)

def router():
    log("Spouštím router...")
    keyboard = xbmcgui.Dialog().input("Zadej název filmu", type=xbmcgui.INPUT_ALPHANUM)
    if keyboard:
        log(f"Zadán hledaný výraz: {keyboard}")
        xbmcgui.Dialog().ok("Výsledek", f"Hledal jsi: {keyboard}")
    else:
        log("Uživatel nezadal žádný text.")

if __name__ == '__main__':
    log("Startuji doplněk Hroch Cinema")
    router()
