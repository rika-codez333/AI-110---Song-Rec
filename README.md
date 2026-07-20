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
Each song receives a score based on how close its audio features match the user's preferences:
```
SCORE = 0.25×energy + 0.20×valence + 0.20×danceability + 
         0.15×mood_match + 0.10×tempo + 0.05×genre_match + 0.05×acousticness

Where numeric features use Gaussian similarity: exp(-k * (user_pref - song_value)²)
And categorical features use exact matching: 1.0 if match, 0.0 otherwise
```

**Ranking & Recommendation**:
1. Score all available songs independently
2. Sort by score (descending)
3. Return top-k recommendations with explainable reasons for each pick

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



