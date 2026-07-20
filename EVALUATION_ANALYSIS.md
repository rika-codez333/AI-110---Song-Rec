# Recommender System Evaluation: Musical Intuition Check

## Profile-by-Profile Subjective Analysis

### Profile 1: High-Energy Pop (energy=0.9, mood=happy)

**Top Recommendation: "Sunrise City - Neon Echo" (6.93/7.8, 89%)**

**Does it feel right?** ✅ YES
- A pop song with happy mood and high energy matching a pop/happy/high-energy user is exactly what you'd expect
- The score (89%) reflects that it hits most targets but isn't perfect on all features
- This feels intuitive and appropriate

**Top 5 breakdown:**
1. ✅ Sunrise City (pop, happy) — Perfect match, feels right
2. ✅ Gym Hero (pop, intense) — Same genre but different mood; energy still high (0.93) so makes sense
3. ⚠️ Rooftop Lights (indie pop, happy) — Genre mismatch but mood/feature match. Does an indie pop song really belong #3 for a pop listener?
4. ⚠️ Storm Runner (rock, intense) — ROCK song in pop recommendations. Scored 4.08/7.8 mainly due to energy (0.91) and danceability (0.66). Feels wrong for this profile.
5. ⚠️ Night Drive Loop (lofi, N/A) — Another non-pop track, barely different score from #4

**Intuition check:** First two feel right. After that, the diversity feels forced—the system is reaching for any high-energy song even if it's wrong for a pop listener.

---

### Profile 2: Chill Lofi (energy=0.2, mood=calm)

**Top Recommendation: "Midnight Coding - LoRoom" (6.09/7.8, 78%)**

**Does it feel right?** ✅ YES
- Lofi beats, low energy, and "Coding" title suggest focus/chill context
- For a lofi listener, this is exactly what you'd want
- Score (78%) seems reasonable—not perfect but very good

**Top 5 breakdown:**
1. 6.09 — Midnight Coding
2. 6.08 — Focus Flow
3. 6.08 — Library Rain
4. 4.12 — Whispers in the Rain
5. 4.06 — Spacewalk Thoughts

**Critical observation:** Items #1-3 are **suspiciously identical in score** (6.08-6.09). This suggests:
- All three songs are lofi + similar low energy (0.35-0.42)
- Genre match (2.0 points) is the dominant factor
- After that, audio features (danceability, valence, acousticness) differ only slightly
- Result: Three functionally identical recommendations

**Intuition check:** ✅ Yes, these are all good chill lofi beats, BUT they feel repetitive. A real user might ask: "Why three almost-identical songs?" The clustering reveals limited diversity in the lofi catalog.

---

### Profile 3: Deep Intense Rock (energy=0.85, mood=intense)

**Top Recommendation: "Storm Runner - Voltline" (7.08/7.8, 91%)**

**Does it feel right?** ✅ YES
- Rock song with intense mood and high energy—exactly what a rock listener wants
- Score (91%) is the highest across all profiles, suggesting a near-perfect match
- This feels very right

**Top 5 breakdown:**
1. 7.08 — Storm Runner (rock, intense)
2. 4.93 — Dancehall Energy (NO rock genre)
3. 4.90 — Bass Drop Thunder (NO rock genre)
4. 4.90 — Neon Mambo (NO rock genre)
5. 4.85 — Gym Hero (NO rock genre)

**🚨 MASSIVE RED FLAG:** There's a **2.15-point cliff** between #1 (7.08) and #2 (4.93).
- #1 has rock genre match (+2.0) AND intense mood (+1.0) AND high energy (~1.4)
- #2-5 have NO rock genre match (0 points), but DO have intense mood (+1.0) and good energy
- So each loses the full 2.0 genre bonus

**Intuition check:** ⚠️ PROBLEMATIC
- If a rock listener plays "Storm Runner" and wants more rock songs, they'd expect songs #2-5 to be rock-adjacent
- Instead, they get Dancehall, Electronic/EDM, and Latin beats
- These are *musically incompatible* with rock but score high due to energy/mood
- **This feels very wrong**—the recommendations break genre coherence

---

## Cross-Profile Pattern Analysis

### Song "Storm Runner" appears 5 times in top-5 recommendations:
1. High-Energy Pop (#4, 4.08/7.8) — Rock song for pop listener ⚠️
2. Deep Intense Rock (#1, 7.08/7.8) — Perfect match ✅
3. Contradictory Preferences (#1, 5.41/7.8) — Rock for rock listener ✅
4. Extremely Picky (#2, 4.08/7.8) — High energy salvages it
5. Impossible Combo (#4, 5.08/7.8) — Intense mood + high energy

**Pattern:** "Storm Runner" appears whenever a user wants high energy + intense mood, regardless of genre. This suggests the algorithm is discovering it as a "universally high-energy intense song" even when genre is different.

### Song "Sunrise City" appears 3 times:
1. High-Energy Pop (#1) — Perfect (pop + happy + high energy) ✅
2. Niche Mood (reflective/pop) (#1, 5.80/7.8) — Pop genre match ✅
3. Contradictory Preferences (rock) (#3, 4.37/7.8) — Wrong genre ⚠️

**Pattern:** Sunrise City is "reliably a strong pop recommendation" but shows up even when not the primary genre.

---

## Intuitive Verdicts

### What feels RIGHT ✅
- **Pop recommendations for pop listeners**: Sunrise City, Gym Hero rank appropriately high
- **Lofi recommendations for lofi listeners**: All three (Midnight Coding, Focus Flow, Library Rain) feel authentic
- **Rock recommendations for rock listeners**: Storm Runner is a perfect #1
- **Energy-driven cross-genre:** When energy is extremely important (0.95 in Extremely Picky profile), songs outside the preferred genre still make sense

### What feels WRONG ⚠️
- **Rock listeners get non-rock fallbacks**: #2-5 in Deep Intense Rock are Dancehall, EDM, Latin—not rock at all
- **Pop listeners get rock songs**: Storm Runner appears as #4 in High-Energy Pop, which feels forced
- **Lofi homogeneity**: Three nearly identical lofi songs cluster together, suggesting the algorithm doesn't differentiate between similar-genre songs
- **Genre cliff is too steep**: The 2.15-point drop from #1 to #2 in rock recommendations suggests genre weight (2.0) is too dominant relative to mood (1.0) and energy (1.4)
- **Mood irrelevance in some cases**: In Contradictory Preferences (rock + happy + energy 0.1), "Storm Runner" ranks #1 despite being the most tonally opposite song for that combination

---

## Specific Hypothesis: Why "Storm Runner" Dominates

Looking at the data:
- "Storm Runner" has energy=0.91, danceability=0.66, valence=0.48 (moderate sad-to-neutral)
- It appears as top-5 whenever a user wants:
  - High energy (0.8+)
  - Intense mood
  - OR any combination where energy + danceability matters more than genre

**Question for the recommender:** Why does "Storm Runner" score so well in the "High-Energy Pop" profile when it's explicitly rock (genre mismatch = -2.0)? 
- It must be winning on energy alone
- Despite genre mismatch, features (0.91 energy, 0.66 danceability) outweigh the genre penalty
- This suggests numeric features are weighted too heavily relative to categorical constraints

---

## Proposed Issues

1. **Genre weight (2.0) creates cliffs, not guidance**
   - A rock listener wants rock recommendations, but loses 2.0 points per non-rock song
   - This creates a "hard constraint" vibe even though mood/energy can compensate
   - Real recommendation systems use genre as *flavor*, not a *deal-breaker*

2. **Energy weight (1.4) is nearly as important as genre (2.0)**
   - Energy is 70% of genre importance
   - This means "high energy" can trump "right genre"
   - Result: Storm Runner appears in pop recommendations

3. **Dataset is too small to support genre diversity**
   - Only 1-3 songs per genre in a 30-song catalog
   - Once the top song per genre is found, fallbacks are drastically lower quality
   - Real systems have 100K+ songs per genre to provide variety

4. **Mood categorical matching loses semantic information**
   - "reflective" ≠ "sad" even though they're similar
   - Niche Mood profile loses 1.0 points per recommendation due to non-existent mood
   - System should use mood *similarity* not mood *equality*

---

---

## AI Assistant's Mathematical Analysis

I asked an AI coding assistant to explain the scoring breakdowns and provide specific math for why "Storm Runner" ranks #4 in the High-Energy Pop profile despite being a rock song.

### Key Finding #1: Energy Weight Dominates

**Storm Runner (rock) in High-Energy Pop profile:**
```
Genre:        rock ≠ pop           → 0.000 (MISS)
Mood:         intense ≠ happy      → 0.000 (MISS)
Energy:       0.91 ≈ 0.90 (Δ²=0.0001)  → 1.4 × exp(-0.0001) = 1.400 ✓✓✓
Danceability: 0.66 ≈ 0.75 (Δ²=0.0081)  → 1.2 × 0.9919 = 1.190
Valence:      0.48 vs 0.80 (Δ²=0.1024) → 1.0 × 0.9027 = 0.903
Acousticness: 0.10 ≈ 0.20 (Δ²=0.01)    → 0.6 × 0.9900 = 0.594
────────────────────────────────────────
TOTAL: 4.087 / 7.8 (52.3%)
```

**The problem:** The rock song loses 2.0 points for genre mismatch BUT gains 4.087 from audio features alone. Result: a net positive 4.087 score, high enough to rank #4 in a 30-song dataset.

**Why:** Energy weight (1.4) is **70% of genre weight** (2.0). When Storm Runner has a near-perfect energy match (0.91 vs 0.90 target), the Gaussian function gives exp(-0.0001) ≈ 0.9999 (nearly perfect), contributing **1.4 points** (18% of max score) on a single feature.

### Key Finding #2: Lofi Clustering is Healthy

The three lofi songs (Midnight Coding, Library Rain, Focus Flow) score 6.78–7.19 because:
- All get +2.0 for genre match
- All get +1.0 for mood match (or lose it like Focus Flow)
- All have similar audio features (low energy, high acousticness)

This **is not a bug**—it correctly identifies them as a tier of similarly-good matches. The 0.4-point spread reflects real differences (mood match, exact energy match, etc.).

### Key Finding #3: The Genre Weight Misconception

The assistant tested reducing genre weight from 2.0 to 1.5 or 1.0. **Result:** Storm Runner's score doesn't improve for pop listeners because:
- Reducing genre doesn't penalize rock songs; it just removes the bonus from genre matches
- The audio features still sum to 4.087
- The gap between "genre match" and "genre miss" narrows, but the rock song is still competitive

**Conclusion:** Genre weight is actually fine. **Energy weight is the real problem.**

### Key Finding #4: The Real Issue is Missing Mood Penalties

Currently, a mood mismatch contributes **0 points** (flat penalty). Compare:
- Sunrise City (pop, happy): Gets +1.0 for mood match
- Storm Runner (rock, intense): Gets +0.0 for mood mismatch (no penalty, just no bonus)

**The asymmetry:** Hits are rewarded (+1.0), but misses are neutral (0.0). This allows songs with wrong mood to still score reasonably well if other features are strong.

---

## Proposed Weight Adjustments (Option C: Balanced Approach)

Based on the AI assistant's recommendation, here's a proposed fix:

### Current Weights
```
Genre:        2.0
Mood:         1.0 (match) / 0.0 (miss) ← ASYMMETRIC
Energy:       1.4
Danceability: 1.2
Valence:      1.0
Tempo:        0.6
Acousticness: 0.6
────────────
MAX SCORE:    7.8
```

### Proposed New Weights ⭐
```
Genre:        2.3 (slight increase for stronger genre coherence)
Mood:         1.0 (match) / -0.5 (PENALTY for miss) ← NOW SYMMETRIC
Energy:       1.2 (slight reduction to reduce dominance)
Danceability: 1.2
Valence:      1.0
Tempo:        0.6
Acousticness: 0.6
────────────
MAX SCORE:    7.9 (approximately)
```

### Impact Analysis

**Storm Runner (rock) in High-Energy Pop:**
```
CURRENT SCORING:
Energy: 1.4, Danceability: 1.19, Valence: 0.903, Acousticness: 0.594
+ Genre miss: 0, Mood miss: 0
= 4.087 / 7.8 (52.3%) ← Still competitive

NEW SCORING:
Energy: 1.2, Danceability: 1.19, Valence: 0.903, Acousticness: 0.594
+ Genre miss: 0, Mood miss: -0.5
= 3.387 / 7.9 (42.9%) ← Much less competitive ✓
```

**Perfect Pop Song (Sunrise City) in High-Energy Pop:**
```
CURRENT SCORING:
Genre match: 2.0, Mood match: 1.0, Energy: 1.4, ...
= 6.93 / 7.8 (89%)

NEW SCORING:
Genre match: 2.3, Mood match: 1.0, Energy: 1.2, ...
≈ 6.9+ / 7.9 (87%) ← Still highly ranked ✓
```

**Expected Effect:** Rock song drops from #4 to #7-10 in pop recommendations, improving genre coherence while maintaining pop songs at the top.

---

## Recommendation

The system **"feels right" for primary matches** (pop for pop listeners, lofi for lofi listeners) but **"feels wrong" for secondary recommendations** due to:
1. **Energy weight too high (1.4)** — allows wrong-genre songs to score well if energy matches
2. **Missing mood penalties** — mood mismatches have no downside, just no bonus
3. **Insufficient dataset diversity** — only 1-3 songs per genre make it hard to fill top-5 with coherent recommendations

### Proposed Fixes:
1. **Add mood mismatch penalty: -0.5 points** (fixes asymmetry)
2. **Reduce energy weight: 1.4 → 1.2** (reduces dominance of single features)
3. **Increase genre slightly: 2.0 → 2.3** (reinforces genre coherence)

These changes would make recommendations "feel more right" by ensuring secondary recommendations (positions #2-5) are genre-coherent, not just feature-aligned.

### Long-term Improvements:
1. Expand catalog to 100+ songs per genre to provide natural variety
2. Add semantic mood similarity (e.g., "reflective" ≈ "calm" via embedding distance)
3. Consider collaborative filtering signals (user behavior: plays, skips, saves) as weight adjustments
4. Implement diversity-aware ranking (penalize score cliffs between #1-#2)
