"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def display_recommendations(recommendations, max_score=7.9):
    """
    Display music recommendations in a clean, readable format.

    Args:
        recommendations: List of tuples (song_dict, score, reasons_list)
        max_score: Maximum possible score (default 7.9)
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


def main() -> None:
    songs = load_songs("data/songs.csv")

    # Define multiple distinct user preference profiles
    user_profiles = {
        "High-Energy Pop": {
            "genre": "pop",
            "mood": "happy",
            "energy": 0.9,
            "description": "Upbeat, feel-good pop music with high energy"
        },
        "Chill Lofi": {
            "genre": "lofi",
            "mood": "calm",
            "energy": 0.2,
            "description": "Relaxing, low-energy lofi beats for focus and relaxation"
        },
        "Deep Intense Rock": {
            "genre": "rock",
            "mood": "intense",
            "energy": 0.85,
            "description": "Heavy, powerful rock music with strong emotions"
        },
    }

    # Run recommendations for each profile
    for profile_name, prefs in user_profiles.items():
        description = prefs.pop("description")
        print(f"\n📊 USER PROFILE: {profile_name}")
        print(f"   Description: {description}")
        print(f"   Preferences: {prefs}")

        recommendations = recommend_songs(prefs, songs, k=5)
        display_recommendations(recommendations)


if __name__ == "__main__":
    main()
