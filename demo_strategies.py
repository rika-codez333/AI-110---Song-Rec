#!/usr/bin/env python3
"""
Demonstration of Challenge 2: Multiple Scoring Modes

This script shows how different scoring strategies produce different recommendations
for the same user profile. Each strategy prioritizes different aspects of songs.
"""

from src.recommender import (
    load_songs, Song, UserProfile, Recommender,
    BalancedStrategy, GenreFirstStrategy, MoodFirstStrategy,
    EnergyFocusedStrategy, QualityFirstStrategy, PopularityDrivenStrategy
)

def display_strategy_comparison(profile_name, user_profile, strategies, songs_data):
    """Compare recommendations across different strategies."""
    print(f"\n{'='*100}")
    print(f"🎵 STRATEGY COMPARISON: {profile_name}")
    print(f"{'='*100}")
    print(f"User Preferences: {profile_name}")
    print(f"  Genre: {user_profile.favorite_genre}")
    print(f"  Mood: {user_profile.favorite_mood}")
    print(f"  Energy: {user_profile.target_energy}")
    print()

    for strategy_name, strategy in strategies.items():
        print(f"\n{'─'*100}")
        print(f"📊 Strategy: {strategy_name}")
        print(f"{'─'*100}")

        recommender = Recommender(songs_data, strategy=strategy)
        recommendations = recommender.recommend(user_profile, k=3)

        for idx, song in enumerate(recommendations, 1):
            explanation = recommender.explain_recommendation(user_profile, song, strategy=strategy)
            print(f"\n  {idx}. {song.title} - {song.artist}")
            print(f"     {explanation}")

def main():
    print("\n" + "="*100)
    print("CHALLENGE 2: MULTIPLE SCORING MODES (STRATEGY PATTERN DEMONSTRATION)")
    print("="*100)

    # Load data
    songs_raw = load_songs("data/songs.csv")

    # Convert to Song objects
    songs = [
        Song(
            id=int(s['id']),
            title=s['title'],
            artist=s['artist'],
            genre=s['genre'],
            mood=s['mood'],
            energy=float(s['energy']),
            tempo_bpm=float(s['tempo_bpm']),
            valence=float(s['valence']),
            danceability=float(s['danceability']),
            acousticness=float(s['acousticness']),
            popularity=float(s['popularity']),
            release_decade=s['release_decade'],
            mood_tags=s['mood_tags'],
            artist_familiarity=float(s['artist_familiarity']),
            production_quality=float(s['production_quality']),
        )
        for s in songs_raw
    ]

    # Define strategies
    strategies = {
        "Balanced": BalancedStrategy(),
        "Genre-First": GenreFirstStrategy(),
        "Mood-First": MoodFirstStrategy(),
        "Energy-Focused": EnergyFocusedStrategy(),
        "Quality-First": QualityFirstStrategy(),
        "Popularity-Driven": PopularityDrivenStrategy(),
    }

    # Test Profile 1: High-Energy Pop
    user1 = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.9,
        preferred_valence=0.75,
        preferred_danceability=0.75,
        preferred_tempo_bpm=120,
        preferred_acousticness=0.3,
        min_popularity=70,
        preferred_production_quality=0.8,
        prefer_artist_familiarity=True
    )

    display_strategy_comparison("High-Energy Pop", user1, strategies, songs)

    # Test Profile 2: Chill Lofi
    user2 = UserProfile(
        favorite_genre="lofi",
        favorite_mood="calm",
        target_energy=0.2,
        preferred_valence=0.5,
        preferred_danceability=0.5,
        preferred_tempo_bpm=85,
        preferred_acousticness=0.75,
        min_popularity=40,
        preferred_production_quality=0.75,
        prefer_artist_familiarity=False
    )

    display_strategy_comparison("Chill Lofi", user2, strategies, songs)

    # Summary
    print(f"\n{'='*100}")
    print("STRATEGY PATTERN SUMMARY")
    print(f"{'='*100}")
    print("""
The Strategy Pattern allows users to switch between different recommendation philosophies:

1. **Balanced**: Equal weight across all features (default)
   → Best for: General-purpose discovery, balanced user preferences

2. **Genre-First**: Genre weight = 4.0 (doubled from 2.3)
   → Best for: Genre-focused users (metal fans, K-pop fans, jazz enthusiasts)

3. **Mood-First**: Mood weight = 2.5 (triple default), valence boosted
   → Best for: Context-aware recommendations (workout, sleep, party)

4. **Energy-Focused**: Energy & danceability = 2.5 (doubled)
   → Best for: Fitness playlists, dance parties, energetic moods

5. **Quality-First**: Production & artist familiarity weights boosted
   → Best for: Audiophiles, listeners who value high production standards

6. **Popularity-Driven**: Popularity & familiarity weights doubled
   → Best for: Mainstream discovery, radio-like recommendations

Each strategy produces DIFFERENT top-5 recommendations for the same user profile
because they weight features differently. Users can choose based on their context!
    """)

if __name__ == "__main__":
    main()
