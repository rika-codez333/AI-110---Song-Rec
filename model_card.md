# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**SoundMatcher 1.0** — A proximity-based content filter for music recommendations powered by Gaussian similarity scoring.

---

## 2. Intended Use  

This recommender generates top-5 song suggestions based on user mood, genre, and audio feature preferences (energy, valence, danceability, etc.). It assumes users can articulate their taste in terms of a favorite genre and current mood, making it suitable for users seeking genre-aligned recommendations with audio feature nuance. **Intended for classroom exploration and research**, not production streaming platforms. The system uses a curated dataset of 31 songs and works best for users with clear genre preferences.

---

## 3. How the Model Works  

The system scores each song by combining two types of matching:

**Categorical Matching** (exact): Does the song's genre match your preference? Does its mood match? These are binary—either it matches (+points) or it doesn't (-0.5 points for mood mismatches).

**Audio Feature Proximity** (Gaussian): For numeric features like energy, valence, danceability, and acousticness, the system measures how close the song is to your preference using a bell-curve formula. A song with energy 0.91 that matches your 0.9 preference gets nearly full credit (0.9999). A song with energy 0.5 gets less credit (0.852). This rewards songs "close enough" to your taste without requiring exact matches.

**Scoring Formula**: Each song gets a final score (0–7.9 max) by summing contributions from: genre match (+2.3), mood match (+1.0) or mismatch (−0.5), energy proximity (+1.2), danceability (+1.2), valence (+1.0), tempo (+0.6), and acousticness (+0.6). The system ranks all songs by score and returns the top 5.

**Key Changes from Starter Logic**: Added mood penalties (−0.5) to discourage contextually wrong songs, increased genre weight from 2.0 to 2.3 for genre coherence, and reduced energy weight from 1.4 to 1.2 to prevent single features from dominating.

---

## 4. Data  

**Size**: 31 songs across 25 distinct genres (pop, lofi, rock, jazz, ambient, electronic, world music, K-pop, reggae, etc.).

**Genre Distribution**: Highly sparse—most genres have only 1–3 songs. Lofi is most represented (3 songs), followed by jazz, synthwave, indie, and others with 2 songs each. Rock, ambient, classical, folk, and many others have only 1 song.

**Mood Representation**: 15 distinct moods (happy, chill, intense, focused, relaxed, moody, peaceful, romantic, uplifting, contemplative, energetic, melancholic, inspiring, introspective, joyful). Some moods are rare: peaceful, romantic, inspiring, introspective, and joyful each appear only 1–2 times.

**Audio Features**: All songs include energy (0.22–0.95), valence (0.42–0.86), danceability (0.15–0.92), tempo (60–152 BPM), and acousticness (0.05–0.94), providing good numeric range.

**Changes Made**: Dataset was curated; no songs were added or removed during optimization.

**Missing Data**: The dataset lacks representation for niche moods (contemplative, introspective, peaceful) and many non-Western genres are undersampled. Users seeking rare mood-genre combinations will struggle due to limited options.

---

## 5. Strengths  

✅ **Genre-Matched Recommendations**: When a user specifies a clear genre preference, the system reliably returns songs from that genre in the top 3–5 (80% genre match rate). Rock listeners consistently see rock songs; pop listeners see pop.

✅ **Audio Feature Nuance**: The Gaussian similarity captures intuitive audio matching. A user wanting high energy (0.9) will prefer songs at 0.85–0.95 over songs at 0.5, and the scoring reflects this correctly.

✅ **Mood Transparency**: The system explicitly flags mood mismatches (⚠️ mood mismatch) so users understand why a technically "close" song may not feel contextually right.

✅ **Explainability**: Every recommendation includes reasons ("🎯 energy excellent match", "🎸 genre matches"), making it clear *why* a song scored high. Users can learn what the system values.

✅ **Handles Contradictory Preferences Well**: When a user specifies conflicting preferences (e.g., "happy mood but rock genre"), the system shows the trade-off explicitly without crashing or defaulting silently.

---

## 6. Limitations and Bias 

⚠️ **Genre Filter Bubble**: The system creates a strong filter bubble by prioritizing genre matches (weight 2.3) combined with a tiny dataset (1–3 songs per genre). A Chill Lofi listener always sees the same 3 lofi songs (scores 5.68–5.70) with zero cross-genre discovery—the next highest non-lofi song scores 3.43, a 60% drop. During sensitivity testing, when we *doubled* energy weight and halved genre weight, Storm Runner (a rock song) reappeared in pop recommendations (#4), demonstrating that the current genre dominance is a necessary—but strong—filter. Users are essentially locked into their preferred genre and struggle to discover similar-sounding songs in other genres. A user who loves "chill, low-energy music" gets trapped in lofi and never discovers ambient or classical alternatives with similar energy profiles.

⚠️ **Niche Mood Under-Representation**: Moods like "peaceful," "romantic," "inspiring," and "introspective" appear only once or twice in the dataset. Users requesting these rare moods don't receive explicit feedback that their request is uncommon—the system silently degrades, scoring mismatches at 0.0 (no penalty) instead of −0.5, reducing transparency. This creates a hidden failure mode.

⚠️ **Categorical Hard Matching**: Genre and mood are binary—either a song matches or it doesn't. A synthwave lover gets 0 credit for synth pop, indie pop, or electronic music, even though these are acoustically similar. This limits diversity and semantic understanding of genre relationships.

---

## 7. Evaluation  

**Standard Profiles Tested** (3 common user types):
- **High-Energy Pop**: energy=0.9, genre=pop, mood=happy → Correctly returns 5 pop songs; #1 is Sunrise City (7.03/7.9, 89%)
- **Chill Lofi**: energy=0.2, genre=lofi, mood=calm → Returns 3 lofi songs clustering tightly (5.68–5.70), #4 drops to 3.43 (non-lofi indie)
- **Deep Intense Rock**: energy=0.85, genre=rock, mood=intense → Correctly ranks Storm Runner #1 (7.18/7.9)

**Adversarial Profiles Tested** (4 edge cases revealing biases):
- **Contradictory Preferences** (happy mood + rock genre + low energy): System shows genre-mood trade-off transparently; genre wins
- **Extremely Picky** (jazz + sad + extreme energy 0.95): Jazz song wins on genre despite 0.58 energy mismatch, validating filter bubble
- **Impossible Combo** (lofi + intense + high energy): Lofi dominates despite mood mismatch; genre lock-in confirmed
- **Niche Mood** (pop + reflective + medium energy): System lacks "reflective" in catalog; gracefully degrades but silently

**Surprises & Key Findings**:
1. **Filter bubble discovered**: Genre weight was so dominant that a rock song ranked #4 for pop listeners before optimization, despite zero genre match. Fixed by increasing genre weight (+0.3) and adding mood penalties (−0.5).
2. **Energy dominance validated**: During sensitivity testing, doubling energy weight (1.2→2.4) and halving genre (2.3→1.15) immediately reintroduced Storm Runner into pop top-5 at score 4.58. This validated that balanced weights are necessary, not arbitrary.
3. **Mood mismatches matter**: Adding −0.5 penalty for mood mismatches reduced Storm Runner's score from 4.08 to 3.38 in pop context (18% drop), confirming asymmetric scoring was a critical bug.

**Metrics Tracked**:
- Genre coherence in top-5 (80% same-genre after optimization vs 60% before)
- Score clustering per genre (lofi: 5.68–5.70 tight; rock: 4.65–7.18 wide due to small N)
- Cross-genre discovery gap (non-preferred genres score 60–70% lower than preferred genre)

---

## 8. Future Work  

**Dataset Expansion** (high impact): Grow from 31 to 100+ songs per genre to enable secondary recommendations within genres. Currently, a lofi listener asking for alternative lofi songs sees only 3 options and tops out.

**Semantic Genre Similarity** (medium impact): Replace binary genre matching with embedding-based similarity. A synthwave lover could receive partial credit for synth pop, electronic, or darkwave—genres that are acoustically similar but categorically different.

**Mood Embeddings** (medium impact): Map moods to a similarity space so "reflective" ≈ "calm" and "peaceful" ≈ "serene" rather than binary mismatch. This would help users with niche moods find approximate matches.

**Diversity-Aware Ranking** (medium impact): Add a penalty for large score cliffs between recommendations. Currently, the #1 and #2 songs can differ by 2.5+ points, creating "winner-take-all" recommendations. A diversity constraint would surface more varied options.

**Collaborative Filtering Signals** (medium impact): Integrate user behavior (plays, skips, saves) to personalize beyond stated preferences. "Users who like your top pick also liked X" would overcome small dataset limitations.

**A/B Testing with Real Users** (high confidence): Validate that mood penalties and increased genre weights actually improve user satisfaction, not just mathematical metrics.

---

## 9. Personal Reflection  

This project revealed that recommendation systems are deceptively complex. The goal—return songs similar to user taste—sounds simple, but "similar" is ambiguous: similar in genre, mood, energy, danceability, or some combination? Our optimization process (Phase 7–8) showed that small weight changes (0.2 on energy, 0.3 on genre, −0.5 for mood) have outsized effects, and the "optimal" weights depend on what you're trying to solve. We fixed the Storm Runner problem (rock song ranking high for pop listeners) by reweighting, but this *tightened* the genre filter bubble—you can't solve both simultaneously with just weights. This taught me that recommender systems always involve trade-offs: genre coherence vs. cross-genre discovery, personalization vs. serendipity, explanation simplicity vs. nuance. The transparency aspect (showing *why* a song scored high with emoji and reasons) turned out to be as important as the scores themselves—users accept weird recommendations if the reasoning is clear. Finally, I learned that a 31-song dataset is too small to generalize; many real insights only emerged during adversarial testing, not with standard use cases. This makes me question how many production recommender systems go unvetted on edge cases.


