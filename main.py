import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import sys

from utils import info, debug, error, warn
import settings

addon_handle = int(sys.argv[1])
base_url = sys.argv[0]
addon = xbmcaddon.Addon()
addon_settings = settings.load()
stream_urls = addon_settings.STREAM_URLS.split(",")
stream_names = addon_settings.STREAM_NAMES.split(",")
# fill the stream names with the default name if the number of names is less than the number of urls
if len(stream_names) < len(stream_urls):
    stream_names += ["stream"] * (len(stream_urls) - len(stream_names))

# Define RTSP streams
streams = [{"name": stream_names[i], "url": stream_urls[i]} for i in range(len(stream_urls))]
info(streams)


def list_streams()->None:
    """Lists the RTSP streams in the Kodi interface."""
    for stream in streams:
        list_item = xbmcgui.ListItem(label=stream["name"])
        list_item.setProperty("IsPlayable", "true")
        xbmcplugin.addDirectoryItem(
            handle=addon_handle,
            url=f"{base_url}?action=play&url={stream['url']}",
            listitem=list_item,
            isFolder=False,
        )
    # Add an option to play all streams
    list_item = xbmcgui.ListItem(label="Play All Streams")
    xbmcplugin.addDirectoryItem(
        handle=addon_handle,
        url=f"{base_url}?action=play_all",
        listitem=list_item,
        isFolder=False,
    )
    xbmcplugin.endOfDirectory(addon_handle)

def play_stream(url):
    """Plays the specified RTSP stream."""
    play_item = xbmcgui.ListItem(path=url)
    xbmcplugin.setResolvedUrl(addon_handle, True, listitem=play_item)

def play_all_streams():
    """Cycles through all RTSP streams with a 30-second wait time between each, looping until stopped."""
    player = xbmc.Player()
    while not player.isPlaying():
        for stream in streams:
            debug(f"Playing stream: {stream['name']}")
            player.play(stream["url"])
            xbmc.sleep(addon_settings.PLAY_TIME*1000)  # Wait for 30 seconds (30000 milliseconds)
            if not player.isPlaying():
                debug("Player stopped")
                return
    info("leaving play_all_streams")
        
def router(paramstring):
    """Route the request based on the parameters."""
    if not paramstring:
        list_streams()
        return
    params = {}
    for pair in paramstring.split('&'):
        if '=' in pair:
            key, value = pair.split('=', 1)
            params[key] = value
        else:
            error(f"Invalid parameter: {pair}")
    action = params.get('action')
    url = params.get('url')

    if action == 'play' and url:
        play_stream(url)
    elif action == 'play_all':
        play_all_streams()
    else:
        list_streams()

def main():
    if addon.getSettingBool(settings.SettingsIds._FIRST_TIME.name):
        info('First time launch')
        addon.openSettings()
        addon.setSettingBool(settings.SettingsIds._FIRST_TIME.name, False)

    info(sys.argv)
    if len(sys.argv) > 2:
        router(sys.argv[2][1:])  # Strip leading '?'
    else:
        list_streams()


if __name__ == "__main__":
    main()