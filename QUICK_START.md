# Quick Start Guide: Advanced Song Recommendation System

## Running the System

### Basic Recommendations
```bash
python3 -m src.main
```
Shows recommendations for 3 user profiles using the **Balanced Strategy**.

### View Different Strategies
```bash
python3 demo_strategies.py
```
Compares how different strategies (Genre-First, Mood-First, Energy-Focused, etc.) produce different recommendations for the same user.

### Run Tests
```bash
python3 -m pytest tests/ -v
```

---

## Understanding the New Features

### Challenge 1: 5 New Song Attributes

Each song now has:
- **Popularity** (0-100): How mainstream the song is
- **Release Decade** (e.g., "2020s"): When the song was released
- **Mood Tags**: Detailed mood descriptors (e.g., "uplifting,energetic")
- **Artist Familiarity** (0-1): How well-known the artist is
- **Production Quality** (0-1): How professionally produced the song is

These contribute to a max score of **9.5** (up from 7.9).

### Challenge 2: Multiple Scoring Strategies

Choose your recommendation philosophy:

| Strategy | Best For | Key Weight |
|----------|----------|-----------|
| **Balanced** | General purpose | All features equal |
| **Genre-First** | Genre fans (metal, K-pop) | Genre = 4.0 |
| **Mood-First** | Context-based (mood matters) | Mood = 2.5 |
| **Energy-Focused** | Activity playlists (gym, party) | Energy = 2.5 |
| **Quality-First** | Audiophiles | Production = 1.8 |
| **Popularity-Driven** | Mainstream discovery | Popularity = 2.0 |

**Usage:**
```python
from src.recommender import Recommender, GenreFirstStrategy, EnergyFocusedStrategy

# Genre-focused recommendations
rec = Recommender(songs, strategy=GenreFirstStrategy())
results = rec.recommend(user, k=5)

# Energy-focused recommendations
rec = Recommender(songs, strategy=EnergyFocusedStrategy())
results = rec.recommend(user, k=5)
```

### Challenge 3: Diversity Penalty

Prevents algorithm from recommending too many songs from same artist:
- First occurrence: No penalty
- Second occurrence of artist: -0.5 points
- Duplicate genre: -0.2 points

Example: If top 5 are [Song A by Artist X, Song B by Artist X, Song C, ...], the penalty may reshuffle to [Song A, Song C, ...] to encourage variety.

### Challenge 4: Visual Summary Table

After each recommendation set, see a clean summary:
```
# | Title (Artist) | Score | Genre/Mood | Top Reason
1 | Sunrise City (Neon Echo) | 8.70/9.5 (92%) | pop/happy | 🎯 energy match
2 | Gym Hero (Max Pulse) | 7.15/9.5 (75%) | pop/intense | 🎯 energy match
```

---

## Key Files

| File | Purpose |
|------|---------|
| `data/songs.csv` | 68 songs with 15 attributes each |
| `src/recommender.py` | Core recommendation engine + Strategy pattern |
| `src/main.py` | Demo runner with 3 user profiles |
| `demo_strategies.py` | Strategy comparison script |
| `tests/test_recommender.py` | Unit tests (2 tests, 100% pass) |
| `ai_interactions.md` | Documentation of AI assistance used |
| `CHALLENGES_COMPLETED.md` | Detailed challenge writeup |

---

## Example: Using Custom Strategy

```python
from src.recommender import (
    load_songs, UserProfile, Recommender, MoodFirstStrategy
)

# Load songs
songs = load_songs("data/songs.csv")

# Create user profile
user = UserProfile(
    favorite_genre="lofi",
    favorite_mood="calm",
    target_energy=0.2,
    preferred_valence=0.5,
    preferred_danceability=0.5,
    preferred_tempo_bpm=85,
    preferred_acousticness=0.75,
    min_popularity=40,  # New field
    preferred_production_quality=0.75,  # New field
    prefer_artist_familiarity=False  # New field
)

# Get recommendations using Mood-First strategy
recommender = Recommender(songs, strategy=MoodFirstStrategy())
recommendations = recommender.recommend(user, k=5)

for song in recommendations:
    explanation = recommender.explain_recommendation(user, song)
    print(f"{song.title} - {song.artist}\n{explanation}\n")
```

---

## Dataset Stats

- **Total Songs**: 68
- **Genres**: 25+ (pop, rock, lofi, jazz, classical, reggae, hip-hop, electronic, metal, country, blues, folk, ambient, house, techno, trance, dubstep, drum & bass, indie rock, alternative, psychedelic, opera, Caribbean varieties, etc.)
- **Attributes per Song**: 15 (id, title, artist, genre, mood, energy, tempo, valence, danceability, acousticness, **popularity**, **release_decade**, **mood_tags**, **artist_familiarity**, **production_quality**)
- **Mood Categories**: 15+ (happy, intense, chill, calm, melancholic, relaxed, focused, peaceful, romantic, contemplative, nostalgic, uplifting, energetic, joyful, inspiring)

---

## Next Steps

1. **Try different strategies** on your favorite user profile in `src/main.py`
2. **Adjust diversity penalty** in `apply_diversity_penalty()` to tune exploration vs. exploitation
3. **Add your own strategy** by subclassing `ScoringStrategy`
4. **Experiment with weights** in strategy classes to tune recommendations

---

## Challenges Completed

✅ **Challenge 1**: Added 5 advanced song attributes + updated scoring  
✅ **Challenge 2**: Implemented Strategy Pattern with 6 scoring modes  
✅ **Challenge 3**: Added diversity penalty for fairness  
✅ **Challenge 4**: Created visual summary table for improved UX  

See `CHALLENGES_COMPLETED.md` for detailed information.

---

## Questions?

- **How does the Strategy Pattern work?** See `src/recommender.py` lines 52-230
- **How is diversity enforced?** See `src/main.py` lines 78-105 (`apply_diversity_penalty`)
- **What are the new attributes?** See `data/songs.csv` columns 11-15
- **How can I add a new strategy?** Create a class inheriting from `ScoringStrategy` and implement `score_song()`
