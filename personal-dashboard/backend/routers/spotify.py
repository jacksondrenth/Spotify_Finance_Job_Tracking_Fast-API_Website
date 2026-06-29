from fastapi import APIRouter, HTTPException
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

load_dotenv()

router = APIRouter()

def get_spotify_client():
    auth_manager = SpotifyOAuth(
        client_id=os.environ["SPOTIFY_CLIENT_ID"],
        client_secret=os.environ["SPOTIFY_CLIENT_SECRET"],
        redirect_uri="http://127.0.0.1:8888/callback",
        scope="user-top-read user-read-recently-played"
    )
    token_info = auth_manager.refresh_access_token(
        os.environ["SPOTIFY_REFRESH_TOKEN"]
    )
    return spotipy.Spotify(auth=token_info["access_token"])


@router.get("/top-tracks")
def get_top_tracks(time_range: str = "medium_term", limit: int = 20):
    """
    Get user's top tracks.
    time_range: short_term (4 weeks), medium_term (6 months), long_term (all time)
    """
    try:
        sp = get_spotify_client()
        results = sp.current_user_top_tracks(
            limit=limit,
            time_range=time_range
        )
        tracks = [
            {
                "id": track["id"],
                "name": track["name"],
                "artist": track["artists"][0]["name"],
                "album": track["album"]["name"],
                "album_art": track["album"]["images"][0]["url"] if track["album"]["images"] else None,
                "spotify_url": track["external_urls"]["spotify"],
                "popularity": track["popularity"]
            }
            for track in results["items"]
        ]
        return {"tracks": tracks, "time_range": time_range}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/recently-played")
def get_recently_played(limit: int = 20):
    """Get user's recently played tracks."""
    try:
        sp = get_spotify_client()
        results = sp.current_user_recently_played(limit=limit)
        tracks = [
            {
                "id": item["track"]["id"],
                "name": item["track"]["name"],
                "artist": item["track"]["artists"][0]["name"],
                "album": item["track"]["album"]["name"],
                "album_art": item["track"]["album"]["images"][0]["url"] if item["track"]["album"]["images"] else None,
                "spotify_url": item["track"]["external_urls"]["spotify"],
                "played_at": item["played_at"]
            }
            for item in results["items"]
        ]
        return {"tracks": tracks}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats")
def get_stats():
    """Get a summary of listening stats across all time ranges."""
    try:
        sp = get_spotify_client()

        short = sp.current_user_top_tracks(limit=50, time_range="short_term")
        medium = sp.current_user_top_tracks(limit=50, time_range="medium_term")
        long = sp.current_user_top_tracks(limit=50, time_range="long_term")

        def top_artists(results):
            artists = {}
            for track in results["items"]:
                artist = track["artists"][0]["name"]
                artists[artist] = artists.get(artist, 0) + 1
            return sorted(artists.items(), key=lambda x: x[1], reverse=True)[:5]

        return {
            "short_term": {
                "top_artists": top_artists(short),
                "track_count": len(short["items"])
            },
            "medium_term": {
                "top_artists": top_artists(medium),
                "track_count": len(medium["items"])
            },
            "long_term": {
                "top_artists": top_artists(long),
                "track_count": len(long["items"])
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))