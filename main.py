# Hroch Cinema – základní main.py pro Kodi doplněk

import sys
import xbmc
import xbmcgui
import xbmcplugin
from urllib.parse import parse_qs

# Plugin handle
HANDLE = int(sys.argv[1])

def show_search():
    """
    Zobrazí dialog pro zadání názvu filmu a vyvolá zpracování vyhledávání (placeholder)
    """
    keyboard = xbmc.Keyboard('', 'Zadej název filmu nebo seriálu')
    keyboard.doModal()
    if not keyboard.isConfirmed():
        return
    title = keyboard.getText()
    xbmcgui.Dialog().ok("Hroch Cinema", f"Hledám: {title}")
    # Zde bude napojení na TMDb + Webshare

def router():
    """
    Směrovací funkce – zatím vždy spustí hledání
    """
    args = dict(parse_qs(sys.argv[2][1:]))
    if args.get("action", [""])[0] == "search":
        show_search()
    else:
        show_search()

if __name__ == "__main__":
    router()
