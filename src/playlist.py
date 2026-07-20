"""
Playlist management module for the Music Recommendation System.

Features:
- Create themed playlists (workout, study, sleep, party, relax)
- Add/remove/reorder songs in playlists
- Export playlists to CSV and JSON formats
- View playlist statistics (duration, avg energy, genres, moods)
"""

import json
import csv
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Tuple
from datetime import datetime


@dataclass
class Playlist:
    """Represents a music playlist with metadata and management."""
    name: str
    theme: str  # workout, study, sleep, party, relax, custom
    songs: List[Dict] = field(default_factory=list)
    duration_minutes: float = 0.0
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    description: str = ""

    def add_song(self, song: Dict, score: float = 0.0) -> None:
        """Add a song to the playlist."""
        song_entry = {
            **song,
            "added_score": score,
            "added_at": datetime.now().isoformat()
        }
        self.songs.append(song_entry)
        self._update_duration()

    def remove_song(self, song_index: int) -> bool:
        """Remove a song by index. Returns True if successful."""
        if 0 <= song_index < len(self.songs):
            self.songs.pop(song_index)
            self._update_duration()
            return True
        return False

    def reorder_song(self, from_index: int, to_index: int) -> bool:
        """Move a song from one position to another."""
        if 0 <= from_index < len(self.songs) and 0 <= to_index < len(self.songs):
            song = self.songs.pop(from_index)
            self.songs.insert(to_index, song)
            return True
        return False

    def _update_duration(self) -> None:
        """Calculate total playlist duration (rough estimate: ~3 min per song)."""
        self.duration_minutes = len(self.songs) * 3.0

    def get_stats(self) -> Dict:
        """Get playlist statistics."""
        if not self.songs:
            return {
                "song_count": 0,
                "duration_minutes": 0.0,
                "genres": [],
                "moods": [],
                "avg_energy": 0.0,
                "avg_danceability": 0.0,
                "artists": []
            }

        genres = list(set(s.get('genre', 'Unknown') for s in self.songs))
        moods = list(set(s.get('mood', 'Unknown') for s in self.songs))
        artists = list(set(s.get('artist', 'Unknown') for s in self.songs))

        energies = [float(s.get('energy', 0.5)) for s in self.songs if s.get('energy')]
        danceabilities = [float(s.get('danceability', 0.5)) for s in self.songs if s.get('danceability')]

        avg_energy = sum(energies) / len(energies) if energies else 0.0
        avg_danceability = sum(danceabilities) / len(danceabilities) if danceabilities else 0.0

        return {
            "song_count": len(self.songs),
            "duration_minutes": self.duration_minutes,
            "genres": genres,
            "moods": moods,
            "avg_energy": round(avg_energy, 2),
            "avg_danceability": round(avg_danceability, 2),
            "artists": artists,
            "unique_artists": len(artists)
        }

    def to_csv(self, filename: str) -> None:
        """Export playlist to CSV file."""
        if not self.songs:
            print(f"Playlist '{self.name}' is empty. No CSV created.")
            return

        fieldnames = ['rank', 'title', 'artist', 'genre', 'mood', 'energy', 'danceability', 'added_score']

        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for idx, song in enumerate(self.songs, 1):
                row = {
                    'rank': idx,
                    'title': song.get('title', ''),
                    'artist': song.get('artist', ''),
                    'genre': song.get('genre', ''),
                    'mood': song.get('mood', ''),
                    'energy': song.get('energy', ''),
                    'danceability': song.get('danceability', ''),
                    'added_score': song.get('added_score', '')
                }
                writer.writerow(row)

    def to_json(self, filename: str) -> None:
        """Export playlist to JSON file."""
        playlist_data = {
            "name": self.name,
            "theme": self.theme,
            "description": self.description,
            "created_at": self.created_at,
            "duration_minutes": self.duration_minutes,
            "song_count": len(self.songs),
            "stats": self.get_stats(),
            "songs": self.songs
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(playlist_data, f, indent=2, ensure_ascii=False)

    def display(self) -> None:
        """Display playlist in a formatted table."""
        print("\n" + "=" * 110)
        print(f"🎵 PLAYLIST: {self.name}")
        print(f"   Theme: {self.theme.upper()} | Duration: {self.duration_minutes:.1f} min | Songs: {len(self.songs)}")
        if self.description:
            print(f"   Description: {self.description}")
        print("=" * 110)

        if not self.songs:
            print("   (Empty playlist)")
            print("=" * 110 + "\n")
            return

        print(f"{'#':<3} {'Title':<35} {'Artist':<25} {'Genre':<15} {'Mood':<12} {'Energy':<8}")
        print("-" * 110)

        for idx, song in enumerate(self.songs, 1):
            title = song.get('title', 'Unknown')[:34]
            artist = song.get('artist', 'Unknown')[:24]
            genre = song.get('genre', 'Unknown')[:14]
            mood = song.get('mood', 'Unknown')[:11]
            energy = f"{float(song.get('energy', 0)):.2f}"

            print(f"{idx:<3} {title:<35} {artist:<25} {genre:<15} {mood:<12} {energy:<8}")

        print("=" * 110)
        stats = self.get_stats()
        print(f"   📊 Genres: {', '.join(stats['genres'][:5])}{'...' if len(stats['genres']) > 5 else ''}")
        print(f"   📊 Avg Energy: {stats['avg_energy']:.2f} | Avg Danceability: {stats['avg_danceability']:.2f}")
        print("=" * 110 + "\n")


class PlaylistGenerator:
    """Generate themed playlists from recommendations."""

    THEME_CONFIGS = {
        "workout": {
            "description": "High-energy tracks for gym and cardio",
            "min_energy": 0.7,
            "preferred_mood": "intense",
            "song_count": 15
        },
        "study": {
            "description": "Focused, non-distracting music for concentration",
            "max_energy": 0.5,
            "preferred_mood": "calm",
            "song_count": 20
        },
        "sleep": {
            "description": "Relaxing, low-energy ambient music",
            "max_energy": 0.3,
            "preferred_mood": "peaceful",
            "song_count": 12
        },
        "party": {
            "description": "Upbeat, danceable tracks for celebrations",
            "min_energy": 0.8,
            "min_danceability": 0.7,
            "preferred_mood": "happy",
            "song_count": 25
        },
        "relax": {
            "description": "Chill, mellow background music",
            "max_energy": 0.6,
            "min_acousticness": 0.5,
            "preferred_mood": "chill",
            "song_count": 18
        }
    }

    @classmethod
    def generate_themed_playlist(cls, songs: List[Dict], theme: str) -> Optional[Playlist]:
        """Generate a themed playlist by filtering songs and scoring them."""
        if theme not in cls.THEME_CONFIGS:
            print(f"Unknown theme: {theme}. Available: {', '.join(cls.THEME_CONFIGS.keys())}")
            return None

        config = cls.THEME_CONFIGS[theme]
        filtered_songs = cls._filter_songs_by_theme(songs, config)

        # Sort by theme-appropriate metrics
        sorted_songs = cls._sort_by_theme(filtered_songs, theme)

        # Take top N songs
        playlist_songs = sorted_songs[:config["song_count"]]

        playlist = Playlist(
            name=f"{theme.capitalize()} Mix",
            theme=theme,
            description=config["description"]
        )

        for idx, song in enumerate(playlist_songs, 1):
            score = 10.0 - (idx * 0.1)  # Decreasing scores
            playlist.add_song(song, score=score)

        return playlist

    @staticmethod
    def _filter_songs_by_theme(songs: List[Dict], config: Dict) -> List[Dict]:
        """Filter songs based on theme constraints."""
        filtered = []

        for song in songs:
            energy = float(song.get('energy', 0.5))
            danceability = float(song.get('danceability', 0.5))
            acousticness = float(song.get('acousticness', 0.5))

            # Check constraints
            if 'min_energy' in config and energy < config['min_energy']:
                continue
            if 'max_energy' in config and energy > config['max_energy']:
                continue
            if 'min_danceability' in config and danceability < config['min_danceability']:
                continue
            if 'min_acousticness' in config and acousticness < config['min_acousticness']:
                continue

            filtered.append(song)

        return filtered

    @staticmethod
    def _sort_by_theme(songs: List[Dict], theme: str) -> List[Dict]:
        """Sort songs according to theme priorities."""
        if theme == "workout":
            return sorted(songs, key=lambda s: float(s.get('energy', 0)) * float(s.get('danceability', 0)), reverse=True)
        elif theme == "study":
            return sorted(songs, key=lambda s: float(s.get('acousticness', 0)), reverse=True)
        elif theme == "sleep":
            return sorted(songs, key=lambda s: (1 - float(s.get('energy', 0))), reverse=True)
        elif theme == "party":
            return sorted(songs, key=lambda s: float(s.get('danceability', 0)), reverse=True)
        elif theme == "relax":
            return sorted(songs, key=lambda s: float(s.get('valence', 0.5)) * float(s.get('acousticness', 0)), reverse=True)
        else:
            return songs

    @staticmethod
    def create_custom_playlist(name: str, songs: List[Dict], description: str = "") -> Playlist:
        """Create a custom playlist from any selection of songs."""
        playlist = Playlist(name=name, theme="custom", description=description)
        for song in songs:
            playlist.add_song(song)
        return playlist
