"""
Adversarial and edge-case testing for the Music Recommender.

These profiles are designed to test the system's robustness and reveal
potential weaknesses or unexpected behavior.
"""

from recommender import load_songs, recommend_songs


def display_recommendations(recommendations, max_score=7.8):
    """Display music recommendations in a clean, readable format."""
    if not recommendations:
        print("No recommendations available.")
        return

    print("\n" + "=" * 70)
    print(f"🎵  TOP RECOMMENDATIONS ({len(recommendations)} songs)")
    print("=" * 70 + "\n")

    for idx, rec in enumerate(recommendations, 1):
        song, score, explanation = rec

        artist = song.get('artist', 'Unknown Artist')
        title = song.get('title', 'Unknown Title')
        print(f"{idx}. {title} - {artist}")

        score_percentage = (score / max_score) * 100
        bar_length = 30
        filled = int(bar_length * score_percentage / 100)
        bar = "█" * filled + "░" * (bar_length - filled)
        print(f"   Score: {score:.2f}/{max_score} │{bar}│ {score_percentage:.0f}%")

        print("   Why you'll love it:")
        if isinstance(explanation, list):
            for reason in explanation:
                print(f"     • {reason}")
        else:
            print(f"     • {explanation}")

        if idx < len(recommendations):
            print("\n" + "-" * 70 + "\n")
        else:
            print("\n" + "=" * 70 + "\n")


def main() -> None:
    songs = load_songs("data/songs.csv")

    # Define adversarial/edge-case user preference profiles
    adversarial_profiles = {
        "Contradictory Preferences": {
            "genre": "rock",
            "mood": "happy",
            "energy": 0.1,
            "description": "Conflicting preferences: happy mood + rock genre + very low energy"
        },
        "Extremely Picky (All Extremes)": {
            "genre": "jazz",
            "mood": "sad",
            "energy": 0.95,
            "description": "Extreme energy (0.95) with sad mood and rare jazz genre"
        },
        "Impossible Combo": {
            "genre": "lofi",
            "mood": "intense",
            "energy": 0.9,
            "description": "High-energy intense lofi (lofi is typically chill, not intense)"
        },
        "Niche Mood (Reflective)": {
            "genre": "pop",
            "mood": "reflective",
            "energy": 0.5,
            "description": "Non-standard mood 'reflective' (system may not have this mood in catalog)"
        },
    }

    # Run recommendations for each adversarial profile
    for profile_name, prefs in adversarial_profiles.items():
        description = prefs.pop("description")
        print(f"\n📊 ADVERSARIAL PROFILE: {profile_name}")
        print(f"   Description: {description}")
        print(f"   Preferences: {prefs}")

        recommendations = recommend_songs(prefs, songs, k=5)
        display_recommendations(recommendations)


if __name__ == "__main__":
    main()
