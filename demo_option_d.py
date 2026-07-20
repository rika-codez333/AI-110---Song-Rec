#!/usr/bin/env python3
"""
Demo script: Option D recommendation algorithm with logging.
Shows the finalized point-weighting strategy in action.
"""

from src.recommender import Song, UserProfile, Recommender, load_songs
import logging

# Set up logging to show detailed scoring
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'
)

def demo_option_d():
    print("=" * 80)
    print("OPTION D: BALANCED RECOMMENDATION ALGORITHM DEMO")
    print("=" * 80)
    print("\n📊 RECIPE:")
    print("  Genre match: +2.0  |  Mood match: +1.0")
    print("  Energy: +1.4  |  Danceability: +1.2  |  Valence: +1.0")
    print("  Tempo: +0.6  |  Acousticness: +0.6")
    print("  Max Score: 7.8\n")

    # Load songs from CSV
    songs_data = load_songs('data/songs.csv')
    songs = [Song(**song) for song in songs_data]
    recommender = Recommender(songs)

    # Demo User 1: Pop + Happy lover
    print("\n" + "=" * 80)
    print("USER 1: Pop + Happy Music Lover")
    print("=" * 80)
    user1 = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.75,
        preferred_valence=0.8,
        preferred_danceability=0.75,
        preferred_tempo_bpm=120,
        preferred_acousticness=0.2,
    )
    print(f"Preferences: pop + happy + high energy (0.75) + danceable (0.75)")
    print(f"\nRecommendations (standard matching, k=1.0):\n")
    recommendations1 = recommender.recommend(user1, k=5, verbose=True)
    print()

    # Show detailed explanation for top recommendation
    print(f"📋 DETAILED EXPLANATION for top pick:")
    explanation = recommender.explain_recommendation(user1, recommendations1[0], verbose=True)
    print(f"\n{explanation}\n")

    # Demo User 2: Lofi + Chill person
    print("\n" + "=" * 80)
    print("USER 2: Lofi + Chill Music Lover")
    print("=" * 80)
    user2 = UserProfile(
        favorite_genre="lofi",
        favorite_mood="chill",
        target_energy=0.35,
        preferred_valence=0.55,
        preferred_danceability=0.5,
        preferred_tempo_bpm=80,
        preferred_acousticness=0.8,
    )
    print(f"Preferences: lofi + chill + low energy (0.35) + acoustic (0.8)")
    print(f"\nRecommendations (standard matching, k=1.0):\n")
    recommendations2 = recommender.recommend(user2, k=5, verbose=True)
    print()

    # Demo User 3: Strict matching (k=2.0)
    print("\n" + "=" * 80)
    print("USER 3: Strict Matching Demo (k=2.0 - must be very close)")
    print("=" * 80)
    user3 = UserProfile(
        favorite_genre="electronic",
        favorite_mood="energetic",
        target_energy=0.9,
        preferred_valence=0.75,
        preferred_danceability=0.85,
        preferred_tempo_bpm=128,
        preferred_acousticness=0.1,
    )
    print(f"Preferences: electronic + energetic + very high energy (0.9) + highly danceable (0.85)")
    print(f"\nRecommendations (STRICT matching, k=2.0):\n")
    recommendations3 = recommender.recommend(user3, k=5, tuning_param=2.0, verbose=True)
    print()

    # Demo User 4: Loose matching (k=0.5)
    print("\n" + "=" * 80)
    print("USER 4: Loose Matching Demo (k=0.5 - close is good enough)")
    print("=" * 80)
    user4 = UserProfile(
        favorite_genre="jazz",
        favorite_mood="relaxed",
        target_energy=0.45,
        preferred_valence=0.65,
        preferred_danceability=0.55,
        preferred_tempo_bpm=100,
        preferred_acousticness=0.75,
    )
    print(f"Preferences: jazz + relaxed + moderate energy (0.45)")
    print(f"\nRecommendations (LOOSE matching, k=0.5):\n")
    recommendations4 = recommender.recommend(user4, k=5, tuning_param=0.5, verbose=True)
    print()

    print("\n" + "=" * 80)
    print("✅ DEMO COMPLETE")
    print("=" * 80)
    print("\n💡 KEY INSIGHTS:")
    print("  • Genre + Mood exact matches award 3.0 points (38% of max score)")
    print("  • Energy + Danceability synergy: users want both to flow together")
    print("  • Valence balances mood (vibe check)")
    print("  • Tempo & Acousticness are equal refinements (0.6 each)")
    print("  • Tuning parameter k adjusts matching strictness:")
    print("    - k=0.5: Loose (accept close matches)")
    print("    - k=1.0: Standard (balanced)")
    print("    - k=2.0: Strict (only very close matches)")
    print()

if __name__ == "__main__":
    demo_option_d()
