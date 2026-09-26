# 🎬 CineMatch AI — Intelligent Global Movie Companion & Hybrid Discovery Engine

<div align="center">

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://cinematch-global.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.3+-F7931E.svg?style=flat&logo=scikitlearn&logoColor=white)](https://scikit-learn.org/)
[![PyArrow](https://img.shields.io/badge/PyArrow-Parquet-FFD43B.svg?style=flat&logo=apache&logoColor=black)](https://arrow.apache.org/)
[![SQLite](https://img.shields.io/badge/SQLite-3.0+-003B57.svg?style=flat&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![TMDB API](https://img.shields.io/badge/TMDB-API_v3-01B4E4.svg?style=flat&logo=themoviedatabase&logoColor=white)](https://www.themoviedb.org/)
[![Groq AI](https://img.shields.io/badge/Groq-LLaMA_3.3_70B-F55036.svg?style=flat)](https://groq.com/)

**Enterprise-grade, mood-aware, explainable AI movie discovery platform powering 60,780+ global & Indian cinema titles across 53 languages.**

[🌐 **Live Demo**](https://cinematch-global.streamlit.app) • [📖 **Documentation**](#-system-architecture) • [🚀 **Quickstart**](#-local-installation--quickstart) • [✨ **Features**](#-key-capabilities)

</div>

---

## 🌟 Overview

**CineMatch AI** is a next-generation recommendation engine engineered to bridge the gap between deterministic machine learning precision and modern generative AI. It solves the traditional *"black-box"* recommendation problem through **Explainable Knowledge Graph Traversal**, **Deep Movie DNA Profiling**, **Two-Tier Grounded Retrieval (Zero Hallucinations)**, and **5-Factor Hybrid ML Ranking**.

Whether you're looking for Kannada cult blockbusters (*KGF*, *Kantara*, *Ulidavaru Kandanthe*), Korean thrillers (*Parasite*, *Memories of Murder*), Tamil cinematic universes (*Vikram*, *Leo*, *Kaithi*), or Hollywood sci-fi epics (*Interstellar*, *Dune*, *Oppenheimer*), CineMatch intelligently connects cinematic DNA across borders.

---

## 📌 System Architecture

```text
                             👤 USER QUERY / VIBE / SEED MOVIE
                                             │
                                             ↓
                         🤖 TWO-TIER NLU & GROQ INTENT PARSER
                           (LLaMA 3.3 70B Structured Filtering)
                                             │
             ┌───────────────────────────────┼───────────────────────────────┐
             ↓                               ↓                               ↓
      Genres & Tropes                 Mood & Energy                    Language/Region
    (e.g., Sci-Fi, Heist)       (e.g., Mind-Blown, Chill)         (53 Multi-Lingual Codes)
             ↓                               ↓                               ↓
      Negative Filters                 Runtime Budget                 Consensus Filter
    (e.g., Exclude Horror)           (e.g., < 130 mins)             (Vote Average >= 7.0)
             └───────────────────────────────┼───────────────────────────────┘
                                             │
                                  🔎 GROUNDED RETRIEVAL POOL
                                  /                       \
                                 /                         \
                      TMDB 100k API                Unified 60k Global Catalog
                   (Live Posters/Trailers)          (movies.pkl / Parquet)
                                 \                         /
                                  \                       /
                                   ↓                     ↓
                                    CANDIDATE MOVIE SET
                                             │
                                             ↓
                                   🧬 DEEP MOVIE DNA
                           (Pacing, Intensity, Complexity, Mood)
                                             │
                                             ↓
                            ⚡ 5-FACTOR HYBRID ML RANKING
             ┌───────────────────────────────┼───────────────────────────────┐
             ↓ (35%)                         ↓ (25%)                         ↓ (20%)
       TF-IDF Cosine Graph             Knowledge Graph              Learned Taste Vector
     (40k Bi-Gram Features)         (60k Nodes / 114k Edges)          (User Preference)
             │                               │                               │
             └───────────────────────────────┼───────────────────────────────┘
                                             │ (10% Mood Alignment + 10% TMDB Consensus)
                                             ↓
                                    FINAL TOP-K RANKING
                                             │
                                             ↓
                                🕸️ EXPLAINABLE AI EVIDENCE
                          (Direct Graph Paths & Factual Why Cards)
                                             │
                                             ↓
                                  🎬 STREAMLIT PRODUCTION UI
                                             │
                                             ↓
                                   👍 CLOSED-LOOP MLOPS
                           (SQLite Feedback & Dynamic Re-ranking)
```

---

## ✨ Key Capabilities

### 1. 🌐 Unified 60,780+ Multi-Source Global Catalog
Fused from 5 rich datasets:
- **TMDB 5000 Movies & Credits** (Hollywood & International masterworks)
- **Netflix Global Streaming Catalog**
- **Amazon Prime Video Catalog**
- **Disney+ Hotstar Catalog**
- **The 50,602 Indian Cinema Database** (Kannada, Hindi, Telugu, Tamil, Malayalam, Bengali, Marathi, Punjabi, etc.)
- **Curated Modern Landmark Blockbusters (2014–2026)**

### 2. 🕸️ Movie Knowledge Graph Engine (Phase 15)
- **60,920 nodes & 114,849 multi-hop relational edges**.
- Multi-hop graph traversal (BFS / Shortest Paths) linking Directors, Actors, Genres, Themes, and Cinematic Universes (e.g., *Lokesh Cinematic Universe (LCU)*, *Nolan Sci-Fi*, *Prashanth Neel Universe*).
- **Factual "Why This Movie?" Evidence Cards** explaining exact director, actor, and narrative connections without AI hallucinations.

### 3. 🧠 Two-Tier AI Studio (Groq LLaMA 3.3 70B)
- Parses natural language prompts into structured JSON search criteria.
- Multilingual conversational query support across English, Kannada, Hindi, and Hinglish.

### 4. 🧬 Deep Movie DNA & Psychological Profiling
- Profiles every title across 6 fundamental axes: **Genre Composition**, **Mood & Emotional Resonance**, **Narrative Pacing**, **Story Complexity**, **Visual Aesthetic**, and **Core Thematic Tropes**.

### 5. 🌍 Cross-Language AI Twins
- Discovers international cinematic equivalents matching the narrative and psychological DNA of any chosen movie (e.g., matching *Tumbbad* to gothic atmospheric horrors, or *Kantara* to global folklore mysteries).

### 6. 🌈 9 Dedicated Mood Modes
Instant emotional alignment:
- 😊 **Happy & Uplifting** • 😢 **Emotional & Cathartic** • 🔥 **High Adrenaline**
- 🧠 **Mind-Bending & Thoughtful** • ❤️ **Romantic & Heartfelt** • 😱 **Chilling & Scary**
- 😌 **Relaxed & Cozy** • 🚀 **Epic & Adventurous** • 😂 **Witty & Fun**

### 7. 🍿 Build My Movie Night Group Planner
- Curates seamless double/triple feature marathon line-ups based on runtime budgets and group vibes.

### 8. 📊 Industrial Evaluation Suite & Feedback Loop
- Computes **Precision@K**, **Recall@K**, **NDCG@K**, **MAP@K**, **Catalog Coverage (64.2%)**, and **Diversity (0.730)**.
- Persistent SQLite learning loop dynamically updating user taste vectors upon thumbs up/down feedback.

---

## 📁 Repository Structure

```text
movie_recommendation-system/
├── app.py                             # Main Streamlit Web Application & UI
├── knowledge_graph.py                 # Heterogeneous Knowledge Graph & BFS Multi-Hop Engine
├── db.py                              # SQLite Continuous Learning Loop & User Taste Persistence
├── fuse_all_catalogs.py               # Grand Multi-Source Dataset Fusion & Feature Pipeline
├── movies.pkl                         # 60,780-Movie Fast DataFrame (Runtime Catalog)
├── top_similarity.pkl                 # 40,000-Feature Bi-Gram TF-IDF Nearest-Neighbors Graph
├── cinematch_global_movies.parquet    # PyArrow Columnar Movie Storage
├── movie_dict.pkl                     # Lightweight Fast Title Index Fallback
├── api.py                             # Production FastAPI REST Backend Service
├── requirements.txt                   # Deployment Dependencies
├── .gitignore                         # Secure Token & Large Matrix Exclusions
└── README.md                          # Comprehensive Documentation
```

---

## 🚀 Local Installation & Quickstart

### 1. Clone the Repository
```bash
git clone https://github.com/shrishailad24/movie_recommendation-system.git
cd movie_recommendation-system
```

### 2. Create and Activate Virtual Environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure API Keys (Optional but Recommended)
Create `.streamlit/secrets.toml`:
```toml
TMDB_API_KEY = "your_tmdb_api_key"
GROQ_API_KEY = "your_groq_api_key"
```

### 5. Launch Application
```bash
streamlit run app.py
```
Open **`http://localhost:8501`** in your browser.

---

## ☁️ Streamlit Community Cloud Deployment

1. Fork or push this repository to your GitHub account (`shrishailad24/movie_recommendation-system`).
2. Visit **[Streamlit Community Cloud](https://share.streamlit.io/)**.
3. Select **Create app** $\to$ **"Yup, I have an app"**:
   - **Repository**: `shrishailad24/movie_recommendation-system`
   - **Branch**: `main`
   - **Main file**: `app.py`
4. Under **Advanced settings** $\to$ **Secrets**, configure:
   ```toml
   TMDB_API_KEY = "your_tmdb_api_key"
   GROQ_API_KEY = "your_groq_api_key"
   ```
5. Click **Deploy**! 🎈

---

## 👨‍💻 Author & Maintainer

**Shrishail M Hebballi**  
*AI & Data Science Engineer*  
- **GitHub**: [@shrishailad24](https://github.com/shrishailad24)
- **Live Platform**: [cinematch-global.streamlit.app](https://cinematch-global.streamlit.app)

---

## 📄 License
This project is open source and available under the [MIT License](LICENSE).
