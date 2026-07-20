"""
Unit tests for the Music Recommender System.
Tests core functionality: scoring, recommendations, diversity penalties, and strategies.
"""

import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.recommender import (
    load_songs, score_song, recommend_songs,
    BalancedStrategy, EnergyFocusedStrategy, GenreFirstStrategy,
    MoodFirstStrategy, QualityFirstStrategy, PopularityDrivenStrategy
)
from src.main import apply_diversity_penalty


class TestSongLoading(unittest.TestCase):
    """Test data loading and song validation."""

    def test_load_songs_returns_list(self):
        """Songs loaded successfully from CSV."""
        songs = load_songs("data/songs.csv")
        self.assertIsInstance(songs, list)
        self.assertGreater(len(songs), 0)

    def test_songs_have_required_fields(self):
        """Each song has required attributes."""
        songs = load_songs("data/songs.csv")
        required_fields = {'title', 'artist', 'genre', 'mood', 'energy',
                          'valence', 'danceability', 'tempo_bpm', 'acousticness'}
        for song in songs:
            for field in required_fields:
                self.assertIn(field, song, f"Song missing {field}")


class TestScoringCore(unittest.TestCase):
    """Test individual song scoring logic."""

    def setUp(self):
        self.songs = load_songs("data/songs.csv")

    def test_score_song_genre_match(self):
        """Genre match awards ~2.3 points."""
        song = {'title': 'Test', 'artist': 'Test', 'genre': 'pop', 'mood': 'happy',
                'energy': 0.5, 'valence': 0.5, 'danceability': 0.5, 'tempo_bpm': 120, 'acousticness': 0.5}
        prefs = {'genre': 'pop', 'mood': 'happy', 'energy': 0.5, 'valence': 0.5,
                 'danceability': 0.5, 'tempo': 120, 'acousticness': 0.5}
        score, _ = score_song(song, prefs)
        self.assertGreater(score, 2.0)

    def test_score_song_genre_mismatch(self):
        """Genre mismatch vs match shows lower score."""
        song_match = {'title': 'Test', 'artist': 'Test', 'genre': 'pop', 'mood': 'happy',
                      'energy': 0.5, 'valence': 0.5, 'danceability': 0.5, 'tempo_bpm': 120, 'acousticness': 0.5}
        song_mismatch = {'title': 'Test', 'artist': 'Test', 'genre': 'rock', 'mood': 'happy',
                         'energy': 0.5, 'valence': 0.5, 'danceability': 0.5, 'tempo_bpm': 120, 'acousticness': 0.5}
        prefs = {'genre': 'pop', 'mood': 'happy', 'energy': 0.5, 'valence': 0.5,
                 'danceability': 0.5, 'tempo': 120, 'acousticness': 0.5}
        score_match, _ = score_song(song_match, prefs)
        score_mismatch, _ = score_song(song_mismatch, prefs)
        self.assertGreater(score_match, score_mismatch)

    def test_score_song_mood_match(self):
        """Mood match contributes to score."""
        song = {'title': 'Test', 'artist': 'Test', 'genre': 'rock', 'mood': 'happy',
                'energy': 0.5, 'valence': 0.5, 'danceability': 0.5, 'tempo_bpm': 120, 'acousticness': 0.5}
        prefs = {'genre': 'rock', 'mood': 'happy', 'energy': 0.5, 'valence': 0.5,
                 'danceability': 0.5, 'tempo': 120, 'acousticness': 0.5}
        score_with, _ = score_song(song, prefs)
        prefs['mood'] = 'calm'
        score_without, _ = score_song(song, prefs)
        self.assertGreater(score_with, score_without)


class TestRecommendations(unittest.TestCase):
    """Test the recommend_songs function."""

    def setUp(self):
        self.songs = load_songs("data/songs.csv")

    def test_recommend_returns_k(self):
        """Returns exactly k recommendations."""
        prefs = {'genre': 'pop', 'mood': 'happy', 'energy': 0.9}
        for k in [1, 3, 5]:
            recs = recommend_songs(prefs, self.songs, k=k)
            self.assertEqual(len(recs), k)

    def test_recommend_sorted_by_score(self):
        """Sorted by score descending."""
        prefs = {'genre': 'pop', 'mood': 'happy', 'energy': 0.9}
        recs = recommend_songs(prefs, self.songs, k=5)
        scores = [score for _, score, _ in recs]
        for i in range(len(scores) - 1):
            self.assertGreaterEqual(scores[i], scores[i + 1])

    def test_recommend_valid_structure(self):
        """Each rec is (song_dict, score, reasons_list)."""
        prefs = {'genre': 'pop', 'mood': 'happy', 'energy': 0.9}
        recs = recommend_songs(prefs, self.songs, k=5)
        for rec in recs:
            self.assertEqual(len(rec), 3)
            song, score, reasons = rec
            self.assertIsInstance(song, dict)
            self.assertIsInstance(score, (int, float))
            self.assertIsInstance(reasons, list)

    def test_recommend_genre_respected(self):
        """Genre preference reflected in results."""
        pop_recs = recommend_songs({'genre': 'pop', 'mood': 'happy', 'energy': 0.5}, self.songs, k=5)
        pop_genres = [song.get('genre') for song, _, _ in pop_recs]
        self.assertGreaterEqual(sum(1 for g in pop_genres if g == 'pop'), 2)


class TestDiversityPenalty(unittest.TestCase):
    """Test diversity penalty application."""

    def test_no_penalty_different_artists(self):
        """No penalty when artists differ."""
        recs = [
            ({"title": "S1", "artist": "A1", "genre": "pop"}, 8.0, []),
            ({"title": "S2", "artist": "A2", "genre": "rock"}, 7.5, []),
        ]
        penalized = apply_diversity_penalty(recs)
        self.assertEqual(penalized[0][1], 8.0)
        self.assertEqual(penalized[1][1], 7.5)

    def test_penalty_duplicate_artist(self):
        """Penalty applied for duplicate artist."""
        recs = [
            ({"title": "S1", "artist": "A1", "genre": "pop"}, 8.0, []),
            ({"title": "S2", "artist": "A1", "genre": "rock"}, 7.5, []),
        ]
        penalized = apply_diversity_penalty(recs, penalty_per_artist=0.5)
        self.assertEqual(penalized[0][1], 8.0)
        self.assertEqual(penalized[1][1], 7.0)

    def test_penalty_duplicate_genre(self):
        """Penalty applied for duplicate genre."""
        recs = [
            ({"title": "S1", "artist": "A1", "genre": "pop"}, 8.0, []),
            ({"title": "S2", "artist": "A2", "genre": "pop"}, 7.5, []),
        ]
        penalized = apply_diversity_penalty(recs, penalty_per_genre=0.2)
        self.assertEqual(penalized[0][1], 8.0)
        self.assertEqual(penalized[1][1], 7.3)


class TestStrategies(unittest.TestCase):
    """Test different scoring strategies."""

    def setUp(self):
        self.songs = load_songs("data/songs.csv")
        self.prefs = {'genre': 'pop', 'mood': 'happy', 'energy': 0.9}

    def test_balanced_strategy(self):
        """BalancedStrategy works."""
        recs = recommend_songs(self.prefs, self.songs, k=5, strategy=BalancedStrategy())
        self.assertEqual(len(recs), 5)

    def test_energy_focused_strategy(self):
        """EnergyFocusedStrategy works."""
        recs = recommend_songs(self.prefs, self.songs, k=5, strategy=EnergyFocusedStrategy())
        self.assertEqual(len(recs), 5)

    def test_genre_first_strategy(self):
        """GenreFirstStrategy works."""
        recs = recommend_songs(self.prefs, self.songs, k=5, strategy=GenreFirstStrategy())
        self.assertEqual(len(recs), 5)

    def test_mood_first_strategy(self):
        """MoodFirstStrategy works."""
        recs = recommend_songs(self.prefs, self.songs, k=5, strategy=MoodFirstStrategy())
        self.assertEqual(len(recs), 5)

    def test_quality_first_strategy(self):
        """QualityFirstStrategy works."""
        recs = recommend_songs(self.prefs, self.songs, k=5, strategy=QualityFirstStrategy())
        self.assertEqual(len(recs), 5)

    def test_popularity_driven_strategy(self):
        """PopularityDrivenStrategy works."""
        recs = recommend_songs(self.prefs, self.songs, k=5, strategy=PopularityDrivenStrategy())
        self.assertEqual(len(recs), 5)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""

    def setUp(self):
        self.songs = load_songs("data/songs.csv")

    def test_k_equals_one(self):
        """Works with k=1."""
        prefs = {'genre': 'pop', 'mood': 'happy', 'energy': 0.5}
        recs = recommend_songs(prefs, self.songs, k=1)
        self.assertEqual(len(recs), 1)

    def test_k_larger_than_catalog(self):
        """Handles k > catalog size."""
        prefs = {'genre': 'pop', 'mood': 'happy', 'energy': 0.5}
        recs = recommend_songs(prefs, self.songs, k=len(self.songs) + 10)
        self.assertLessEqual(len(recs), len(self.songs))

    def test_empty_penalty_list(self):
        """Diversity penalty handles empty list."""
        penalized = apply_diversity_penalty([])
        self.assertEqual(len(penalized), 0)


class TestIntegration(unittest.TestCase):
    """Full pipeline tests."""

    def setUp(self):
        self.songs = load_songs("data/songs.csv")

    def test_full_pipeline_balanced(self):
        """Full pipeline: preferences -> recommendations -> penalties."""
        prefs = {'genre': 'pop', 'mood': 'happy', 'energy': 0.9}
        recs = recommend_songs(prefs, self.songs, k=5)
        penalized = apply_diversity_penalty(recs)
        self.assertEqual(len(penalized), 5)
        for _song, score, reasons, _note in penalized:
            self.assertGreater(score, 0)
            self.assertIsInstance(reasons, list)

    def test_full_pipeline_energy_focused(self):
        """Full pipeline with Energy-Focused strategy."""
        prefs = {'genre': 'pop', 'mood': 'happy', 'energy': 0.9}
        recs = recommend_songs(prefs, self.songs, k=5, strategy=EnergyFocusedStrategy())
        penalized = apply_diversity_penalty(recs)
        self.assertEqual(len(penalized), 5)

    def test_different_profiles(self):
        """Different profiles produce different results."""
        pop_recs = recommend_songs({'genre': 'pop', 'mood': 'happy', 'energy': 0.9}, self.songs, k=5)
        lofi_recs = recommend_songs({'genre': 'lofi', 'mood': 'calm', 'energy': 0.2}, self.songs, k=5)
        pop_genres = [s['genre'] for s, _, _ in pop_recs]
        lofi_genres = [s['genre'] for s, _, _ in lofi_recs]
        self.assertGreater(pop_genres.count('pop'), 1)
        self.assertGreater(lofi_genres.count('lofi'), 1)


if __name__ == '__main__':
    unittest.main()
