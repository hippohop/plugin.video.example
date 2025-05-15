# Hroch Cinema – Kodi doplněk s vyhledáváním přes TMDb a přehráváním z Webshare

import sys
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import requests
from urllib.parse import quote_plus, parse_qs
import xml.etree.ElementTree as ET

ADDON = xbmcaddon.Addon()
HANDLE = int(sys.argv[1])
BASE_URL = "https://webshare.cz"
API_URL = BASE_URL + "/api/"
TMDB_API_KEY = "9ba8d27b2191a53104555851652dd1be"
TMDB_URL = "https://api.themoviedb.org/3/search/multi?query={query}&api_key=" + TMDB_API_KEY + "&language=cs"

def get_token():
    username = ADDON.getSetting("ws_username")
    password = ADDON.getSetting("ws_password")
    if not username or not password:
        xbmcgui.Dialog().notification("Hroch Cinema", "Zadej přihlášení k Webshare v nastavení", xbmcgui.NOTIFICATION_ERROR)
        return None
    salt_res = requests.post(API_URL + "salt/", data={"username_or_email": username})
    salt_xml = ET.fromstring(salt_res.content)
    if salt_xml.find("status").text != "OK":
        return None
    salt = salt_xml.find("salt").text
    import hashlib
    salted = hashlib.sha1((password + salt).encode()).hexdigest()
    digest = hashlib.md5((username + ":Webshare:" + salted).encode()).hexdigest()
    login_data = {"username_or_email": username, "password": salted, "digest": digest, "keep_logged_in": 1}
    login_res = requests.post(API_URL + "login/", data=login_data)
    login_xml = ET.fromstring(login_res.content)
    return login_xml.find("token").text if login_xml.find("status").text == "OK" else None

def search_tmdb(title):
    url = TMDB_URL.format(query=quote_plus(title))
    try:
        res = requests.get(url)
        results = res.json().get("results", [])
        return [{
            "title": r.get("title") or r.get("name"),
            "year": (r.get("release_date") or r.get("first_air_date") or "??")[:4],
            "overview": r.get("overview", ""),
            "poster": "https://image.tmdb.org/t/p/w500" + r["poster_path"] if r.get("poster_path") else ""
        } for r in results if r.get("media_type") in ("movie", "tv")]
    except:
        return []

def search_webshare(title, token):
    html = requests.get(BASE_URL + "/search?string=" + quote_plus(title), cookies={"ws_token": token}).text
    links = []
    for line in html.splitlines():
        if "/file/" in line and "href=" in line:
            for part in line.split('href="'):
                if part.startswith("/file/"):
                    url = BASE_URL + part.split('"')[0]
                    name = url.split("/")[-1]
                    links.append((url, name))
    return links

def filter_links(links):
    priority = [
        ("2160p", "cz", "dabing"),
        ("2160p", "cz"),
        ("1080p", "cz", "dabing"),
        ("1080p", "cz"),
        ("720p", "cz", "dabing"),
        ("720p", "cz"),
        ("cz",),
        ()
    ]
    for tags in priority:
        match = [l for l in links if all(t in l[1].lower() for t in tags)]
        if match:
            return match
    return []

def play_url(url):
    item = xbmcgui.ListItem(path=url)
    item.setProperty("IsPlayable", "true")
    xbmcplugin.setResolvedUrl(HANDLE, True, item)

def show_results(results):
    for result in results:
        list_item = xbmcgui.ListItem(label=f"{result['title']} ({result['year']})")
        list_item.setInfo("video", {"title": result["title"], "plot": result["overview"], "year": result["year"]})
        if result["poster"]:
            list_item.setArt({"poster": result["poster"]})
        url = f"{sys.argv[0]}?action=webshare&title={quote_plus(result['title'])}"
        xbmcplugin.addDirectoryItem(HANDLE, url, list_item, isFolder=False)
    xbmcplugin.endOfDirectory(HANDLE)

def router():
    args = dict(parse_qs(sys.argv[2][1:]))
    action = args.get("action", [""])[0]

    if action == "webshare":
        title = args.get("title", [""])[0]
        token = get_token()
        if not token:
            return
        links = search_webshare(title, token)
        matches = filter_links(links)
        if not matches:
            xbmcgui.Dialog().notification("Hroch Cinema", "Nenalezeny žádné vhodné releasy", xbmcgui.NOTIFICATION_INFO)
            return
        if len(matches) == 1:
            play_url(matches[0][0])
        else:
            names = [name for url, name in matches]
            index = xbmcgui.Dialog().select("Vyberte releas", names)
            if index >= 0:
                play_url(matches[index][0])
    else:
        keyboard = xbmc.Keyboard('', 'Zadej název filmu/seriálu')
        keyboard.doModal()
        if not keyboard.isConfirmed():
            return
        title = keyboard.getText()
        results = search_tmdb(title)
        if not results:
            xbmcgui.Dialog().notification("Hroch Cinema", "Žádné výsledky", xbmcgui.NOTIFICATION_INFO)
            return
        show_results(results)

if __name__ == "__main__":
    router()
