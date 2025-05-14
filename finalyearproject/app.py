from flask import Flask, request, jsonify
from googleapiclient.discovery import build
import os

app = Flask(__name__)

# Set your API key here
YOUTUBE_API_KEY = os.getenv("YoutubeAPIkey") or "YoutubeAPIkey"

def fetch_backing_track(song_title):
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    query = f"{song_title} guitar solo backing track"

    search_response = youtube.search().list(
        q=query,
        part="snippet",
        type="video",
        maxResults=5
    ).execute()

    for item in search_response.get("items", []):
        title = item["snippet"]["title"].lower()
        if "backing track" in title or "jam track" in title:
            video_id = item["id"]["videoId"]
            return {
                "title": item["snippet"]["title"],
                "url": f"https://www.youtube.com/watch?v={video_id}",
                "embed": f"https://www.youtube.com/embed/{video_id}"
            }

    return {"error": "No suitable backing track found"}

@app.route("/search", methods=["GET"])
def search_song():
    song = request.args.get("song")
    if not song:
        return jsonify({"error": "Missing song parameter"}), 400

    youtube_result = fetch_backing_track(song)

    # Placeholder tab and chord data (to be replaced later)
    response = {
        "song": song,
        "backing_track": youtube_result,
        "tabs": [
            "e|----0----3--0-----|",
            "B|--1---1--------3--|"
        ],
        "lyrics_chords": [
            {
                "line": "On a dark desert highway",
                "chords_above": "     Bm              F#"
            },
            {
                "line": "Cool wind in my hair",
                "chords_above": "      A               E"
            }
        ]
    }

    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)
