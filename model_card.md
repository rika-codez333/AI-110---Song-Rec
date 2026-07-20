# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**SoundMatcher 1.0** — A proximity-based music recommender that scores songs by matching genre, mood, and audio features.

---

## 2. Goal / Task

This recommender suggests the top 5 songs that match a user's mood, favorite genre, and audio preferences (like energy and danceability). It's designed for users who can describe what they want: "I like pop music with happy mood and high energy." The system returns ranked recommendations with explanations for why each song was suggested.

---

## 3. Data Used

**Dataset**: 31 songs across 25 genres (pop, lofi, rock, jazz, K-pop, reggae, etc.)

**Moods**: 15 different moods represented (happy, intense, chill, peaceful, romantic, etc.)

**Audio Features**:
- Energy (0.22–0.95): How intense/powerful the song is
- Valence (0.42–0.86): How happy/positive it sounds
- Danceability (0.15–0.92): How groovy/rhythmic it is
- Tempo (60–152 BPM): How fast it plays
- Acousticness (0.05–0.94): How acoustic vs. electronic it is

**Limitation**: Most genres have only 1–3 songs, so recommendations get stuck within the same few songs. Rare moods (peaceful, romantic) are under-represented.

---

## 4. Algorithm Summary

**Step 1: Categorical Matching** (Genre & Mood)
- Genre match? Yes = +2.3 points. No = 0 points.
- Mood match? Yes = +1.0 points. No = −0.5 points (penalty).

**Step 2: Audio Feature Matching** (Proximity-based)
- For each numeric feature (energy, valence, etc.), the system measures how close the song is to the user's preference.
- A song with energy 0.91 matching user preference 0.9? Gets nearly full credit (1.2 points).
- A song with energy 0.5 when user wants 0.9? Gets partial credit (~0.92 points).
- This uses a bell-curve formula: `similarity = exp(-k × distance²)`. No song gets zero credit—even mismatches are viable.

**Step 3: Scoring**
- Sum all contributions: genre + mood + energy + danceability + valence + tempo + acousticness.
- Maximum possible score: 7.9 points.
- Rank all songs by score and return the top 5.

**Why This Design**: Genre and mood are "hard requirements" (you want pop, not rock). Audio features are "soft preferences" (you want high energy, but a lower-energy song can still work if genre matches).

---

## 5. Observed Behavior / Biases

**The Genre Filter Bubble**
If you like lofi music, you'll only see the 3 lofi songs in the catalog. Non-lofi songs score 60% lower. The system locks you into your preferred genre because:
- Genre weight (2.3) is much higher than other features (energy, mood, etc.)
- Each genre has only 1–3 songs, so there's nothing else like them
- Users can't discover "similar-sounding" music in different genres (like ambient music with the same low energy as lofi)

**Niche Moods Disappear**
Moods like "peaceful" and "romantic" appear only once or twice in the dataset. If you ask for these, the system returns songs but doesn't tell you it's struggling. There's no alert that your mood request is uncommon.

**Genre Matching is Binary**
Synthwave gets zero credit for being like synth pop or electronic music, even though they sound similar. The system only gives points for exact genre matches, not close matches. This limits cross-genre discovery.

**Why This Matters**
These biases aren't bugs—they're trade-offs. We made genre weight high on purpose to prevent rock songs from showing up in pop recommendations. But that same choice prevents a pop listener from discovering reggaeton or dance music (which have similar energy). You can't have both genre purity AND cross-genre discovery with just weights. 

---

## 6. Evaluation Process

**How We Tested It**

**Standard Profiles** (3 realistic user types):
- High-Energy Pop Listener (energy 0.9, happy mood, pop genre)
  - Got: Sunrise City, Gym Hero, Rooftop Lights, Storm Runner, Night Drive Loop
  - Check: Top 3 are all pop? Yes ✓. Does Gym Hero rank high despite "intense" mood? Yes, because energy matches well ✓
  
- Chill Lofi Listener (energy 0.2, calm mood, lofi genre)
  - Got: Library Rain, Focus Flow, Midnight Coding (all lofi)
  - Check: Are all recommendations lofi? Yes ✓. Is there a huge gap to non-lofi songs? Yes, 60% score drop ✓
  
- Deep Intense Rock Listener (energy 0.85, intense mood, rock genre)
  - Got: Storm Runner (the only rock song), then dancehall/reggaeton with high energy
  - Check: Does rock song dominate? Yes ✓. Do fallback songs have intense mood? Yes ✓

**Edge Case Testing** (4 tricky profiles):
- Contradictory Preferences (happy rock + low energy) → System ranked rock high despite contradictions
- Extremely Picky (jazz + sad + very high energy) → Jazz song won on genre despite terrible energy fit
- Impossible Combo (lofi + intense + high energy) → Lofi songs ranked high despite energy mismatch
- Niche Mood (reflective genre) → System didn't warn that this mood is rare

**Key Finding**: The system works well when users have clear genre preferences. It struggles when:
- They want rare moods (peaceful, romantic)
- They ask for contradictory things (calm rock)
- They want cross-genre discovery

**Why "Gym Hero" Ranks #2 for Pop Listeners**
- User wants: Pop (genre), happy (mood), high energy (0.9)
- Gym Hero is: Pop (✓), intense mood (✗), energy 0.93 (✓✓)
- Score breakdown: +2.3 (genre) +1.2 (energy near-perfect) −0.5 (mood mismatch) = 3.0 base, then +1.7 from other features = 4.7 total
- Plain English: "This song is 85% what you asked for, with one compromise." Users accept this trade-off if they understand it.  

---

## 7. Intended Use and Non-Intended Use

**✅ What This System IS For:**
- Classroom projects and learning about recommendation algorithms
- Exploring how weights and scoring rules affect recommendations
- Understanding trade-offs between genre coherence and discovery
- Testing recommendation logic before building a real system
- Understanding why different users get different results

**❌ What This System is NOT For:**
- Real music streaming services (too few songs, not personalized to individual listening history)
- Making money or targeting users for ads
- Predicting what someone will like based on their demographics (age, culture, gender)
- Production systems without additional testing and validation
- Handling users with rare or niche tastes (dataset too small)

**Key Limitation**: This system works best for users with clear genre preferences. It will disappoint users who want:
- Cross-genre discovery
- Rare or niche moods (peaceful, reflective)
- Recommendations outside their favorite genre
- Constantly fresh suggestions (only 31 songs total)

---

## 8. Ideas for Improvement

**#1: Expand the Dataset**
Add 100+ more songs per genre. Right now, a lofi listener only sees 3 songs. With more songs, we could recommend different lofi songs instead of just the same 3 over and over.

**#2: Add Semantic Genre Similarity**
Use machine learning embeddings so synthwave gets partial credit for being similar to synth pop and electronic music. Right now it's binary—match or no match. Allowing "close matches" would fix the genre filter bubble.

**#3: Use Real User Behavior**
Track what users actually play, skip, and save. "Users who liked this song also enjoyed X" is much more powerful than asking users what they like. This would overcome the small dataset problem.

**Bonus Ideas** (if you keep developing):
- Add mood embeddings so "reflective" counts as similar to "calm"
- Penalize score cliffs (if songs #1 and #2 are 2+ points apart, it feels like "winner takes all")
- Test with real users to see if mood penalties actually make recommendations feel better
- Build a diversity-aware ranking that suggests more varied options instead of clustering around one sound


