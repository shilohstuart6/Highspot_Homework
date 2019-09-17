import argparse
import json

def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description='Edit a mixtape')
    parser.add_argument("input_file", type=str)
    parser.add_argument("change_file", type=str)
    parser.add_argument("output_file", type=str)
    args = parser.parse_args()

    # Read mixtape and change file
    with open(args.input_file, 'r') as f:
        mixtape = json.load(f)
    with open(args.change_file, 'r') as f:
        changes = json.load(f)

    # Build mixtape dicts for easy reference by id
    playlists = {}
    users = {}
    songs = {}
    for playlist in mixtape["playlists"]:
        playlists[playlist["id"]] = {
            "id": playlist["id"], 
            "user_id": playlist["user_id"], 
            "song_ids": playlist["song_ids"]}
    for user in mixtape["users"]:
        users[user["id"]] = {
            "id": user["id"],
            "name": user["name"]
        }
    for song in mixtape["songs"]:
        songs[song["id"]] = {
            "id": song["id"],
            "artist": song["artist"],
            "title": song["title"]
        }

    # Add songs to existing playlists
    for inst in changes["add_to_playlist"]:
        playlist = playlists.get(inst["playlist_id"])
        # Check the playlist exists
        if not playlist:
            print("playlist id " + inst["playlist_id"] + " not found.")
            continue
        # Check the song ids exist
        for song_id in inst["song_ids"]:
            if not songs.get(song_id):
                print("song id " + song_id + " not found")  
                inst["song_ids"].remove(song_id)
        # Add the song ids to the playlist
        playlist["song_ids"] = playlist["song_ids"] + inst["song_ids"]                

    # Add new playlists
    for inst in changes["new_playlist"]:
        #Check the user exists
        if not users.get(inst["user_id"]):
            print("user id " + inst["user_id"] + " not found")
            continue
        # Check the song ids exist
        for song_id in inst["song_ids"]:
            if not songs.get(song_id):
                print("song id " + song_id + " not found")
                inst["song_ids"].remove(song_id)
        if len(inst["song_ids"]) == 0:
            print("playlist must have at least one song")
            continue
        # Get a new playlist id
        playlist_id = new_playlist_id(playlists)
        # Create the playlist
        playlists[playlist_id] = {
            "id": playlist_id, 
            "user_id": inst["user_id"],
            "song_ids": inst["song_ids"]}

    # Remove deleted playlists
    for playlist_id in changes["remove_playlist"]:
        playlist = playlists.get(playlist_id)
        if not playlist:
            print("playlist id " + playlist_id + " not found")
            continue
        playlists[playlist_id] = {}

    # Update mixtape playlists
    mixtape["playlists"] = []
    for playlist in playlists.values():
        mixtape["playlists"].append(playlist)

    # Write mixtape to output file
    with open(args.output_file, 'w') as f:
        json.dump(mixtape, f)

def new_playlist_id(playlists):
    taken_ids = set()
    for playlist_id in playlists.keys():
        taken_ids.add(int(playlist_id))

    playlist_id = 1
    while playlist_id in taken_ids:
        playlist_id += 1
    return str(playlist_id)

if __name__ == '__main__':
    main()