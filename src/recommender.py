from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import math
import csv

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    preferred_valence: float
    preferred_danceability: float
    preferred_tempo_bpm: float
    preferred_acousticness: float

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """
        Recommends top-k songs based on user profile using proximity-based content filtering.
        """
        user_prefs = {
            'genre': user.favorite_genre,
            'mood': user.favorite_mood,
            'energy': user.target_energy,
            'valence': user.preferred_valence,
            'danceability': user.preferred_danceability,
            'tempo_bpm': user.preferred_tempo_bpm,
            'acousticness': user.preferred_acousticness,
        }

        scored_songs = []
        for song in self.songs:
            song_dict = {
                'id': song.id,
                'title': song.title,
                'artist': song.artist,
                'genre': song.genre,
                'mood': song.mood,
                'energy': song.energy,
                'tempo_bpm': song.tempo_bpm,
                'valence': song.valence,
                'danceability': song.danceability,
                'acousticness': song.acousticness,
            }
            score, _ = score_song(user_prefs, song_dict)
            scored_songs.append((song, score))

        ranked = sorted(scored_songs, key=lambda x: -x[1])
        return [song for song, _ in ranked[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """
        Explains why a song was recommended to a user.
        """
        user_prefs = {
            'genre': user.favorite_genre,
            'mood': user.favorite_mood,
            'energy': user.target_energy,
            'valence': user.preferred_valence,
            'danceability': user.preferred_danceability,
            'tempo_bpm': user.preferred_tempo_bpm,
            'acousticness': user.preferred_acousticness,
        }

        song_dict = {
            'id': song.id,
            'title': song.title,
            'artist': song.artist,
            'genre': song.genre,
            'mood': song.mood,
            'energy': song.energy,
            'tempo_bpm': song.tempo_bpm,
            'valence': song.valence,
            'danceability': song.danceability,
            'acousticness': song.acousticness,
        }

        score, reasons = score_song(user_prefs, song_dict)
        explanation = f"Score: {score:.3f}\n" + "\n".join(reasons)
        return explanation

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file and returns list of song dicts.
    """
    songs = []
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            song = {
                'id': int(row['id']),
                'title': row['title'],
                'artist': row['artist'],
                'genre': row['genre'],
                'mood': row['mood'],
                'energy': float(row['energy']),
                'tempo_bpm': float(row['tempo_bpm']),
                'valence': float(row['valence']),
                'danceability': float(row['danceability']),
                'acousticness': float(row['acousticness']),
            }
            songs.append(song)
    return songs

def score_song(user_prefs: Dict, song: Dict, k: float = 1.0) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences using proximity-based Gaussian similarity.

    Args:
        user_prefs: Reference song preferences (e.g., user's liked song or target profile)
        song: Song to score
        k: Gaussian tuning parameter (higher = stricter matching, default 1.0)

    Returns:
        (score, reasons): Score (0-1) and list of contributing factors
    """
    # Default weights (hybrid model)
    weights = {
        'energy': 0.25,
        'valence': 0.20,
        'danceability': 0.20,
        'mood': 0.15,
        'tempo_bpm': 0.10,
        'genre': 0.05,
        'acousticness': 0.05,
    }

    score = 0.0
    reasons = []

    # Numerical features: Gaussian similarity (proximity-based)
    numerical_features = ['energy', 'valence', 'danceability', 'tempo_bpm', 'acousticness']
    for feature in numerical_features:
        pref_val = user_prefs.get(feature, 0.5)
        song_val = song.get(feature, 0.5)
        distance_squared = (pref_val - song_val) ** 2
        similarity = math.exp(-k * distance_squared)
        contribution = weights[feature] * similarity
        score += contribution

        if similarity > 0.9:
            reasons.append(f"🎯 {feature} excellent match ({song_val:.2f} ≈ {pref_val:.2f})")
        elif similarity > 0.7:
            reasons.append(f"✓ {feature} good match ({song_val:.2f})")

    # Categorical features: exact match scoring
    if song['mood'] == user_prefs.get('mood'):
        score += weights['mood']
        reasons.append(f"🎭 mood matches ({song['mood']})")

    if song['genre'] == user_prefs.get('genre'):
        score += weights['genre']
        reasons.append(f"🎸 genre matches ({song['genre']})")

    return round(score, 3), reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, List[str]]]:
    """
    Ranks all songs by score and returns top-k recommendations.

    Args:
        user_prefs: User preference profile (e.g., favorite song or UserProfile as dict)
        songs: List of songs to score
        k: Number of recommendations to return (default 5)

    Returns:
        List of (song_dict, score, reasons) tuples, sorted by score descending
    """
    scored_songs = []

    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored_songs.append((song, score, reasons))

    ranked = sorted(scored_songs, key=lambda x: -x[1])
    return ranked[:k]
