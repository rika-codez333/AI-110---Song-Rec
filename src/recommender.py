from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import math
import csv
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

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

    def recommend(self, user: UserProfile, k: int = 5, tuning_param: float = 1.0, verbose: bool = False) -> List[Song]:
        """
        Recommends top-k songs based on user profile using proximity-based content filtering.

        Args:
            user: UserProfile with preferences
            k: Number of recommendations (default 5)
            tuning_param: Gaussian k parameter (0.5=loose, 1.0=standard, 2.0=strict)
            verbose: If True, logs detailed scoring breakdown

        Returns:
            List of top-k Song objects, ranked by score
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

        if verbose:
            logger.info(f"Recommending top-{k} songs | User: genre={user.favorite_genre}, mood={user.favorite_mood}, energy={user.target_energy}")

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
            score, _ = score_song(user_prefs, song_dict, k=tuning_param, verbose=verbose)
            scored_songs.append((song, score))

        ranked = sorted(scored_songs, key=lambda x: -x[1])

        if verbose:
            logger.info(f"Top-{k} recommendations:")
            for idx, (song, score) in enumerate(ranked[:k], 1):
                logger.info(f"  {idx}. {song.title} ({song.artist}) - Score: {score:.3f}/7.9")

        return [song for song, _ in ranked[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song, tuning_param: float = 1.0, verbose: bool = False) -> str:
        """
        Explains why a song was recommended to a user.

        Args:
            user: UserProfile with preferences
            song: Song to explain
            tuning_param: Gaussian k parameter
            verbose: If True, logs the explanation

        Returns:
            String explanation with score and contributing factors
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

        score, reasons = score_song(user_prefs, song_dict, k=tuning_param, verbose=verbose)
        explanation = f"Score: {score:.3f}/7.9\n" + "\n".join(reasons)

        if verbose:
            logger.info(f"Explaining '{song.title}': {explanation.replace(chr(10), ' | ')}")

        return explanation

def load_songs(csv_path: str) -> List[Dict]:
    """Parse songs from CSV into a list of dictionaries."""
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

def score_song(user_prefs: Dict, song: Dict, k: float = 1.0, verbose: bool = False) -> Tuple[float, List[str]]:
    """Score a song against user preferences using proximity-based Gaussian similarity.

    Option C Recipe: Balanced approach with improved genre coherence
    - Genre match: +2.3 (improved) | Mood match: +1.0 | Mood mismatch: -0.5 (NEW)
    - Energy: +1.2 (reduced) | Danceability: +1.2 | Valence: +1.0
    - Tempo: +0.6 | Acousticness: +0.6
    - Max score: ~7.9

    Args:
        user_prefs: Reference song preferences (e.g., user's liked song or target profile)
        song: Song to score
        k: Gaussian tuning parameter (0.5=loose, 1.0=standard, 2.0=strict, default 1.0)
        verbose: If True, logs detailed scoring breakdown for this song

    Returns:
        (score, reasons): Score (0-7.9 max) and list of contributing factors
    """
    # Option C: Improved weights with mood penalty for better genre coherence
    weights = {
        'genre': 2.3,
        'mood': 1.0,
        'mood_mismatch': -0.5,
        'energy': 1.2,
        'danceability': 1.2,
        'valence': 1.0,
        'tempo_bpm': 0.6,
        'acousticness': 0.6,
    }

    score = 0.0
    reasons = []
    contributions = {}

    if verbose:
        logger.info(f"Scoring '{song.get('title', 'Unknown')}' | k={k} (tuning: 0.5=loose, 1.0=standard, 2.0=strict)")

    # Numerical features: Gaussian similarity (proximity-based)
    numerical_features = ['energy', 'danceability', 'valence', 'tempo_bpm', 'acousticness']
    for feature in numerical_features:
        pref_val = user_prefs.get(feature, 0.5)
        song_val = song.get(feature, 0.5)
        distance_squared = (pref_val - song_val) ** 2
        similarity = math.exp(-k * distance_squared)
        contribution = weights[feature] * similarity
        score += contribution
        contributions[feature] = (contribution, similarity, song_val, pref_val)

        if verbose:
            logger.debug(f"  {feature}: similarity={similarity:.3f}, contribution={contribution:.3f} ({song_val:.2f} vs {pref_val:.2f})")

        if similarity > 0.9:
            reasons.append(f"🎯 {feature} excellent match ({song_val:.2f} ≈ {pref_val:.2f})")
        elif similarity > 0.7:
            reasons.append(f"✓ {feature} good match ({song_val:.2f})")

    # Categorical features: exact match scoring
    mood_match = song['mood'] == user_prefs.get('mood')
    genre_match = song['genre'] == user_prefs.get('genre')

    if mood_match:
        score += weights['mood']
        contributions['mood'] = (weights['mood'], 1.0, song['mood'], user_prefs.get('mood'))
        reasons.append(f"🎭 mood matches ({song['mood']})")
        if verbose:
            logger.debug(f"  mood: MATCH +{weights['mood']:.1f}")
    else:
        mood_penalty = weights['mood_mismatch']
        score += mood_penalty
        contributions['mood'] = (mood_penalty, 0.0, song['mood'], user_prefs.get('mood'))
        reasons.append(f"⚠️ mood mismatch ({song['mood']} ≠ {user_prefs.get('mood')})")
        if verbose:
            logger.debug(f"  mood: MISMATCH {mood_penalty:.1f}")

    if genre_match:
        score += weights['genre']
        contributions['genre'] = (weights['genre'], 1.0, song['genre'], user_prefs.get('genre'))
        reasons.append(f"🎸 genre matches ({song['genre']})")
        if verbose:
            logger.debug(f"  genre: MATCH +{weights['genre']:.1f}")
    else:
        contributions['genre'] = (0.0, 0.0, song['genre'], user_prefs.get('genre'))
        if verbose:
            logger.debug(f"  genre: no match ({song['genre']} ≠ {user_prefs.get('genre')})")

    if verbose:
        logger.info(f"  ➜ Final score: {round(score, 3):.3f}/7.9 (max)")

    return round(score, 3), reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5, tuning_param: float = 1.0, verbose: bool = False) -> List[Tuple[Dict, float, List[str]]]:
    """Rank songs by score and return top-k recommendations.

    Args:
        user_prefs: User preference profile (e.g., favorite song or UserProfile as dict)
        songs: List of songs to score
        k: Number of recommendations to return (default 5)
        tuning_param: Gaussian k parameter (0.5=loose, 1.0=standard, 2.0=strict, default 1.0)
        verbose: If True, logs detailed scoring for each song

    Returns:
        List of (song_dict, score, reasons) tuples, sorted by score descending
    """
    scored_songs = []

    if verbose:
        logger.info(f"Recommending top-{k} songs for user with prefs: {user_prefs}")

    for song in songs:
        score, reasons = score_song(user_prefs, song, k=tuning_param, verbose=verbose)
        scored_songs.append((song, score, reasons))

    ranked = sorted(scored_songs, key=lambda x: -x[1])

    if verbose:
        logger.info(f"Top {k} recommendations:")
        for idx, (song, score, _) in enumerate(ranked[:k], 1):
            logger.info(f"  {idx}. {song.get('title', 'Unknown')} - {score:.3f}/7.9")

    return ranked[:k]
