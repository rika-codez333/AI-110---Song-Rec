# 🎵 Music Recommender Simulation

## Project Summary

This project builds a **content-based music recommender system** that predicts which songs a user will love by analyzing audio features and emotional attributes. The system models songs as 10-dimensional vectors (genre, mood, energy, valence, danceability, tempo, acousticness, and metadata) and users as preference profiles with favorite genre, mood, target energy level, and acoustic preferences. Using **proximity-based Gaussian scoring**, it computes a match score for each song that rewards songs close to the user's taste without penalizing diversity. The system is designed to be interpretable (every recommendation includes explanations), lightweight (no external ML models), and tunable (weights and matching parameters can be adjusted).

This mirrors how real-world platforms like Spotify work on their recommendation backend: they blend collaborative filtering (what similar users like) with content-based filtering (what this song is actually like) and explicit user feedback (likes, skips, playlists) to serve personalized recommendations at scale.

---

## How The System Works

### Real-World Context
Streaming platforms like Spotify and YouTube Music use two main approaches to recommend songs: **collaborative filtering** (analyzing what similar users like) and **content-based filtering** (analyzing song attributes). This system implements **content-based filtering** because it works well with limited user data and is interpretable—you can explain *why* a song was recommended. Real-world systems often blend both approaches and add a third layer: **user behavior data** (plays, skips, likes). Our version prioritizes **audio features** (energy, valence, danceability) as the foundation for predicting musical "vibe," since these directly capture what makes a song feel right for a given mood or context.

### System Architecture

**Song Features** (10 attributes per song):
- **Categorical**: `genre`, `mood` — semantic labels
- **Numeric Audio Features**:
  - `energy` (0–1): Intensity/loudness of track
  - `valence` (0–1): Emotional positivity (sad → happy)
  - `danceability` (0–1): Groove and rhythm suitability
  - `tempo_bpm` (60–152): Speed in beats per minute
  - `acousticness` (0–1): Acoustic vs. electronic production
- **Metadata**: `id`, `title`, `artist`

**UserProfile Storage**:
The system represents a user's taste through four core preferences:
- `favorite_genre` — preferred music category (e.g., "pop", "lofi")
- `favorite_mood` — preferred emotional context (e.g., "chill", "intense")
- `target_energy` — ideal energy level (0–1 scale, e.g., 0.8 for high-energy)
- `likes_acoustic` — boolean for acoustic vs. electronic preference

**Scoring Algorithm** (Content-Based Proximity Matching):
Each song receives a score based on how close its audio features match the user's preferences.

### Algorithm Recipe (Option D: Balanced Discovery)

**Weights per Feature** (maximum score: 7.8):
| Feature | Weight | Scoring Method |
|---------|--------|-----------------|
| Genre | 2.0 | Exact match: +2.0 if match, 0 otherwise |
| Mood | 1.0 | Exact match: +1.0 if match, 0 otherwise |
| Energy | 1.4 | Gaussian similarity: 1.4 × exp(-k × distance²) |
| Danceability | 1.2 | Gaussian similarity: 1.2 × exp(-k × distance²) |
| Valence | 1.0 | Gaussian similarity: 1.0 × exp(-k × distance²) |
| Tempo (BPM) | 0.6 | Gaussian similarity: 0.6 × exp(-k × distance²) |
| Acousticness | 0.6 | Gaussian similarity: 0.6 × exp(-k × distance²) |

**Formula**:
```
TOTAL_SCORE = genre_contrib + mood_contrib + energy_contrib + 
              danceability_contrib + valence_contrib + tempo_contrib + acousticness_contrib

Where:
- genre_contrib = 2.0 if (song.genre == user.favorite_genre) else 0.0
- mood_contrib = 1.0 if (song.mood == user.favorite_mood) else 0.0
- numeric_contrib = weight × exp(-k × (user_preference - song_value)²)
- k = tuning_param (0.5=loose/forgiving, 1.0=standard, 2.0=strict)
```

**Intuition**: The system rewards songs that match audio features *close to* what the user likes (via Gaussian), without penalizing songs that differ. Genre and mood are exact-match categorical filters—a critical design choice that emphasizes user intent over serendipity.

**Ranking & Recommendation**:
1. Score all available songs independently using the formula above
2. Sort by total score (descending)
3. Return top-k recommendations with explainable reasons for each pick
4. Explanations highlight which features contributed most to the score (marked with 🎯 for excellent matches >0.9 similarity, ✓ for good matches >0.7)

### Potential Biases in This System

1. **Heavy Genre Preference**: Genre is weighted at 2.0 (25.6% of max score), making exact-match genre the strongest factor. This system might **over-prioritize familiar genres and miss great cross-genre discoveries**. A user who loves "pop" might miss an amazing "lofi" acoustic track with identical energy/mood characteristics.

2. **Categorical Mood Rigidity**: Mood uses exact matching (chill = chill, intense = intense), with no similarity metric. **A song with mood="chill" won't match a user preferring mood="relaxed," even though they're semantically identical.** This creates artificial "cliffs" in recommendations.

3. **Gaussian Centering on User Preferences**: The Gaussian similarity rewards songs matching the user's *exact* preferences (e.g., target_energy = 0.5). This can **suppress unexpected discoveries**—a high-energy song that matches mood and genre perfectly might score lower than a mediocre low-energy song if the user's target_energy doesn't match.

4. **Tiny Catalog Bias**: Recommendations are only as diverse as the training data. A 30-song catalog won't find the perfect song in a library of millions.

5. **No Temporal or Popularity Signals**: The system doesn't account for song release date, artist popularity, or trending status. Very old or niche songs might not be recommended despite matching features.

6. **No Feedback Loop**: The system is static—it doesn't learn from user behavior (skips, replays, saves). Real systems like Spotify adjust weights after each interaction.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

### Example 1: High-Energy Workout User
```
User Profile: genre=pop, mood=intense, target_energy=0.93, likes_acoustic=False

Top 5 Recommendations:

1. ⭐ Gym Hero by Max Pulse | Score: 1.000
   🎯 energy excellent match (0.93 ≈ 0.93)
   🎯 valence excellent match (0.77 ≈ 0.77)
   🎸 genre matches (pop)

2. Storm Runner by Voltline | Score: 0.824
   🎯 energy excellent match (0.91 ≈ 0.93)
   ✓ danceability good match (0.66)

3. Sunrise City by Neon Echo | Score: 0.744
   🎯 energy excellent match (0.82 ≈ 0.93)
   🎯 valence excellent match (0.84 ≈ 0.77)

4. Rooftop Lights by Indigo Parade | Score: 0.688
   ✓ energy good match (0.76)
   🎯 valence excellent match (0.81 ≈ 0.77)

5. Night Drive Loop by Neon Echo | Score: 0.671
   ✓ energy good match (0.75)
   ✓ danceability good match (0.73)
```

### Example 2: Chill Study User
```
User Profile: genre=lofi, mood=chill, target_energy=0.35, likes_acoustic=True

Top 5 Recommendations:

1. ⭐ Library Rain by Paper Lanterns | Score: 1.000
   🎯 energy excellent match (0.35 ≈ 0.35)
   🎸 genre matches (lofi)
   🎭 mood matches (chill)

2. Midnight Coding by LoRoom | Score: 0.897
   🎯 energy excellent match (0.42 ≈ 0.35)
   🎸 genre matches (lofi)

3. Spacewalk Thoughts by Orbit Bloom | Score: 0.842
   🎯 energy excellent match (0.28 ≈ 0.35)
   ✓ acousticness good match (0.92)

4. Focus Flow by LoRoom | Score: 0.749
   🎯 energy excellent match (0.40 ≈ 0.35)
   🎸 genre matches (lofi)

5. Coffee Shop Stories by Slow Stereo | Score: 0.697
   ✓ energy good match (0.37)
   ✓ acousticness good match (0.89)
```

**Key Observation**: The recommender learns that "musical vibe" emerges from audio features (energy, valence, danceability) more than categorical labels, allowing cross-genre recommendations when the emotional tone matches.

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



