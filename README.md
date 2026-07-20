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

### Running the Evaluation Scripts

**Standard Profile Evaluation** (3 diverse user profiles):
```bash
python -m src.main
```

This runs recommendations for:
1. **High-Energy Pop** — upbeat, feel-good music
2. **Chill Lofi** — relaxing, low-energy focus music
3. **Deep Intense Rock** — heavy, powerful rock

**Adversarial Testing** (4 edge-case profiles to stress-test the system):
```bash
python src/adversarial_test.py
```

This tests how the system handles:
1. **Contradictory Preferences** — conflicting signals (rock + happy + low energy)
2. **Extremely Picky** — extreme feature values (energy=0.95 with rare genre)
3. **Impossible Combo** — semantically contradictory preferences (intense lofi)
4. **Niche Mood** — non-existent mood category in the catalog

---

## System Evaluation: Multi-Profile Testing

This section documents how the recommender performs across **three distinct user profiles** representing different musical tastes and contexts. Each profile was evaluated on the same song catalog to assess recommendation quality, diversity, and scoring consistency.

### Profile 1: High-Energy Pop Listener
**Preferences**: `genre=pop, mood=happy, energy=0.9`  
**Context**: Upbeat, feel-good pop music with maximum energy

```
======================================================================
🎵  TOP RECOMMENDATIONS (5 songs)
======================================================================

1. Sunrise City - Neon Echo
   Score: 6.93/7.8 │██████████████████████████░░░░│ 89%
   Why you'll love it:
     • 🎯 energy excellent match (0.82 ≈ 0.90)
     • 🎯 danceability excellent match (0.79 ≈ 0.50)
     • ✓ valence good match (0.84)
     • 🎯 acousticness excellent match (0.18 ≈ 0.50)
     • 🎭 mood matches (happy)
     • 🎸 genre matches (pop)

----------------------------------------------------------------------

2. Gym Hero - Max Pulse
   Score: 5.86/7.8 │██████████████████████░░░░░░░░│ 75%
   Why you'll love it:
     • 🎯 energy excellent match (0.93 ≈ 0.90)
     • ✓ danceability good match (0.88)
     • 🎯 valence excellent match (0.77 ≈ 0.50)
     • ✓ acousticness good match (0.05)
     • 🎸 genre matches (pop)

----------------------------------------------------------------------

3. Rooftop Lights - Indigo Parade
   Score: 4.95/7.8 │███████████████████░░░░░░░░░░░│ 63%
   Why you'll love it:
     • 🎯 energy excellent match (0.76 ≈ 0.90)
     • 🎯 danceability excellent match (0.82 ≈ 0.50)
     • 🎯 valence excellent match (0.81 ≈ 0.50)
     • 🎯 acousticness excellent match (0.35 ≈ 0.50)
     • 🎭 mood matches (happy)

----------------------------------------------------------------------

4. Storm Runner - Voltline
   Score: 4.08/7.8 │███████████████░░░░░░░░░░░░░░░│ 52%
   Why you'll love it:
     • 🎯 energy excellent match (0.91 ≈ 0.90)
     • 🎯 danceability excellent match (0.66 ≈ 0.50)
     • 🎯 valence excellent match (0.48 ≈ 0.50)
     • ✓ acousticness good match (0.10)

----------------------------------------------------------------------

5. Night Drive Loop - Neon Echo
   Score: 4.06/7.8 │███████████████░░░░░░░░░░░░░░░│ 52%
   Why you'll love it:
     • 🎯 energy excellent match (0.75 ≈ 0.90)
     • 🎯 danceability excellent match (0.73 ≈ 0.50)
     • 🎯 valence excellent match (0.49 ≈ 0.50)
     • 🎯 acousticness excellent match (0.22 ≈ 0.50)

======================================================================
```

**Analysis**: The High-Energy Pop profile ranks songs aggressively by energy match. "Sunrise City" wins with both genre and mood matches, plus strong energy/danceability alignment (0.82 energy is close to target 0.9). Note that items #4 and #5 lack explicit mood/genre matches but are still recommended due to excellent feature matches—showing the system's ability to discover songs outside strict categorical boundaries.

---

### Profile 2: Chill Lofi Listener
**Preferences**: `genre=lofi, mood=calm, energy=0.2`  
**Context**: Relaxing, low-energy lofi beats for focus and relaxation

```
======================================================================
🎵  TOP RECOMMENDATIONS (5 songs)
======================================================================

1. Midnight Coding - LoRoom
   Score: 6.09/7.8 │███████████████████████░░░░░░░│ 78%
   Why you'll love it:
     • 🎯 energy excellent match (0.42 ≈ 0.20)
     • 🎯 danceability excellent match (0.62 ≈ 0.50)
     • 🎯 valence excellent match (0.56 ≈ 0.50)
     • 🎯 acousticness excellent match (0.71 ≈ 0.50)
     • 🎸 genre matches (lofi)

----------------------------------------------------------------------

2. Focus Flow - LoRoom
   Score: 6.08/7.8 │███████████████████████░░░░░░░│ 78%
   Why you'll love it:
     • 🎯 energy excellent match (0.40 ≈ 0.20)
     • 🎯 danceability excellent match (0.60 ≈ 0.50)
     • 🎯 valence excellent match (0.59 ≈ 0.50)
     • 🎯 acousticness excellent match (0.78 ≈ 0.50)
     • 🎸 genre matches (lofi)

----------------------------------------------------------------------

3. Library Rain - Paper Lanterns
   Score: 6.08/7.8 │███████████████████████░░░░░░░│ 78%
   Why you'll love it:
     • 🎯 energy excellent match (0.35 ≈ 0.20)
     • 🎯 danceability excellent match (0.58 ≈ 0.50)
     • 🎯 valence excellent match (0.60 ≈ 0.50)
     • ✓ acousticness good match (0.86)
     • 🎸 genre matches (lofi)

----------------------------------------------------------------------

4. Whispers in the Rain - Indie Soul
   Score: 4.12/7.8 │███████████████░░░░░░░░░░░░░░░│ 53%
   Why you'll love it:
     • 🎯 energy excellent match (0.35 ≈ 0.20)
     • 🎯 danceability excellent match (0.54 ≈ 0.50)
     • 🎯 valence excellent match (0.48 ≈ 0.50)
     • 🎯 acousticness excellent match (0.78 ≈ 0.50)

----------------------------------------------------------------------

5. Spacewalk Thoughts - Orbit Bloom
   Score: 4.06/7.8 │███████████████░░░░░░░░░░░░░░░│ 52%
   Why you'll love it:
     • 🎯 energy excellent match (0.28 ≈ 0.20)
     • 🎯 danceability excellent match (0.41 ≈ 0.50)
     • 🎯 valence excellent match (0.65 ≈ 0.50)
     • ✓ acousticness good match (0.92)

======================================================================
```

**Analysis**: The Chill Lofi profile demonstrates the system's strength in low-energy contexts. The top 3 songs are tightly clustered (all 6.08-6.09 score, 78%) because they're all lofi genre with similar low-energy features. Note that #4 (Whispers in the Rain) has no explicit mood/genre match but still scores 4.12/7.8 due to energy-valence alignment—showing the Gaussian similarity function rewards "close-but-not-exact" matches.

---

### Profile 3: Deep Intense Rock Listener
**Preferences**: `genre=rock, mood=intense, energy=0.85`  
**Context**: Heavy, powerful rock music with strong emotions

```
======================================================================
🎵  TOP RECOMMENDATIONS (5 songs)
======================================================================

1. Storm Runner - Voltline
   Score: 7.08/7.8 │███████████████████████████░░░│ 91%
   Why you'll love it:
     • 🎯 energy excellent match (0.91 ≈ 0.85)
     • 🎯 danceability excellent match (0.66 ≈ 0.50)
     • 🎯 valence excellent match (0.48 ≈ 0.50)
     • ✓ acousticness good match (0.10)
     • 🎭 mood matches (intense)
     • 🎸 genre matches (rock)

----------------------------------------------------------------------

2. Dancehall Energy - Kingston Sound
   Score: 4.93/7.8 │██████████████████░░░░░░░░░░░░│ 63%
   Why you'll love it:
     • 🎯 energy excellent match (0.86 ≈ 0.85)
     • ✓ danceability good match (0.89)
     • 🎯 valence excellent match (0.68 ≈ 0.50)
     • ✓ acousticness good match (0.16)
     • 🎭 mood matches (intense)

----------------------------------------------------------------------

3. Bass Drop Thunder - DJ Impulse
   Score: 4.90/7.8 │██████████████████░░░░░░░░░░░░│ 63%
   Why you'll love it:
     • 🎯 energy excellent match (0.95 ≈ 0.85)
     • ✓ danceability good match (0.91)
     • 🎯 valence excellent match (0.65 ≈ 0.50)
     • ✓ acousticness good match (0.12)
     • 🎭 mood matches (intense)

----------------------------------------------------------------------

4. Neon Mambo - Havana Nights
   Score: 4.90/7.8 │██████████████████░░░░░░░░░░░░│ 63%
   Why you'll love it:
     • 🎯 energy excellent match (0.89 ≈ 0.85)
     • ✓ danceability good match (0.88)
     • 🎯 valence excellent match (0.72 ≈ 0.50)
     • ✓ acousticness good match (0.09)
     • 🎭 mood matches (intense)

----------------------------------------------------------------------

5. Gym Hero - Max Pulse
   Score: 4.85/7.8 │██████████████████░░░░░░░░░░░░│ 62%
   Why you'll love it:
     • 🎯 energy excellent match (0.93 ≈ 0.85)
     • ✓ danceability good match (0.88)
     • 🎯 valence excellent match (0.77 ≈ 0.50)
     • ✓ acousticness good match (0.05)
     • 🎭 mood matches (intense)

======================================================================
```

**Analysis**: The Deep Intense Rock profile shows a massive gap between #1 (7.08/7.8, 91%) and the rest (4.85-4.93, 62-63%). This is because "Storm Runner" is the only song matching **all four core criteria** (genre=rock, mood=intense, high energy, low acousticness). The lower-ranked songs match mood and energy but lack the genre match. This reveals a potential bias: the genre weight (2.0) is so heavy that songs lacking genre match struggle to score well, even with excellent feature alignment.

---

## Adversarial Testing: Edge Cases & Robustness

To ensure the recommender system is robust, we tested it with four **adversarial/edge-case profiles** designed to expose potential weaknesses or unexpected behavior. These profiles test how the system handles conflicting preferences, extreme values, and non-standard mood categories.

### Test 1: Contradictory Preferences
**Profile**: `genre=rock, mood=happy, energy=0.1`  
**Challenge**: Can the system handle conflicting signals—rock (intense) with happy mood (upbeat) and very low energy (chill)?

```
📊 ADVERSARIAL PROFILE: Contradictory Preferences
   Description: Conflicting preferences: happy mood + rock genre + very low energy
   Preferences: {'genre': 'rock', 'mood': 'happy', 'energy': 0.1}

======================================================================
🎵  TOP RECOMMENDATIONS (5 songs)
======================================================================

1. Storm Runner - Voltline
   Score: 5.41/7.8 │████████████████████░░░░░░░░░░│ 69%
   Why you'll love it:
     • 🎯 danceability excellent match (0.66 ≈ 0.50)
     • 🎯 valence excellent match (0.48 ≈ 0.50)
     • ✓ acousticness good match (0.10)
     • 🎸 genre matches (rock)

----------------------------------------------------------------------

2. Rooftop Lights - Indigo Parade
   Score: 4.48/7.8 │█████████████████░░░░░░░░░░░░░│ 57%
   Why you'll love it:
     • 🎯 danceability excellent match (0.82 ≈ 0.50)
     • 🎯 valence excellent match (0.81 ≈ 0.50)
     • 🎯 acousticness excellent match (0.35 ≈ 0.50)
     • 🎭 mood matches (happy)

----------------------------------------------------------------------

3. Sunrise City - Neon Echo
   Score: 4.37/7.8 │████████████████░░░░░░░░░░░░░░│ 56%
   Why you'll love it:
     • 🎯 danceability excellent match (0.79 ≈ 0.50)
     • ✓ valence good match (0.84)
     • 🎯 acousticness excellent match (0.18 ≈ 0.50)
     • 🎭 mood matches (happy)

----------------------------------------------------------------------

4. Whispers in the Rain - Indie Soul
   Score: 4.07/7.8 │███████████████░░░░░░░░░░░░░░░│ 52%
   Why you'll love it:
     • 🎯 energy excellent match (0.35 ≈ 0.10)
     • 🎯 danceability excellent match (0.54 ≈ 0.50)
     • 🎯 valence excellent match (0.48 ≈ 0.50)
     • 🎯 acousticness excellent match (0.78 ≈ 0.50)

----------------------------------------------------------------------

5. Spacewalk Thoughts - Orbit Bloom
   Score: 4.03/7.8 │███████████████░░░░░░░░░░░░░░░│ 52%
   Why you'll love it:
     • 🎯 energy excellent match (0.28 ≈ 0.10)
     • 🎯 danceability excellent match (0.41 ≈ 0.50)
     • 🎯 valence excellent match (0.65 ≈ 0.50)
     • ✓ acousticness good match (0.92)

======================================================================
```

**Finding**: The system prioritizes genre match (#1 Storm Runner scores 5.41 for matching rock) even though it contradicts the happy mood + low energy combination. Items #2-3 compromise by prioritizing mood/valence over genre. This shows **genre weight dominates even when contextually inappropriate**.

---

### Test 2: Extremely Picky (All Extremes)
**Profile**: `genre=jazz, mood=sad, energy=0.95`  
**Challenge**: Can the system handle an extreme energy preference (0.95 = very high) combined with a sad mood and a rare genre (jazz)?

```
📊 ADVERSARIAL PROFILE: Extremely Picky (All Extremes)
   Description: Extreme energy (0.95) with sad mood and rare jazz genre
   Preferences: {'genre': 'jazz', 'mood': 'sad', 'energy': 0.95}

======================================================================
🎵  TOP RECOMMENDATIONS (5 songs)
======================================================================

1. Coffee Shop Stories - Slow Stereo
   Score: 5.67/7.8 │█████████████████████░░░░░░░░░│ 73%
   Why you'll love it:
     • ✓ energy good match (0.37)
     • 🎯 danceability excellent match (0.54 ≈ 0.50)
     • 🎯 valence excellent match (0.71 ≈ 0.50)
     • ✓ acousticness good match (0.89)
     • 🎸 genre matches (jazz)

----------------------------------------------------------------------

2. Storm Runner - Voltline
   Score: 4.08/7.8 │███████████████░░░░░░░░░░░░░░░│ 52%
   Why you'll love it:
     • 🎯 energy excellent match (0.91 ≈ 0.95)
     • 🎯 danceability excellent match (0.66 ≈ 0.50)
     • 🎯 valence excellent match (0.48 ≈ 0.50)
     • ✓ acousticness good match (0.10)

----------------------------------------------------------------------

3. Neon Nights - Synthwave Masters
   Score: 4.04/7.8 │███████████████░░░░░░░░░░░░░░░│ 52%
   Why you'll love it:
     • 🎯 energy excellent match (0.81 ≈ 0.95)
     • 🎯 danceability excellent match (0.76 ≈ 0.50)
     • 🎯 valence excellent match (0.51 ≈ 0.50)
     • 🎯 acousticness excellent match (0.19 ≈ 0.50)

----------------------------------------------------------------------

4. Night Drive Loop - Neon Echo
   Score: 4.04/7.8 │███████████████░░░░░░░░░░░░░░░│ 52%
   Why you'll love it:
     • 🎯 energy excellent match (0.75 ≈ 0.95)
     • 🎯 danceability excellent match (0.73 ≈ 0.50)
     • 🎯 valence excellent match (0.49 ≈ 0.50)
     • 🎯 acousticness excellent match (0.22 ≈ 0.50)

----------------------------------------------------------------------

5. Rising Sun - Trap Collective
   Score: 4.00/7.8 │███████████████░░░░░░░░░░░░░░░│ 51%
   Why you'll love it:
     • 🎯 energy excellent match (0.72 ≈ 0.95)
     • 🎯 danceability excellent match (0.71 ≈ 0.50)
     • 🎯 valence excellent match (0.74 ≈ 0.50)
     • 🎯 acousticness excellent match (0.31 ≈ 0.50)

======================================================================
```

**Finding**: The only jazz match (#1) scores 5.67 despite having **terrible energy alignment** (0.37 vs 0.95 target—a massive mismatch!). The system doesn't penalize the genre weight by the energy error, showing that **genre matching can override feature misalignment**. Items #2-5 have better energy fits (0.72-0.91) but no genre match, so they score lower. This reveals a critical bias: rare genres get a "free pass" on feature accuracy.

---

### Test 3: Impossible Combo
**Profile**: `genre=lofi, mood=intense, energy=0.9`  
**Challenge**: Lofi is inherently chill (low energy), but this profile requests high-energy intense lofi—a genre/mood mismatch.

```
📊 ADVERSARIAL PROFILE: Impossible Combo
   Description: High-energy intense lofi (lofi is typically chill, not intense)
   Preferences: {'genre': 'lofi', 'mood': 'intense', 'energy': 0.9}

======================================================================
🎵  TOP RECOMMENDATIONS (5 songs)
======================================================================

1. Midnight Coding - LoRoom
   Score: 5.87/7.8 │██████████████████████░░░░░░░░│ 75%
   Why you'll love it:
     • ✓ energy good match (0.42)
     • 🎯 danceability excellent match (0.62 ≈ 0.50)
     • 🎯 valence excellent match (0.56 ≈ 0.50)
     • 🎯 acousticness excellent match (0.71 ≈ 0.50)
     • 🎸 genre matches (lofi)

----------------------------------------------------------------------

2. Focus Flow - LoRoom
   Score: 5.83/7.8 │██████████████████████░░░░░░░░│ 75%
   Why you'll love it:
     • ✓ energy good match (0.40)
     • 🎯 danceability excellent match (0.60 ≈ 0.50)
     • 🎯 valence excellent match (0.59 ≈ 0.50)
     • 🎯 acousticness excellent match (0.78 ≈ 0.50)
     • 🎸 genre matches (lofi)

----------------------------------------------------------------------

3. Library Rain - Paper Lanterns
   Score: 5.74/7.8 │██████████████████████░░░░░░░░│ 74%
   Why you'll love it:
     • ✓ energy good match (0.35)
     • 🎯 danceability excellent match (0.58 ≈ 0.50)
     • 🎯 valence excellent match (0.60 ≈ 0.50)
     • ✓ acousticness good match (0.86)
     • 🎸 genre matches (lofi)

----------------------------------------------------------------------

4. Storm Runner - Voltline
   Score: 5.08/7.8 │███████████████████░░░░░░░░░░░│ 65%
   Why you'll love it:
     • 🎯 energy excellent match (0.91 ≈ 0.90)
     • 🎯 danceability excellent match (0.66 ≈ 0.50)
     • 🎯 valence excellent match (0.48 ≈ 0.50)
     • ✓ acousticness good match (0.10)
     • 🎭 mood matches (intense)

----------------------------------------------------------------------

5. Dancehall Energy - Kingston Sound
   Score: 4.93/7.8 │██████████████████░░░░░░░░░░░░│ 63%
   Why you'll love it:
     • 🎯 energy excellent match (0.86 ≈ 0.90)
     • ✓ danceability good match (0.89)
     • 🎯 valence excellent match (0.68 ≈ 0.50)
     • ✓ acousticness good match (0.16)
     • 🎭 mood matches (intense)

======================================================================
```

**Finding**: The system strongly recommends lofi songs (5.74-5.87 score, 74-75%) **despite ignoring the energy preference entirely** (all have energy 0.35-0.42, nowhere near 0.9). Genre weight is worth ~2.0 points, while a full 0.5-point energy mismatch costs almost nothing. Item #4 (Storm Runner) with energy 0.91 and mood match only scores 5.08, showing that **genre match >> energy + mood match**. This is a critical weakness.

---

### Test 4: Niche Mood (Reflective)
**Profile**: `genre=pop, mood=reflective, energy=0.5`  
**Challenge**: "Reflective" is not a standard mood in the catalog (which has happy, calm, sad, intense). How does the system degrade when mood doesn't exist?

```
📊 ADVERSARIAL PROFILE: Niche Mood (Reflective)
   Description: Non-standard mood 'reflective' (system may not have this mood in catalog)
   Preferences: {'genre': 'pop', 'mood': 'reflective', 'energy': 0.5}

======================================================================
🎵  TOP RECOMMENDATIONS (5 songs)
======================================================================

1. Sunrise City - Neon Echo
   Score: 5.80/7.8 │██████████████████████░░░░░░░░│ 74%
   Why you'll love it:
     • 🎯 energy excellent match (0.82 ≈ 0.50)
     • 🎯 danceability excellent match (0.79 ≈ 0.50)
     • ✓ valence good match (0.84)
     • 🎯 acousticness excellent match (0.18 ≈ 0.50)
     • 🎸 genre matches (pop)

----------------------------------------------------------------------

2. Gym Hero - Max Pulse
   Score: 5.62/7.8 │█████████████████████░░░░░░░░░│ 72%
   Why you'll love it:
     • ✓ energy good match (0.93)
     • ✓ danceability good match (0.88)
     • 🎯 valence excellent match (0.77 ≈ 0.50)
     • ✓ acousticness good match (0.05)
     • 🎸 genre matches (pop)

----------------------------------------------------------------------

3. Jazz Blue - New York Trio
   Score: 4.17/7.8 │████████████████░░░░░░░░░░░░░░│ 53%
   Why you'll love it:
     • 🎯 energy excellent match (0.52 ≈ 0.50)
     • 🎯 danceability excellent match (0.58 ≈ 0.50)
     • 🎯 valence excellent match (0.48 ≈ 0.50)
     • 🎯 acousticness excellent match (0.68 ≈ 0.50)

----------------------------------------------------------------------

4. Midnight Coding - LoRoom
   Score: 4.14/7.8 │███████████████░░░░░░░░░░░░░░░│ 53%
   Why you'll love it:
     • 🎯 energy excellent match (0.42 ≈ 0.50)
     • 🎯 danceability excellent match (0.62 ≈ 0.50)
     • 🎯 valence excellent match (0.56 ≈ 0.50)
     • 🎯 acousticness excellent match (0.71 ≈ 0.50)

----------------------------------------------------------------------

5. Midnight Melancholy - Blue Notes Trio
   Score: 4.14/7.8 │███████████████░░░░░░░░░░░░░░░│ 53%
   Why you'll love it:
     • 🎯 energy excellent match (0.45 ≈ 0.50)
     • 🎯 danceability excellent match (0.64 ≈ 0.50)
     • 🎯 valence excellent match (0.42 ≈ 0.50)
     • 🎯 acousticness excellent match (0.72 ≈ 0.50)

======================================================================
```

**Finding**: When mood "reflective" doesn't match any song in the catalog (no mood="reflective" songs exist), the system **gracefully degrades by ignoring the mood score entirely** and relying on genre + audio features. Pop genre match (#1, #2) gets the highest scores (5.80, 5.62), while items #3-5 with no genre match score lower (4.14-4.17). This is **graceful degradation**, but it means a non-existent mood preference silently fails—the user gets recommendations without the mood they requested.

---

## System Findings & Insights

### Summary of Key Observations

Across the seven test profiles (3 standard + 4 adversarial), the system revealed several consistent patterns:

1. **Genre Weight Dominates Everything** (2.0 / 7.8 = 25.6% of max score)
   - Songs matching the requested genre get massive boosts, even when other preferences are violated.
   - Example: Test 2 (Extremely Picky) recommends "Coffee Shop Stories" (5.67 score) with energy 0.37 when the user wants 0.95, simply because it's jazz.
   - Example: Test 3 (Impossible Combo) recommends lofi songs with energy 0.4 when the user wants 0.9, purely for genre matching.
   - **Implication**: The system is conservative—it filters by genre first, then tunes by features. This works for familiar genres but fails when users want cross-genre discovery.

2. **Energy Mismatches Are Forgiving**
   - The Gaussian similarity function with k=0.5 rewards "close-but-not-exact" energy matches heavily.
   - Example: Test 2 has a 0.58-point energy gap (0.95 target vs 0.37 actual) but still scores 5.67/7.8.
   - Example: Test 3 has a 0.5-point energy gap (0.9 target vs 0.4 actual) but scores 5.87/7.8.
   - **Implication**: Energy preferences are suggestions, not requirements. Good for serendipity, bad for users with strict energy needs.

3. **Mood Matching is Binary (All-or-Nothing)**
   - Exact mood matches add 1.0 point; non-matches add 0.0.
   - Example: Test 4 (Niche Mood) loses 1.0 points because "reflective" mood doesn't exist in the catalog.
   - **Implication**: Mood categories need to be curated and consistent. Semantically similar moods (calm, chill, relaxing) are treated as completely different.

4. **High-Ranked Songs Often Lack Expected Features**
   - Even in standard profiles, top-ranked songs sometimes miss mood or valence alignment.
   - Example: Profile 1 (High-Energy Pop) has #2 (Gym Hero) with no explicit mood match, and #4-5 with no genre or mood match.
   - **Implication**: The algorithm is lenient—genre + energy alignment can overcome missing mood/valence. This allows discovery but may surprise users.

5. **Catalog Size Matters**
   - With only 30 songs, there's limited diversity. If you want jazz with energy 0.95, only one song matches the genre.
   - **Implication**: Results would change dramatically with more songs. Biases might amplify or diminish depending on genre distribution.

### When the System Works Well

- **Clear, standard preferences**: If a user says "pop, happy, high energy," the system finds great matches.
- **Genre-centric users**: Users who prioritize genre first will be satisfied.
- **Feature-balanced catalogs**: If your song catalog is well-distributed across moods/energy, recommendations are diverse.

### When the System Struggles

- **Conflicting preferences**: "rock + happy + low energy" causes the system to compromise in suboptimal ways.
- **Rare genres with extreme features**: If you want a rare genre with non-typical audio features, you'll get poor matches.
- **Non-existent moods**: If the user's mood isn't in the catalog, the system silently loses 1.0 points per song.
- **Cross-genre discovery**: The heavy genre weight prevents exploring songs outside the favorite genre.

---

## Extending the Evaluation

### How to Add Your Own Profiles

You can easily add new user profiles to test different scenarios:

**1. For standard profiles**, edit `src/main.py`:
```python
user_profiles = {
    "Your Profile Name": {
        "genre": "your_genre",
        "mood": "your_mood",
        "energy": 0.5,  # 0.0 to 1.0
        "description": "Your profile description"
    },
    # ... more profiles
}
```

**2. For adversarial/edge-case profiles**, edit `src/adversarial_test.py`:
```python
adversarial_profiles = {
    "Your Edge Case": {
        "genre": "genre",
        "mood": "mood",
        "energy": 0.5,
        "description": "What are you testing?"
    },
    # ... more profiles
}
```

**3. Run your profiles**:
```bash
python -m src.main              # For standard profiles
python src/adversarial_test.py  # For adversarial profiles
```

### Profile Design Tips

- **Standard profiles** should represent real user archetypes (e.g., "Morning Workout", "Late Night Study")
- **Adversarial profiles** should challenge the system (e.g., conflicting values, rare genres, extreme feature values)
- Always include a `description` field explaining the profile's purpose
- Vary the `energy` (0.0 = low, 1.0 = high) and `mood` values to test different scenarios

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users
- Results from the standard profile evaluation (see System Evaluation section above)
- Results from the adversarial testing suite (see Adversarial Testing section above)

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



