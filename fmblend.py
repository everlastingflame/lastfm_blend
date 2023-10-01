import requests

def get_top_songs(api_key, username, period):
    url = 'http://ws.audioscrobbler.com/2.0/'
    params = {
        'method': 'user.gettoptracks',
        'user': username,
        'period': period,
        'api_key': api_key,
        'format': 'json',
        'limit': 100
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        tracks = response.json()['toptracks']['track']
        return [(track['name'], track['artist']['name']) for track in tracks]  
    else:
        return f"Error with status code: {response.status_code}"

    
def get_similar(api_key, track, artist):
    url = 'http://ws.audioscrobbler.com/2.0/'
    params = {
        'method': 'track.getSimilar',
        'track': track,
        'artist': artist,  # Add artist parameter
        'api_key': api_key,
        'format': 'json',   
        'limit': 5
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        tracks = response.json().get('similartracks', {}).get('track', [])
        return [(track['name'], track['artist']['name']) for track in tracks]
    else:
        return f"Error with status code: {response.status_code}"



# Usage
api_key = '345ec1ae02d615b7a7fadbece710e91b'
username = input("Enter a last.fm username: ")
username2 = input("Enter a second last.fm username:")
period = input("Enter the period of time you want to see your top songs for (7day, 1month, 3month, 6month, 12month, overall): ")

top_songs_user1 = get_top_songs(api_key, username, period)
top_songs_user2 = get_top_songs(api_key, username2, period)

top_similar_songs1 = []
top_similar_songs2 = []

for song, artist in top_songs_user1:
    top_similar_songs1.extend(get_similar(api_key, song, artist))

for song, artist in top_songs_user2:
    top_similar_songs2.extend(get_similar(api_key, song, artist))



recommended_tracks = top_similar_songs1 + top_similar_songs2

final_recommendations = [track for track in recommended_tracks if track not in (top_songs_user1 + top_songs_user2)]


playlist = []

added_tracks = set()

limit = min(25, len(top_songs_user1), len(top_songs_user2), len(final_recommendations))
for i in range(limit):
    # Check if the track from top_songs_user1[i] is not in added_tracks
    if top_songs_user1[i] not in added_tracks:
        playlist.append(top_songs_user1[i])  # Add the track to the playlist
        added_tracks.add(top_songs_user1[i])  # Add the track to added_tracks
    
    # Do the same for top_songs_user2[i]
    if top_songs_user2[i] not in added_tracks:
        playlist.append(top_songs_user2[i])
        added_tracks.add(top_songs_user2[i])
    
    # And for final_recommendations[i]
    if final_recommendations[i] not in added_tracks:
        playlist.append(final_recommendations[i])
        added_tracks.add(final_recommendations[i])


    

for track_name, artist_name in playlist:
    print(f"{track_name} - {artist_name}")

