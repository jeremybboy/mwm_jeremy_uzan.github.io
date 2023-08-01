import json
from flask import Flask, render_template, request

app = Flask(__name__)

def load_data():
    music_data = "music_data_set_(1).json"
    with open(music_data, "r") as file:
        data = json.load(file)
    return data

def reorganize_data(data):
    new_data = {
        "tracks": [],
        "recommendations": []
    }

    for track in data["tracks"]:
        new_track = {
            "track_id": int(track.get("track_id", 0)),
            "title": track.get("title", ""),
            "artist": track.get("artist", ""),
            "album": track.get("album", ""),
            "year": int(track.get("year", 0)),
            "tempo": int(track.get("tempo", 0)),
            "rhythm": track.get("rhythm", ""),
            "genre": track.get("genre", "")
        }
        new_data["tracks"].append(new_track)

    for rec in data["recommendations"]:
        new_rec = {
            "track_id": int(rec.get("track_id", 0)),
            "recommendations": [int(track_id) for track_id in rec.get("recommendations", [])]
        }
        new_data["recommendations"].append(new_rec)

    return new_data

def show_tracks(data):
    for track in data["tracks"]:
        print(f"{track['track_id']}: {track['title']} - {track['artist']}")

def generate_recommendations(data, track_id):
    recommendations = next(
        (rec for rec in data["recommendations"] if rec["track_id"] == track_id),
        None
    )
    if recommendations:
        recommendation_ids = recommendations["recommendations"]
        recommended_tracks = [
            track for track in data["tracks"] if track["track_id"] in recommendation_ids
        ]
        return recommended_tracks
    return []

@app.route('/', methods=['GET', 'POST'])
def index():
    data = load_data()
    data = reorganize_data(data)
    
    if request.method == 'POST':
        selected_track_id = int(request.form['track'])
        recommendations = generate_recommendations(data, selected_track_id)
        return render_template('index.html', tracks=data["tracks"], recommendations=recommendations, selected_track_id=selected_track_id)
    
    return render_template('index.html', tracks=data["tracks"])

if __name__ == "__main__":
    app.run(debug=True)
