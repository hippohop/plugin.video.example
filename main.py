import xbmc
import xbmcaddon
import xbmcgui
import urllib.parse
import urllib.request
import http.cookiejar
import json

ADDON = xbmcaddon.Addon()
USERNAME = ADDON.getSetting("ws_user")
PASSWORD = ADDON.getSetting("ws_pass")

BASE_URL = "https://webshare.cz"
API_URL = f"{BASE_URL}/api/"

def login():
    data = urllib.parse.urlencode({'username': USERNAME, 'password': PASSWORD}).encode()
    req = urllib.request.Request(API_URL + "login/", data=data)
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    try:
        with opener.open(req) as response:
            result = json.loads(response.read())
            if result.get("status") == "OK":
                return opener
            else:
                xbmcgui.Dialog().ok("Chyba", "Přihlášení na Webshare selhalo.")
                return None
    except Exception as e:
        xbmcgui.Dialog().ok("Chyba připojení", str(e))
        return None

def run():
    kb = xbmc.Keyboard('', 'Zadej název filmu')
    kb.doModal()
    if not kb.isConfirmed():
        return
    query = kb.getText()
    if not query:
        return

    opener = login()
    if not opener:
        return

    # Zatím jen oznámení
    xbmcgui.Dialog().ok("Webshare Search", f"Byl by spuštěn dotaz: {query}")

if __name__ == "__main__":
    run()
