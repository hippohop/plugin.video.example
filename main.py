
# Hroch Cinema – Kodi doplněk s vyhledáváním přes TMDb a přehráváním z Webshare

import sys
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import requests
from urllib.parse import quote_plus, parse_qs
import xml.etree.ElementTree as ET

try:
    from thetmdb import TMDbHelper
except ImportError:
    xbmcgui.Dialog().notification("Hroch Cinema", "Chybí doplněk TMDb Helper!", xbmcgui.NOTIFICATION_ERROR)
    sys.exit()

tmdb = TMDbHelper()
tmdb.language = "cs"

ADDON = xbmcaddon.Addon()
HANDLE = int(sys.argv[1])
BASE_URL = "https://webshare.cz"
API_URL = BASE_URL + "/api/"

def log(msg, level=xbmc.LOGDEBUG):
    xbmc.log(f"[HrochCinema] {msg}", level)

def get_token():
    username = ADDON.getSetting("ws_user")
    password = ADDON.getSetting("ws_pass")
    if not username or not password:
        log("Chybí přihlašovací údaje Webshare", xbmc.LOGERROR)
        return None
    response = requests.post(API_URL + "login/", data={"username": username, "password": password})
    result = response.json()
    return result.get("token")

def search_tmdb(query):
    results = tmdb.search(query)
    if not results:
        log(f"Nic nenalezeno pro: {query}", xbmc.LOGWARNING)
        return []
    log(f"Nalezeno výsledků: {len(results)}", xbmc.LOGINFO)
    return results

def search_webshare(title, token):
    response = requests.get(API_URL + "file/find/", params={"search": title, "show": "all", "page": 1, "limit": 50, "wst": token})
    return response.json().get("files", [])

def filter_results(results):
    filtered = []
    for r in results:
        name = r.get("name", "").lower()
        if any(res in name for res in ["2160p", "1080p"]) and ("cz" in name or "czech" in name):
            filtered.append(r)
    return filtered

def select_result(results):
    labels = [r.get("name", "Neznámý soubor") for r in results]
    index = xbmcgui.Dialog().select("Vyber releas", labels)
    return results[index] if index >= 0 else None

def play_file(file_info, token):
    file_id = file_info.get("ident")
    if not file_id:
        log("Soubor nemá ID", xbmc.LOGERROR)
        return
    stream_url = f"https://webshare.cz/api/file/link/?ident={file_id}&wst={token}"
    response = requests.get(stream_url)
    link = response.json().get("link")
    if not link:
        log("Nelze získat odkaz ke streamu", xbmc.LOGERROR)
        return
    li = xbmcgui.ListItem(path=link)
    xbmcplugin.setResolvedUrl(HANDLE, True, li)

def run():
    query = xbmcgui.Dialog().input("Zadej název filmu")
    if not query:
        return

    results = search_tmdb(query)
    if not results:
        return

    first = results[0]
    title = first.get("title", "")
    log(f"Vybraný titul z TMDb: {title}")

    token = get_token()
    if not token:
        return

    releases = search_webshare(title, token)
    log(f"Nalezeno {len(releases)} releasů na Webshare")

    filtered = filter_results(releases)
    if not filtered:
        xbmcgui.Dialog().notification("Hroch Cinema", "Nenalezeny releasy s CZ a požadovanou kvalitou", xbmcgui.NOTIFICATION_INFO)
        return

    selected = select_result(filtered)
    if selected:
        play_file(selected, token)

if __name__ == "__main__":
    run()
