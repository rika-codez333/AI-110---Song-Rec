# Song Recommender Data Flow

## Overview
```mermaid
graph LR
    A["<b>INPUT</b><br/>User Preferences<br/>─────<br/>• favorite_genre<br/>• favorite_mood<br/>• target_energy<br/>• preferred_valence<br/>• preferred_danceability<br/>• preferred_tempo_bpm<br/>• preferred_acousticness"] 
    
    B["<b>THE LOOP</b><br/>Score Every Song<br/>─────<br/>Load CSV<br/>↓<br/>For each song:<br/>calculate score<br/>↓<br/>Sort by score<br/>↓<br/>Return top K"]
    
    C["<b>OUTPUT</b><br/>Top K Recommendations<br/>─────<br/>1. Song Title (score)<br/>2. Song Title (score)<br/>3. Song Title (score)<br/>4. Song Title (score)<br/>5. Song Title (score)"]
    
    A -->|pass prefs| B
    B -->|ranked list| C
    
    style A fill:#e0f2fe,stroke:#0891b2,stroke-width:2px,color:#1f2937
    style B fill:#fef3c7,stroke:#d97706,stroke-width:2px,color:#1f2937
    style C fill:#dbeafe,stroke:#0891b2,stroke-width:2px,color:#1f2937
```

---

## The Loop in Detail

### How Each Song Gets Scored

```mermaid
graph TD
    S["📥 SONG<br/>From CSV"]
    
    C["Calculate contributions:<br/>─────<br/>Categorical:<br/>• Genre match? +2.0 or 0<br/>• Mood match? +1.0 or 0<br/><br/>Numeric (Gaussian):<br/>• energy: 1.4 × exp(-k×d²)<br/>• danceability: 1.2 × exp(-k×d²)<br/>• valence: 1.0 × exp(-k×d²)<br/>• tempo_bpm: 0.6 × exp(-k×d²)<br/>• acousticness: 0.6 × exp(-k×d²)"]
    
    T["➕ SUM all<br/>contributions<br/>─────<br/>Max: 7.8"]
    
    O["💾 Store<br/>song, score,<br/>reasons"]
    
    S --> C
    C --> T
    T --> O
    
    style S fill:#e0f2fe,stroke:#0891b2,stroke-width:2px,color:#1f2937
    style C fill:#fef3c7,stroke:#d97706,stroke-width:2px,color:#1f2937
    style T fill:#fef3c7,stroke:#d97706,stroke-width:2px,color:#1f2937
    style O fill:#dbeafe,stroke:#0891b2,stroke-width:2px,color:#1f2937
```

---

## Scoring Algorithm: Option D (Balanced Discovery)

### Weights Table

| Feature | Weight | Scoring Method |
|---------|--------|-----------------|
| **Genre** | 2.0 | Exact match: +2.0 if match, 0 otherwise |
| **Mood** | 1.0 | Exact match: +1.0 if match, 0 otherwise |
| **Energy** | 1.4 | Gaussian: 1.4 × exp(-k × distance²) |
| **Danceability** | 1.2 | Gaussian: 1.2 × exp(-k × distance²) |
| **Valence** | 1.0 | Gaussian: 1.0 × exp(-k × distance²) |
| **Tempo (BPM)** | 0.6 | Gaussian: 0.6 × exp(-k × distance²) |
| **Acousticness** | 0.6 | Gaussian: 0.6 × exp(-k × distance²) |
| **MAX SCORE** | **7.8** | Sum of all contributions |

### Formula
```
TOTAL_SCORE = genre_contrib + mood_contrib + energy_contrib + 
              danceability_contrib + valence_contrib + 
              tempo_contrib + acousticness_contrib

Where:
  • genre_contrib = 2.0 if (song.genre == user.favorite_genre) else 0
  • mood_contrib = 1.0 if (song.mood == user.favorite_mood) else 0
  • numeric_contrib = weight × exp(-k × (user_pref - song_value)²)
  • k = tuning_param (0.5=loose/forgiving, 1.0=standard, 2.0=strict)
```

---

## Example: Full Flow for a High-Energy User

```mermaid
graph LR
    subgraph input["INPUT: User Profile"]
        U["genre: pop<br/>mood: intense<br/>energy: 0.93<br/>valence: 0.77"]
    end
    
    subgraph process["LOOP: Scoring"]
        P1["Song 1: Gym Hero<br/>─────<br/>genre: ✓ +2.0<br/>energy: 0.93 → +1.34<br/>valence: 0.77 → +0.98<br/>danceability: +0.89<br/>SUM = 5.21"]
        
        P2["Song 2: Library Rain<br/>─────<br/>genre: ✗ +0.0<br/>energy: 0.35 → +0.42<br/>valence: 0.40 → +0.15<br/>danceability: +0.08<br/>SUM = 0.65"]
        
        P3["...continue<br/>for all songs<br/>in CSV..."]
    end
    
    subgraph output["OUTPUT: Ranked"]
        O["1️⃣ Gym Hero (5.21)<br/>2️⃣ Storm Runner (3.83)<br/>3️⃣ Sunrise City (3.44)<br/>4️⃣ Rooftop Lights (3.12)<br/>5️⃣ Night Drive Loop (2.95)"]
    end
    
    input --> process
    process --> output
    
    style input fill:#e0f2fe,stroke:#0891b2,stroke-width:2px
    style process fill:#fef3c7,stroke:#d97706,stroke-width:2px
    style output fill:#dbeafe,stroke:#0891b2,stroke-width:2px
```

---

## Key Insights

**🎯 Every Song Is Independent**  
The loop doesn't compare songs to each other—each song is scored individually against the user's preferences using the same formula.

**🔄 The Loop Pattern**
1. Load all songs from CSV
2. For each song: calculate score (0–7.8 max)
3. After all songs scored: sort by score (descending)
4. Return top K songs with explanations

**⚙️ Tuning the Gaussian (k parameter)**
- `k = 0.5`: Loose/forgiving — songs far from user pref still score well
- `k = 1.0`: Standard — balanced match/discovery
- `k = 2.0`: Strict — only songs very close to user pref score high

**🎭 Categorical vs. Numeric**
- **Genre & Mood**: All-or-nothing exact matches (0 or full weight)
- **Audio Features**: Soft Gaussian similarity (reward closeness, don't punish difference)
