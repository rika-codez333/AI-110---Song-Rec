# Weight Adjustment Proposal: Improving Genre Coherence

## Executive Summary

**Current behavior:** The recommender produces high-quality primary matches but questionable secondary recommendations. Rock songs appear in pop playlists, and genre diversity is sacrificed for energy matching.

**Root cause:** Energy weight (1.4) is 70% of genre weight (2.0), and mood mismatches incur no penalty (0 points). This allows feature-aligned songs to score well even when contextually wrong.

**Proposed fix:** Three small weight adjustments that improve genre coherence while preserving feature-based discovery.

---

## Current vs Proposed Weights

| Feature | Current | Proposed | Change | Rationale |
|---------|---------|----------|--------|-----------|
| Genre | 2.0 | 2.3 | +0.3 | Reinforces genre coherence; prevents genre-less songs from ranking #2-3 |
| Mood (match) | 1.0 | 1.0 | — | Keep as-is |
| Mood (miss) | 0.0 | -0.5 | **NEW** | Penalize contextually wrong moods (e.g., intense when happy is desired) |
| Energy | 1.4 | 1.2 | -0.2 | Reduce dominance of single numeric features |
| Danceability | 1.2 | 1.2 | — | Keep as-is |
| Valence | 1.0 | 1.0 | — | Keep as-is |
| Tempo | 0.6 | 0.6 | — | Keep as-is |
| Acousticness | 0.6 | 0.6 | — | Keep as-is |
| **Max Score** | **7.8** | **~7.9** | +0.1 | Minimal impact; mood penalty adds asymmetry |

---

## Mathematical Validation

### Case 1: Pop Listener (High-Energy Pop)

**Problem song: Storm Runner (rock, intense)**

Current:
- Genre: 0 (no match)
- Mood: 0 (intense ≠ happy)
- Energy: 1.4 × exp(-0.0001) = 1.400
- Danceability + Valence + Acousticness: 2.687
- **Total: 4.087 / 7.8 (52%)** ← Still ranks #4 ⚠️

Proposed:
- Genre: 0 (no match)
- Mood: -0.5 (penalty for mismatch)
- Energy: 1.2 × exp(-0.0001) = 1.200
- Danceability + Valence + Acousticness: 2.687
- **Total: 3.387 / 7.9 (43%)** ← Drops to #7-10 ✅

**Winner song: Sunrise City (pop, happy)**

Current:
- Genre: 2.0 (match)
- Mood: 1.0 (match)
- Energy: 1.4 × exp(-0.0064) = 1.400
- Danceability + Valence + Acousticness: 1.133
- **Total: 6.933 / 7.8 (89%)** ← Ranks #1 ✅

Proposed:
- Genre: 2.3 (match)
- Mood: 1.0 (match)
- Energy: 1.2 × exp(-0.0064) = 1.200
- Danceability + Valence + Acousticness: 1.133
- **Total: 6.633 / 7.9 (84%)** ← Still ranks #1, minimal drop ✅

**Result:** Gap widens from 2.846 points (current) to 3.246 points (proposed). Genre-coherence improves.

### Case 2: Rock Listener (Deep Intense Rock)

**Primary song: Storm Runner (rock, intense)**

Current:
- Genre: 2.0 (match)
- Mood: 1.0 (match)
- Energy: 1.4 × exp(-0.0036) = 1.398
- Danceability + Valence + Acousticness: 1.701
- **Total: 7.099 / 7.8 (91%)** ← Ranks #1 ✅

Proposed:
- Genre: 2.3 (match)
- Mood: 1.0 (match)
- Energy: 1.2 × exp(-0.0036) = 1.200
- Danceability + Valence + Acousticness: 1.701
- **Total: 6.801 / 7.9 (86%)** ← Still #1, slightly lower ✅

**Secondary song: Dancehall Energy (dancehall, intense, no rock genre)**

Current:
- Genre: 0 (no match)
- Mood: 1.0 (match)
- Energy: 1.4 × exp(-0.0025) = 1.397
- Danceability + Valence + Acousticness: 2.572
- **Total: 4.969 / 7.8 (64%)** ← Ranks #2 ⚠️

Proposed:
- Genre: 0 (no match)
- Mood: 1.0 (match, no penalty here)
- Energy: 1.2 × exp(-0.0025) = 1.197
- Danceability + Valence + Acousticness: 2.572
- **Total: 4.769 / 7.9 (60%)** ← Still #2, but closer margin

**Note:** The cliff from #1 to #2 remains (2.032 points) because this song legitimately matches mood and energy. To improve rock recommendations, you'd need more rock songs in the dataset.

### Case 3: Lofi Listener (Chill Lofi)

**Clustering songs: Midnight Coding, Focus Flow, Library Rain**

Current scores: 6.09, 6.08, 6.08 (nearly identical)

Proposed Impact:
- All get +2.3 for genre (instead of +2.0): +0.3 points each
- Midnight Coding gets +1.0 for mood (unchanged)
- Focus Flow loses mood match, gets no penalty currently (stays 0)
- Library Rain gets +1.0 for mood (unchanged)
- Energy/other features adjust minimally

**Expected new scores:** 6.39, 6.36, 6.38 (same clustering, slightly higher)

**Result:** Clustering persists (good!) but all three songs rise together, improving user satisfaction. ✓

---

## Implementation Checklist

### Step 1: Update `recommender.py` Weights

```python
# In score_song() function, change:

# Current
weights = {
    'genre': 2.0,
    'mood': 1.0,
    'energy': 1.4,
    'danceability': 1.2,
    'valence': 1.0,
    'tempo': 0.6,
    'acousticness': 0.6
}

# Proposed
weights = {
    'genre': 2.3,
    'mood': 1.0,
    'energy': 1.2,
    'danceability': 1.2,
    'valence': 1.0,
    'tempo': 0.6,
    'acousticness': 0.6
}

# Also add mood penalty logic:
# If song.mood != user.mood and mood is specified:
#   score -= 0.5
```

### Step 2: Re-run Evaluations

```bash
# Run both evaluation scripts to see the impact
python -m src.main
python src/adversarial_test.py
```

### Step 3: Verify Results

Check for:
1. ✅ Do pop recommendations now exclude rock songs from top-5?
2. ✅ Do rock recommendations still have "Storm Runner" at #1?
3. ✅ Are lofi recommendations still clustering (diversity within genre)?
4. ✅ Do adversarial profiles degrade more gracefully (no cliff from #1 to #2)?

### Step 4: Document Findings

Update README with new results and explain the weight changes.

---

## Expected Outcomes

| Profile | Current | Expected After | Improvement |
|---------|---------|-----------------|------------|
| High-Energy Pop | Storm Runner #4 | Storm Runner #7-10 | Genre coherence ✓ |
| Deep Intense Rock | #2 cliff (2.15pt) | #2 cliff (~2.03pt) | Slight improvement |
| Chill Lofi | Clustering (healthy) | Clustering (healthy) | Preserved |
| Contradictory Prefs | Storm Runner #1 | Different song #1 | Better mood-aware |

---

## Risks & Mitigations

| Risk | Likelihood | Mitigation |
|------|------------|-----------|
| Pop recommendations become too rigid (no cross-genre discovery) | Low | -0.5 mood penalty only applies to exact mood mismatch; still allows energy-based discovery |
| Energy-based recommendations suffer | Medium | Energy weight drops from 1.4 to 1.2 (still significant); Gaussian ensures close matches score well |
| Lofi clustering breaks | Low | All lofi songs receive same genre/mood bonuses, so clustering should persist |
| Score distributions change significantly | Low | Max score only increases by 0.1; percentage scores remain comparable |

**Recommendation:** Test these weights on your dataset. If results don't feel better, you can revert or adjust energy back to 1.3 (middle ground).

---

## Next Steps

1. **Quick test (5 min):** Modify `recommender.py`, run evaluations, observe changes
2. **Deep analysis (10 min):** Compare before/after for High-Energy Pop and Deep Intense Rock profiles
3. **Documentation (5 min):** Update README with new results and methodology
4. **Optional:** Experiment with mood penalty values (-0.3, -0.7) to find optimal setting

---

## Questions for Further Refinement

- **What if mood penalty is too harsh?** Try -0.3 instead of -0.5
- **What if energy weight reduction breaks discovery?** Revert to 1.3 (middle ground)
- **What if genre weight increase over-prioritizes genre?** Reduce genre to 2.2 or 2.1
- **Should different moods have different penalties?** (e.g., sad→happy is worse than calm→happy) — not recommended for now, keep simple

Would you like me to implement these changes and test them?
