# Mixtape Editor
- Written by Shiloh Stuart
- Technical homework for Highspot

## Use
- Run the `mixtape_editor.py` script with three arguments: input file, change file, and output file. For example, on windows: `py ./mixtape_editor.py mixtape.json changes.json mixtape_out.json`
  - The input file should be in the format provided in `mixtape.json` by Highspot for this assignment.
  - The change file should be in the following format:
  ```json
    {
        "add_to_playlist": [
            {
                "playlist_id": "1",
                "song_ids": ["1", "2", "3"]
            }
        ],
        "new_playlist": [
            {
                "user_id": "1",
                "song_ids": ["1", "2", "3"]
            }
        ],
        "remove_playlist": ["1", "2", "3"]
    }
  ``` 
  - The output file will be written in the same format as `mixtape.json`

## Scalability
### Large mixtape files
- Iterating over large numbers of users, songs, or playlists to build dicts could add a lot of time to the process. If `mixtape.json` is very large, it would be better to build a `Mixtape` object with a custom decoder to make this more efficient.

### Large change files
- Iterating over a large number of `song_ids` included in `add_to_playlist` or `new_playlist` instructions could be a big efficiency issue. One way to speed this up would be to gather a set of all `song_ids` included in all instructions, check them all, and make a list of invalid ids. Then, when processing the changes, iterate over the set of invalid ids and use `remove_all` to remove any invalid ids from the list of `song_ids` in the instruction.
