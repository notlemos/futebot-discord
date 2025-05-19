from cachetools import TTLCache, cached
import pylast
import os

cacheAlbum = TTLCache(maxsize=128, ttl=300)

cacheRecentTracks = TTLCache(maxsize=50, ttl=15)


API_KEY = os.getenv('APILASTFM')
API_SECRET = os.getenv('APILASTFMSECRET')




@cached(cacheAlbum)
def topalbums():
    network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET)
    user = network.get_user('Leemoos')

    top_albums = user.get_top_albums(limit=10) 
    all_data = []
    
    for item in top_albums:
        album = item.item
        cover_url = album.get_cover_image()
        if cover_url:
            cover_hd = cover_url.replace("/300x300/", "/600x600/")
        playcount = item.weight
    
        all_data.append({
            'title': album.title,
            'artist': album.artist.name,
            'contagem': playcount,
            'cover': cover_hd
        })
   
    return all_data
@cached(cacheAlbum)
def toptracks(user):
    network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET)

    user = network.get_user(user)
    all_data = []
    
    top_tracks = user.get_top_tracks(limit=10)

    for item in top_tracks:
        track = item.item 
        
        title = track.title
        artist = track.artist.name
        playcount = item.weight
        all_data.append({
            'title': title,
            'artist': artist,
            'playcount': playcount
        })
    
    return all_data
    


