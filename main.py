
import xbmcplugin
import xbmcgui
import xbmcaddon
import sys
import urllib.parse
from tmdbhelper import TMDB
import requests
import re

addon = xbmcaddon.Addon()
addon_handle = int(sys.argv[1])
base_url = sys.argv[0]
args = sys.argv[2]

# TMDb Helper
tmdb = TMDB('movie', language='cs')

def build_url(query):
    return base_url + '?' + urllib.parse.urlencode(query)

def get_search_query():
    keyboard = xbmcgui.Dialog().input("Zadej název filmu", type=xbmcgui.INPUT_ALPHANUM)
    return keyboard

def search_tmdb(query):
    results = tmdb.search(query)
    return results

def search_webshare(title):
    session = requests.Session()
    username = addon.getSetting('ws_user')
    password = addon.getSetting('ws_pass')

    login_data = {
        'username': username,
        'password': password
    }

    login_response = session.post('https://webshare.cz/api/login/', data=login_data)
    token = login_response.json().get('token')

    headers = {
        'Authorization': f'Bearer {token}'
    }

    search_response = session.get(f'https://webshare.cz/api/file/find?query={urllib.parse.quote(title)}', headers=headers)
    files = search_response.json().get('data', [])
    return files

def filter_results(files):
    preferred = []
    for f in files:
        name = f.get('name', '').lower()
        if any(res in name for res in ['2160p', '1080p']) and ('cz' in name or 'czech' in name):
            preferred.append(f)
    return preferred if preferred else files

def list_tmdb_results(results):
    for result in results:
        title = result.get('title') or result.get('name')
        year = result.get('release_date', '')[:4]
        poster = result.get('poster_path', '')
        tmdb_id = result.get('id')

        list_item = xbmcgui.ListItem(label=f"{title} ({year})")
        list_item.setArt({'thumb': f"https://image.tmdb.org/t/p/w500{poster}"})

        url = build_url({'action': 'select_release', 'title': title})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=list_item, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)

def list_releases(releases):
    for file in releases:
        name = file.get('name')
        url = file.get('link')
        list_item = xbmcgui.ListItem(label=name)
        list_item.setProperty('IsPlayable', 'true')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=list_item, isFolder=False)
    xbmcplugin.endOfDirectory(addon_handle)

def router(params):
    if not params:
        query = get_search_query()
        if not query:
            return
        results = search_tmdb(query)
        list_tmdb_results(results)
    elif params.get('action') == 'select_release':
        title = params.get('title')
        files = search_webshare(title)
        filtered = filter_results(files)
        list_releases(filtered)

if __name__ == '__main__':
    param_dict = dict(urllib.parse.parse_qsl(args[1:]))
    router(param_dict)
