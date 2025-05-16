# -*- coding: utf-8 -*-
import xbmcplugin
import xbmcgui
import xbmcaddon
import xbmc
import sys
import urllib.parse
import requests
from tmdbhelper import TMDB

addon = xbmcaddon.Addon()
addon_handle = int(sys.argv[1])
base_url = sys.argv[0]
args = sys.argv[2]

tmdb = TMDB('movie', language='cs')

def log(msg):
    xbmc.log(f"[HROCH CINEMA] {msg}", xbmc.LOGNOTICE)

def build_url(query):
    return base_url + '?' + urllib.parse.urlencode(query)

def get_search_query():
    return xbmcgui.Dialog().input("Zadej název filmu", type=xbmcgui.INPUT_ALPHANUM)

def search_tmdb(query):
    log(f"Hledám na TMDb: {query}")
    return tmdb.search(query)

def search_webshare(title):
    log(f"Hledám na Webshare: {title}")
    session = requests.Session()
    username = addon.getSetting("ws_user")
    password = addon.getSetting("ws_pass")
    if not username or not password:
        xbmcgui.Dialog().notification("Webshare", "Chybí přihlašovací údaje", xbmcgui.NOTIFICATION_ERROR)
        return []
    try:
        login_data = {"username": username, "password": password}
        r = session.post("https://webshare.cz/api/login/", data=login_data)
        r.raise_for_status()
        token = r.json().get("token")
        if not token:
            raise Exception("Přihlášení selhalo")
        headers = {"Authorization": f"Bearer {token}"}
        search_url = f"https://webshare.cz/api/file/find?query={urllib.parse.quote(title)}"
        r = session.get(search_url, headers=headers)
        r.raise_for_status()
        return r.json().get("data", [])
    except Exception as e:
        log(f"Chyba při hledání na Webshare: {str(e)}")
        xbmcgui.Dialog().notification("Webshare", f"Chyba: {e}", xbmcgui.NOTIFICATION_ERROR)
        return []

def filter_results(files):
    log("Filtruji výsledky podle kvality a jazyka...")
    filtered = []
    for f in files:
        name = f.get("name", "").lower()
        if any(q in name for q in ["2160p", "1080p"]) and any(lang in name for lang in ["cz", "czech"]):
            filtered.append(f)
    return filtered if filtered else files

def list_tmdb_results(results):
    for result in results:
        title = result.get("title") or result.get("name")
        year = result.get("release_date", "")[:4]
        poster = result.get("poster_path", "")
        list_item = xbmcgui.ListItem(label=f"{title} ({year})")
        list_item.setArt({"thumb": f"https://image.tmdb.org/t/p/w500{poster}"})
        url = build_url({"action": "select_release", "title": title})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=list_item, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)

def list_releases(releases):
    for file in releases:
        name = file.get("name")
        link = file.get("link")
        list_item = xbmcgui.ListItem(label=name)
        list_item.setProperty("IsPlayable", "true")
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=link, listitem=list_item, isFolder=False)
    xbmcplugin.endOfDirectory(addon_handle)

def router(params):
    log(f"Routing parametry: {params}")
    if not params:
        query = get_search_query()
        if not query:
            return
        results = search_tmdb(query)
        list_tmdb_results(results)
    elif params.get("action") == "select_release":
        title = params.get("title")
        releases = search_webshare(title)
        filtered = filter_results(releases)
        list_releases(filtered)

# Spuštění doplňku
log("Spouštím doplněk Hroch Cinema")
params = dict(urllib.parse.parse_qsl(args[1:]))
router(params)
