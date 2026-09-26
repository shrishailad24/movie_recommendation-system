# 🎬 CineMatch AI — Global Movie Discovery Platform & Hybrid Recommendation Engine

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red.svg)](https://streamlit.io/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg)](https://fastapi.tiangolo.com/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.3+-orange.svg)](https://scikit-learn.org/)
[![SQLite](https://img.shields.io/badge/Database-SQLite%203-003B57.svg)](https://www.sqlite.org/)
[![TMDB](https://img.shields.io/badge/API-TMDB-01b4e4.svg)](https://www.themoviedb.org/)
[![Groq](https://img.shields.io/badge/LLM-Groq%20AI-f55036.svg)](https://groq.com/)

**CineMatch AI** is an enterprise-grade, mood-aware, explainable AI global movie recommendation and discovery platform. It combines **Two-Tier AI Intent Parsing + Deterministic Grounded Retrieval (No Hallucinations)**, **5-Factor Hybrid ML Ranking**, **TMDB Worldwide Catalog Integration**, **Cross-Language Global AI Twins**, **Movie DNA Profiling**, **Closed-Loop Feedback Learning**, **FastAPI REST Endpoints**, and a **Multi-Movie Group Scheduler**.

---

## 📌 Complete System Architecture

```text
                         👤 USER NATURAL LANGUAGE QUERY
                                       │
                                       ↓
                        🤖 CINEMATCH AI STUDIO (NLU)
                        (Intent Extraction & Context Memory)
                                       │
            ┌──────────────────────────┼──────────────────────────┐
            ↓                          ↓                          ↓
    Genre & Tropes               Mood & Emotion            Country & Language
  (e.g., Thriller, Sci-Fi)     (e.g., Mind-Blown, Chill)    (e.g., Korean, Kannada)
            ↓                          ↓                          ↓
    Negative Filters             Runtime Budget             Consensus Rating
   (Exclude: Horror)            (e.g., < 120 min)          (Rating >= 7.0)
            └──────────────────────────┼──────────────────────────┘
                                       │
                            🔎 GROUNDED RETRIEVAL
                           /                       \
                          /                         \
                TMDB Worldwide API            Local Movie Catalog
                 (100,000+ Titles)              (movies.pkl)
                          \                         /
                           \                       /
                            ↓                     ↓
                             CANDIDATE MOVIE POOL
                                       │
                                       ↓
                             🧬 DEEP MOVIE DNA
                     (Pacing, Intensity, Complexity, Themes)
                                       │
                                       ↓
                           5-FACTOR HYBRID ML ENGINE
          ┌────────────────────────────┼────────────────────────────┐
          ↓ (40%)                      ↓ (20%)                      ↓ (20%)
    Content Similarity                Movie DNA                   User Taste
    (Cosine Vector Matrix)        (Thematic Depth)             (Learned Vector)
          │                            │                            │
          └────────────────────────────┼────────────────────────────┘
                                       │ (10% Mood + 10% Rating)
                                       ↓
                               FINAL TOP-K RANKING
                                       │
                                       ↓
                           🤖 FACTUAL AI EXPLANATION
                     (Grounded on Real Retrieved Evidence)
                                       │
                                       ↓
                            🎬 USER RECOMMENDATIONS
                                       │
                                       ↓
                             👍 USER FEEDBACK LOOP
                       (Records in SQLite / Re-ranks Taste)
```

---

## 🏆 Development Phases (1 through 11)

| Phase | Milestone | Features & Implementation |
|---|---|---|
| **Phase 1** | **Production UI & TMDB** | Real posters, backdrops, YouTube trailer modals, DNS fallback resilience, and responsive cards. |
| **Phase 2** | **Personalization & Taste** | User Taste Vector, persistent favorites/watchlist, 5-star ratings, and Hidden Gems detection. |
| **Phase 3** | **World Cinema & Discovery** | Global cinema explorer across 17+ languages (Kannada, Hindi, Korean, Japanese, French, Spanish, etc.). |
| **Phase 4** | **Cross-Language AI Twins** | Recommends international equivalents matching any movie's psychological and thematic DNA. |
| **Phase 5** | **Deep Movie DNA Profiler** | Evaluates Genre structure, Mood & Vibe, Pacing, Story Complexity, Visuals, and Core Themes. |
| **Phase 6** | **Dedicated Mood Mode** | 9-state emotional recommender (*😊 Happy, 😢 Emotional, 🔥 Excited, 🧠 Thoughtful, ❤️ Romantic, 😱 Scared, 😌 Relaxed, 🚀 Adventurous, 😂 Funny*). |
| **Phase 7** | **AI Movie Assistant** | Multi-turn conversational companion with memory refinement and Kannada/Hindi/English NLP. |
| **Phase 8** | **Build My Movie Night** | Multi-movie group planner with 8 theme modes (*😂 Laugh, ❤️ Couple, 🔥 Thriller, 🧠 Brainy, etc.*) and total runtime calculation. |
| **Phase 9** | **Recommendation Evaluation** | Industrial evaluation suite calculating **Precision@K**, **Recall@K**, **NDCG@K**, **MAP@K**, **Catalog Coverage (64.2%)**, and **Diversity (0.730)**. |
| **Phase 10** | **Production REST Backend** | Standalone FastAPI backend (`api.py`) exposing auth, discovery, hybrid scoring, collections, and analytics endpoints. |
| **Phase 11** | **CineMatch AI Studio** | Natural Language Intent Extractor $\to$ Structured Filters $\to$ Grounded Retrieval $\to$ Hybrid ML $\to$ Evidence Explanations (Zero Hallucinations). |
| **Phase 12** | **Continuous Feedback MLOps** | Persistent SQLite DB learning loop, rating recalibration, and real-time taste vector re-ranking. |
| **Phase 13** | **Data & ML Infrastructure** | Automated Data Quality Audit, Two-Stage Candidate Retrieval, Model Version Registry (v1–v4), Experiment Tracking, and PSI Drift Monitoring. |
| **Phase 14** | **CineMatch 2.0 Product & UX** | Netflix/Letterboxd Personalized Feed, Head-to-Head Movie Comparison, Curated & Custom Collections, and Gamification Achievement Badges. |
| **Phase 15** | **Intelligence 2.0: Knowledge Graph** | Heterogeneous Movie Knowledge Graph (4,930+ nodes, 13,590+ edges), BFS Multi-Hop Path Finder, Ego-Network Mermaid Visualizer, Entity Filmography, and Relational Explainable AI. |

---

## 📁 Repository Structure

```text
movie-recommender-system/
├── app.py                  # Main Streamlit web application & AI platform
├── api.py                  # Production FastAPI REST Backend service
├── knowledge_graph.py      # Heterogeneous Movie Knowledge Graph engine & path traversals
├── ml_pipeline.py          # Data ingestion audit, Two-Stage retrieval, Model Registry & Drift monitor
├── main.py                 # ML training pipeline, vectorization & CLI tester
├── db.py                   # Persistent SQLite database layer & CRUD operations

├── cinematch.db            # SQLite database file
├── movies.pkl              # Processed movies DataFrame (4,800+ titles)
├── top_similarity.pkl      # Lightweight top-50 similarity mapping (~3.2 MB)
├── similarity.pkl          # Full similarity matrix
├── requirements.txt        # Python package dependencies (Streamlit, FastAPI, etc.)
├── application_image.png   # Application preview screenshot
├── .gitignore              # Git ignore rules for venv, cache, and secrets
├── .streamlit/             # Secrets configuration directory
│   └── secrets.toml
└── README.md               # Complete project documentation
```

---

## 🚀 Quick Start

### 1. Clone & Install
```bash
git clone https://github.com/shrishailad24/movie_recommendation-system.git
cd movie_recommendation-system
pip install -r requirements.txt
```

### 2. Configure Secrets (`.streamlit/secrets.toml`)
```toml
TMDB_API_KEY = "YOUR_TMDB_API_KEY"
GROQ_API_KEY = "YOUR_GROQ_API_KEY"
```

### 3. Run the Streamlit Interactive Platform
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

### 4. Run the FastAPI REST Backend
```bash
python -m uvicorn api:app --reload --port 8000
```
Explore interactive Swagger documentation at `http://localhost:8000/docs`.

---

## 📜 License
Distributed under the MIT License.
