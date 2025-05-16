import sys

log("Spouštím doplněk Hroch Cinema")
params = dict(urllib.parse.parse_qsl(sys.argv[2][1:]))
router(params)

def router(params):
    log(f"Routing parametry: {params}")
    if not params:
        # Zobraz položku pro vyhledávání jako adresářovou položku
        url = build_url({"action": "search"})
        list_item = xbmcgui.ListItem(label="🔍 Vyhledat film")
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=list_item, isFolder=True)
        xbmcplugin.endOfDirectory(addon_handle)
        return

    if params.get("action") == "search":
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

log("Spouštím doplněk Hroch Cinema")
params = dict(urllib.parse.parse_qsl(args[1:]))
router(params)
