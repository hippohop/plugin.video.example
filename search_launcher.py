import xbmc
import sys
import urllib.parse

if len(sys.argv) > 1:
    query = sys.argv[1]
    encoded_query = urllib.parse.quote_plus(query)
    url = f'plugin://plugin.video.themoviedb.helper/?action=search_movies&query={encoded_query}'
    xbmc.executebuiltin(f'ActivateWindow(Videos,"{url}",return)')
