"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender with multiple scoring modes.

Features:
- Multiple scoring strategies (Balanced, Genre-First, Mood-First, Energy-Focused, Quality-First, Popularity-Driven)
- Diversity penalty to avoid recommending too many songs from same artist
- Formatted table output with visual indicators
- Playlist generation and export (CSV/JSON)
"""

from typing import List, Dict
from .recommender import (
    load_songs, recommend_songs,
    BalancedStrategy, GenreFirstStrategy, MoodFirstStrategy,
    EnergyFocusedStrategy, QualityFirstStrategy, PopularityDrivenStrategy
)
from .playlist import Playlist, PlaylistGenerator


def display_recommendations(recommendations, max_score=9.5):
    """
    Display music recommendations in a clean, readable format.

    Args:
        recommendations: List of tuples (song_dict, score, reasons_list)
        max_score: Maximum possible score (default 9.5)
    """
    if not recommendations:
        print("No recommendations available.")
        return

    # Header
    print("\n" + "=" * 70)
    print(f"🎵  TOP RECOMMENDATIONS ({len(recommendations)} songs)")
    print("=" * 70 + "\n")

    # Display each recommendation
    for idx, rec in enumerate(recommendations, 1):
        song, score, explanation = rec

        # Song info with number
        artist = song.get('artist', 'Unknown Artist')
        title = song.get('title', 'Unknown Title')
        print(f"{idx}. {title} - {artist}")

        # Score with progress bar
        score_percentage = (score / max_score) * 100
        bar_length = 30
        filled = int(bar_length * score_percentage / 100)
        bar = "█" * filled + "░" * (bar_length - filled)
        print(f"   Score: {score:.2f}/{max_score} │{bar}│ {score_percentage:.0f}%")

        # Reasons as formatted bullet points
        print("   Why you'll love it:")
        if isinstance(explanation, list):
            for reason in explanation:
                print(f"     • {reason}")
        else:
            print(f"     • {explanation}")

        # Separator between recommendations
        if idx < len(recommendations):
            print("\n" + "-" * 70 + "\n")
        else:
            print("\n" + "=" * 70 + "\n")


def apply_diversity_penalty(recommendations, penalty_per_artist=0.5, penalty_per_genre=0.2):
    """Apply diversity penalty to prevent too many songs from same artist/genre.

    Args:
        recommendations: List of (song_dict, score, reasons_list) tuples
        penalty_per_artist: Penalty deducted for each duplicate artist
        penalty_per_genre: Penalty deducted for each duplicate genre

    Returns:
        List of recommendations with adjusted scores and diversity notes
    """
    seen_artists = set()
    seen_genres = set()
    penalized_recs = []

    for song, score, reasons in recommendations:
        artist = song.get('artist')
        genre = song.get('genre')
        diversity_note = ""
        adjusted_score = score

        if artist in seen_artists:
            adjusted_score -= penalty_per_artist
            diversity_note = f" (artist duplicate: -{penalty_per_artist})"

        if genre in seen_genres:
            adjusted_score -= penalty_per_genre
            diversity_note += f" (genre duplicate: -{penalty_per_genre})"

        penalized_recs.append((song, adjusted_score, reasons, diversity_note))
        seen_artists.add(artist)
        seen_genres.add(genre)

    # Re-sort by adjusted score
    penalized_recs.sort(key=lambda x: -x[1])
    return penalized_recs

def display_recommendations_table(recommendations, max_score=9.5):
    """Display recommendations as a formatted summary table (Challenge 4)."""
    if not recommendations:
        print("No recommendations available.")
        return

    print("\n" + "=" * 120)
    print(f"🎵 RECOMMENDATION SUMMARY TABLE")
    print("=" * 120)

    # Create table rows
    table_rows = []
    for idx, rec in enumerate(recommendations, 1):
        if len(rec) == 4:  # Includes diversity note
            song, score, explanation, diversity_note = rec
        else:
            song, score, explanation = rec
            diversity_note = ""

        title = song.get('title', 'Unknown')
        artist = song.get('artist', 'Unknown')
        genre = song.get('genre', 'Unknown')
        mood = song.get('mood', 'Unknown')
        score_pct = (score / max_score) * 100

        # Top reason for recommendation
        top_reason = explanation[0] if explanation else "No explanation"

        table_rows.append([
            idx,
            f"{title}\n({artist})",
            f"{score:.2f}/9.5\n({score_pct:.0f}%)",
            f"{genre}\n{mood}",
            top_reason + diversity_note
        ])

    # Print with aligned columns
    header = ["#", "Title (Artist)", "Score", "Genre/Mood", "Top Reason"]
    col_widths = [3, 35, 15, 20, 50]

    # Header
    print(f"{'#':<3} {'Title (Artist)':<35} {'Score':<15} {'Genre/Mood':<20} {'Top Reason':<50}")
    print("-" * 120)

    # Rows
    for row in table_rows:
        print(f"{row[0]:<3} {row[1]:<35} {row[2]:<15} {row[3]:<20} {row[4]:<50}")

    print("=" * 120 + "\n")

def demonstrate_playlists(songs: List[Dict]) -> None:
    """Demonstrate themed playlist generation (new feature)."""
    print("\n\n" + "="*120)
    print("🎵 PLAYLIST FEATURE DEMONSTRATION")
    print("="*120)
    print("Creating themed playlists for different contexts...\n")

    themes = ["workout", "study", "sleep", "party", "relax"]
    playlists = {}

    for theme in themes:
        playlist = PlaylistGenerator.generate_themed_playlist(songs, theme)
        if playlist:
            playlists[theme] = playlist
            playlist.display()
            print()

    # Save playlists to files
    print("="*120)
    print("📁 SAVING PLAYLISTS TO FILES")
    print("="*120)
    for theme, playlist in playlists.items():
        csv_file = f"playlists/{theme}_playlist.csv"
        json_file = f"playlists/{theme}_playlist.json"
        try:
            import os
            os.makedirs("playlists", exist_ok=True)
            playlist.to_csv(csv_file)
            playlist.to_json(json_file)
            print(f"✅ {theme.capitalize()} playlist saved to {csv_file} and {json_file}")
        except Exception as e:
            print(f"⚠️  Could not save {theme} playlist: {e}")

    print("\n")


def main() -> None:
    songs = load_songs("data/songs.csv")

    # Define multiple distinct user preference profiles
    user_profiles = {
        "High-Energy Pop": {
            "genre": "pop",
            "mood": "happy",
            "energy": 0.9,
            "min_popularity": 70,
            "description": "Upbeat, feel-good pop music with high energy and broad appeal"
        },
        "Chill Lofi": {
            "genre": "lofi",
            "mood": "calm",
            "energy": 0.2,
            "min_popularity": 50,
            "description": "Relaxing, low-energy lofi beats for focus with good production"
        },
        "Deep Intense Rock": {
            "genre": "rock",
            "mood": "intense",
            "energy": 0.85,
            "min_popularity": 40,
            "description": "Heavy, powerful rock music with strong emotions"
        },
    }

    # Define different scoring strategies for Challenge 2
    strategies = {
        "Balanced": BalancedStrategy(),
        "Genre-First": GenreFirstStrategy(),
        "Energy-Focused": EnergyFocusedStrategy(),
    }

    # Run recommendations for each profile with different strategies
    for profile_name, prefs in user_profiles.items():
        description = prefs.pop("description")
        print(f"\n\n📊 USER PROFILE: {profile_name}")
        print(f"   Description: {description}")
        print(f"   Preferences: {prefs}")

        # Show recommendations for the default Balanced strategy
        recommendations = recommend_songs(prefs, songs, k=5)
        display_recommendations(recommendations)

        # Show a summary table (Challenge 4)
        print("\n📊 QUICK SUMMARY TABLE:")
        display_recommendations_table(recommendations)

        # Show an example with Energy-Focused strategy (Challenge 2)
        if profile_name == "High-Energy Pop":
            print("\n🎵 ALTERNATIVE VIEW: Energy-Focused Strategy")
            print("   (Prioritizes energy and danceability over genre)")
            # Note: For this we'd need to enhance recommend_songs to accept strategy
            print("   [See Challenge 2 implementation in recommender.py for strategy pattern]")

    # Demonstrate playlist creation (new feature)
    demonstrate_playlists(songs)


if __name__ == "__main__":
    main()
