"""Tests for playlist generation and management."""

from src.playlist import Playlist, PlaylistGenerator


def test_playlist_add_song():
    """Test adding songs to a playlist."""
    playlist = Playlist(name="Test Playlist", theme="custom")
    song = {"title": "Test Song", "artist": "Test Artist", "genre": "pop", "energy": 0.7}

    playlist.add_song(song, score=8.5)

    assert len(playlist.songs) == 1
    assert playlist.songs[0]["title"] == "Test Song"


def test_playlist_remove_song():
    """Test removing songs from a playlist."""
    playlist = Playlist(name="Test Playlist", theme="custom")
    song1 = {"title": "Song 1", "artist": "Artist 1", "genre": "pop", "energy": 0.7}
    song2 = {"title": "Song 2", "artist": "Artist 2", "genre": "rock", "energy": 0.8}

    playlist.add_song(song1)
    playlist.add_song(song2)

    assert len(playlist.songs) == 2
    playlist.remove_song(0)
    assert len(playlist.songs) == 1
    assert playlist.songs[0]["title"] == "Song 2"


def test_playlist_get_stats():
    """Test getting playlist statistics."""
    playlist = Playlist(name="Test Playlist", theme="custom")
    song1 = {"title": "Song 1", "artist": "Artist 1", "genre": "pop", "mood": "happy", "energy": 0.8, "danceability": 0.7}
    song2 = {"title": "Song 2", "artist": "Artist 2", "genre": "rock", "mood": "intense", "energy": 0.6, "danceability": 0.5}

    playlist.add_song(song1)
    playlist.add_song(song2)

    stats = playlist.get_stats()
    assert stats["song_count"] == 2
    assert "pop" in stats["genres"]
    assert "rock" in stats["genres"]
    assert stats["avg_energy"] > 0


def test_generate_themed_playlist():
    """Test themed playlist generation."""
    songs = [
        {"title": "High Energy", "artist": "Test", "genre": "pop", "mood": "happy", "energy": 0.9, "danceability": 0.8, "acousticness": 0.2},
        {"title": "Low Energy", "artist": "Test", "genre": "ambient", "mood": "calm", "energy": 0.1, "danceability": 0.2, "acousticness": 0.8},
    ]

    playlist = PlaylistGenerator.generate_themed_playlist(songs, "workout")

    assert playlist is not None
    assert playlist.theme == "workout"
    assert len(playlist.songs) > 0
