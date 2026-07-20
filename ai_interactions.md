# AI Interactions Log

## Challenge 1: Add Advanced Song Features

**What task did you give the agent?**

Enhanced the song dataset and scoring logic to include 5 new complex attributes:
1. **Song Popularity** (0-100): Numeric score representing mainstream appeal
2. **Release Decade** (e.g., 2020s, 2010s): Temporal dimension for songs
3. **Detailed Mood Tags** (comma-separated): Multi-faceted mood descriptors beyond single word
4. **Artist Familiarity** (0-1): Score representing mainstream recognition of artist
5. **Production Quality** (0-1): Quantifies production depth and professional polish

**Prompts used:**

"Add 5 new complex attributes to the song CSV dataset. Update the Song and UserProfile dataclasses, the load_songs function, and the scoring logic to account for these new features. The new attributes should increase the max score from 7.9 to approximately 9.5."

**What did the agent generate or change?**

1. **data/songs.csv**: Added 5 new columns with realistic values for all 39 original songs, then expanded to 68 songs
2. **src/recommender.py**:
   - Updated Song dataclass to include new fields
   - Updated UserProfile dataclass with new preference fields (min_popularity, preferred_production_quality, prefer_artist_familiarity)
   - Updated load_songs() to parse new CSV fields
   - Enhanced score_song() to score popularity, production_quality, and artist_familiarity using Gaussian similarity
   - Updated weights to reflect new max_score of 9.5
3. **src/main.py**: Updated display_recommendations() max_score parameter from 7.9 to 9.5

**What did you verify or fix manually?**

- Manually reviewed CSV data to ensure popularity values were realistic (30-85 range) and release decades matched song era
- Verified that mood_tags were semantically aligned with the mood field (e.g., "happy" mood had "uplifting,energetic" tags)
- Ran the system end-to-end to confirm scores were in expected range (~4-9 range) and that new attributes contributed measurably to recommendations
- Expanded dataset from 39 to 68 songs to add Caribbean and other underrepresented genres while maintaining data consistency

**Dataset Expansion Result:**
- Original: 39 songs across 15 genres
- Enhanced: 68 songs across 25+ genres including more hip-hop variants, electronic varieties, dance music, classical variants, and Caribbean sounds

---

## Challenge 2: Create Multiple Scoring Modes (Strategy Pattern)

**Which design pattern did you use?**

**Strategy Pattern** - Defines a family of algorithms (scoring strategies), encapsulates each one, and makes them interchangeable.

**How did AI help you brainstorm or implement it?**

Created a comprehensive Strategy pattern implementation with:
1. Abstract base class `ScoringStrategy` with score_song() method
2. Five concrete strategy implementations:
   - **BalancedStrategy**: Default, equal weights across all features
   - **GenreFirstStrategy**: Doubles genre weight to 4.0 (heavily prioritizes genre matching)
   - **MoodFirstStrategy**: Triples mood weight to 2.5 (emotional alignment first)
   - **EnergyFocusedStrategy**: Doubles energy/danceability to 2.5 (workout/party playlists)
   - **QualityFirstStrategy**: Boosts production_quality and artist_familiarity (audiophile preference)
   - **PopularityDrivenStrategy**: Doubles popularity and familiarity weights (mainstream focus)

**How does the pattern appear in your final code?**

Location: `src/recommender.py` (lines ~52-230)

- **Strategy interface**: `ScoringStrategy` abstract base class
- **Concrete strategies**: Six implementations (BalancedStrategy, GenreFirstStrategy, etc.)
- **Context**: `Recommender` class accepts optional `strategy` parameter in __init__() and recommend()
- **Usage in recommend()**: Dynamically selects strategy (lines ~307-310)
  ```python
  strategy_to_use = strategy or self.strategy
  score, _ = strategy_to_use.score_song(user_prefs, song_dict, k=tuning_param)
  ```

**Why Strategy Pattern?**
- **Flexibility**: Users can switch between different recommendation philosophies without changing core algorithm
- **Extensibility**: New strategies can be added by creating new classes without modifying existing code
- **Testability**: Each strategy can be tested independently
- **Separation of Concerns**: Weight tuning is isolated in strategy classes

---

## Challenge 3: Diversity and Fairness Logic

**What task did you give the agent?**

Implement a diversity penalty that prevents the recommender from suggesting too many songs from the same artist or genre in the top results. This ensures users get varied recommendations rather than multiple songs from a single artist or genre cluster.

**Prompts used:**

"Add a diversity penalty function that deducts points from a song's score if its artist or genre is already present in the top recommendations. The penalty should be configurable (e.g., -0.5 for duplicate artist, -0.2 for duplicate genre)."

**What did the agent generate or change?**

Created `apply_diversity_penalty()` function in `src/main.py` (lines ~78-105):
- Tracks seen artists and genres as it iterates through recommendations
- Applies configurable penalties for duplicate artists (-0.5 default) and genres (-0.2 default)
- Re-sorts recommendations after applying penalties
- Returns annotated recommendations with diversity notes showing which penalties were applied

**Implementation Details:**
```python
def apply_diversity_penalty(recommendations, penalty_per_artist=0.5, penalty_per_genre=0.2):
    """Apply diversity penalty to prevent too many songs from same artist/genre."""
```

**What did you verify or fix manually?**

- Tested that penalties are applied in correct order (first occurrence gets no penalty, second occurrence gets penalized)
- Verified re-sorting works correctly after adjusting scores
- Confirmed that diversity notes are accurately displayed (e.g., "(artist duplicate: -0.5)")
- Checked that penalties can prevent previously top-ranked songs from staying in top-5 if they're artist duplicates

**Example Scenario:**
Before diversity penalty:
- #1: Song A by Artist X (Score 8.5)
- #2: Song B by Artist X (Score 8.3) ← Duplicate artist
- #3: Song C by Genre Pop (Score 7.9)

After diversity penalty:
- #1: Song A by Artist X (Score 8.5)
- #2: Song C by Genre Pop (Score 7.9) ← Moved up, replaces duplicate
- #3: Song B by Artist X (Score 7.8) ← Penalized, score drops

---

## Challenge 4: Visual Summary Table

**What task did you give the agent?**

Create a formatted summary table that displays top recommendations in a clean, scannable format with:
- Song title and artist
- Score and percentage
- Genre and mood
- Top reason for recommendation
- All in a visually organized table format

**Prompts used:**

"Create a display function that shows recommendations as a formatted ASCII table with columns for rank, title, artist, score, genre, mood, and the top reason why each song was recommended. Ensure the table is readable in the terminal."

**What did the agent generate or change?**

Created `display_recommendations_table()` function in `src/main.py` (lines ~108-148):
- Formats recommendations as aligned columns
- Shows ranking (#), title/artist, score/percentage, genre/mood, and top reason
- Properly handles multi-line entries for readability
- Displays ===== separators for visual structure
- Integrated into main() to display after each recommendation set

**Table Format:**
```
========================================================================================================================
🎵 RECOMMENDATION SUMMARY TABLE
========================================================================================================================
#   Title (Artist)                      Score           Genre/Mood           Top Reason
------------------------------------------------------------------------------------------------------------------------
1   Focus Flow (LoRoom)                 7.31/9.5 (77%)  lofi/focused         🎯 energy excellent match
...
========================================================================================================================
```

**What did you verify or fix manually?**

- Verified column widths are adequate for typical song titles/artists without truncation
- Tested with longer titles to ensure proper wrapping/alignment
- Confirmed header and row separators display correctly
- Checked that score percentages are calculated correctly (score / 9.5 * 100)
- Verified top reason extraction pulls the first (most significant) reason from explanation list

---

## Integration & Testing

**How do all challenges work together?**

1. **Challenge 1 (Advanced Features)** → Enhanced scoring data
2. **Challenge 2 (Strategy Pattern)** → Multiple ranking modes on that enhanced data
3. **Challenge 3 (Diversity)** → Filter/adjust recommendations for variety
4. **Challenge 4 (Visual Table)** → Present results in scannable format

**End-to-End Flow:**
```
User Profile → Scoring Strategy → Diversity Penalty → Table Display
                ↓
          Multiple attributes scored
          (genre, mood, energy, popularity, quality, etc.)
```

**Files Modified:**
- `data/songs.csv`: 39 → 68 songs, added 5 new feature columns
- `src/recommender.py`: Strategy pattern, enhanced scoring, new Song/UserProfile fields
- `src/main.py`: Multiple strategies, diversity logic, table display

---

## Learnings & Design Decisions

**Why these 5 new attributes?**
- **Popularity**: Real recommenders use engagement metrics; popularity as a proxy
- **Release Decade**: Temporal signal for whether users prefer current vs. classic music
- **Mood Tags**: Single-word moods (happy, sad) are too coarse; tags enable semantic nuance
- **Artist Familiarity**: Users often prefer known artists; models mainstream bias explicitly
- **Production Quality**: Quality is subjective but measurable (dynamic range, clarity, mixing)

**Strategy Pattern Benefits:**
- Genre-First for users who strongly identify with a genre (metal fans, K-pop fans)
- Mood-First for context-based recommendations (workout playlist vs. sleep playlist)
- Energy-Focused for specific use cases (gym, party) where energy matters most
- Quality-First for audiophiles who care about mixing/production
- Popularity-Driven for mainstream discovery (opposite of serendipity)

**Diversity Penalty Rationale:**
- Prevents "algorithm repetition" where same artists dominate
- Encourages cross-artist discovery while respecting preferences
- Configurable penalties allow tuning for different risk appetites

---
