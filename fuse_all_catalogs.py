"""
🎬 CineMatch Master Global Catalog & Multi-Source Fusion Engine (Grand Edition)
================================================================================
Unifies and fuses 5 rich movie datasets + Curated Landmark Blockbusters:
  1. TMDB 5000 Movies & Credits (from film-recommendation-engine.ipynb)
  2. Netflix Global Movies & Series (from eda-stream-platforms-ntflix-amazn-disny.ipynb)
  3. Amazon Prime Video Catalog (from eda-stream-platforms-ntflix-amazn-disny.ipynb)
  4. Disney+ Hotstar Catalog (from eda-stream-platforms-ntflix-amazn-disny.ipynb)
  5. The 50,602 Indian Cinema Database (Kannada, Hindi, Telugu, Tamil, Malayalam, Bengali, etc.)
  6. Curated Modern Blockbusters (2014-2026) with detailed cast, directors, and plot keywords

Outputs:
  - cinematch_global_movies.parquet (Parquet Columnar Storage)
  - movies.pkl (Fast runtime DataFrame)
  - top_similarity.pkl (Scalable TF-IDF Nearest-Neighbors Cosine Graph)
================================================================================
"""

import os
import sys
import re
import json
import pickle
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INDIAN_CSV_PATH = r"C:\Users\shash\Downloads\indian movies.csv\indian movies.csv"
NETFLIX_CSV_PATH = os.path.join(BASE_DIR, "netflix_titles.csv")
AMAZON_CSV_PATH = os.path.join(BASE_DIR, "amazon_prime_titles.csv")
DISNEY_CSV_PATH = os.path.join(BASE_DIR, "disney_plus_titles.csv")
TMDB_MOVIES_PATH = os.path.join(BASE_DIR, "tmdb_5000_movies.csv")
TMDB_CREDITS_PATH = os.path.join(BASE_DIR, "tmdb_5000_credits.csv")

PARQUET_OUT = os.path.join(BASE_DIR, "cinematch_global_movies.parquet")
MOVIES_PKL = os.path.join(BASE_DIR, "movies.pkl")
SIM_PKL = os.path.join(BASE_DIR, "top_similarity.pkl")

LANG_CODE_MAP = {
    'hindi': 'hi',
    'kannada': 'kn',
    'telugu': 'te',
    'tamil': 'ta',
    'malayalam': 'ml',
    'bengali': 'bn',
    'marathi': 'mr',
    'punjabi': 'pa',
    'urdu': 'ur',
    'gujarati': 'gu',
    'oriya': 'or',
    'assamese': 'as',
    'nepali': 'ne',
    'bhojpuri': 'bho',
    'rajastani': 'raj',
    'sanskrit': 'sa',
    'kashmiri': 'ks',
    'konkani': 'kok',
    'tulu': 'tcy'
}

GENRE_MAP = {
    'science fiction': 'scifi',
    'sci-fi': 'scifi',
    'sci fi': 'scifi',
    'romantic comedy': 'romance comedy',
    'rom-com': 'romance comedy',
    'action & adventure': 'action adventure',
    'tv movie': '',
    'motion picture': '',
}

GENERIC_STOPWORDS = {
    "chapter", "part", "vol", "volume", "movie", "film", "films",
    "one", "two", "three", "first", "second", "third", "exploring",
    "production", "starring", "directed", "releases", "landmark",
    "cinematic", "story", "acclaimed", "premier", "series", "season",
    "an", "the", "and", "or", "in", "on", "at", "by", "for", "with",
    "indian", "cinema", "shows", "show", "release"
}

# Curated Landmark Modern Blockbusters (2014 - 2026)
CURATED_BLOCKBUSTERS = [
    {
        "title": "Kantara",
        "original_title": "Kantara",
        "director": "Rishab Shetty",
        "cast": "Rishab Shetty, Sapthami Gowda, Kishore, Achyuth Kumar, Pramod Shetty",
        "genres": "Action Drama Mystery Thriller Folklore",
        "keywords": "panjurli, guliga daiva, daivaradhane, forest officer conflict, coastal karnataka, bhoota kola, tribal folklore, land dispute, sandalwood, karnataka",
        "overview": "When greed paves the way for betrayal, blood-shed and passion, a young tribal man reluctantly embraces the tradition of his ancestors to protect his village against the evil forest lord.",
        "year": 2022,
        "original_language": "kn",
        "languages": "KN, HI, TE, TA, ML",
        "countries": "India",
        "vote_average": 8.3,
        "vote_count": 28000,
        "popularity": 45.0,
        "runtime": 148,
        "movie_id": 9900001
    },
    {
        "title": "K.G.F: Chapter 2",
        "original_title": "K.G.F: Chapter 2",
        "director": "Prashanth Neel",
        "cast": "Yash, Sanjay Dutt, Raveena Tandon, Srinidhi Shetty, Prakash Raj, Rao Ramesh",
        "genres": "Action Crime Drama Period Thriller",
        "keywords": "kolar gold fields, rocky bhai, adheera, prime minister ramika sen, gold mine, mass action, crime syndicate, period action, sandalwood, hombale",
        "overview": "The blood-soaked land of Kolar Gold Fields has a new overlord now. Rocky, whose name strikes fear in the heart of his foes. His allies look up to him as their savior, the government sees him as a threat.",
        "year": 2022,
        "original_language": "kn",
        "languages": "KN, HI, TE, TA, ML",
        "countries": "India",
        "vote_average": 8.4,
        "vote_count": 42000,
        "popularity": 55.0,
        "runtime": 168,
        "movie_id": 9900002
    },
    {
        "title": "K.G.F: Chapter 1",
        "original_title": "K.G.F: Chapter 1",
        "director": "Prashanth Neel",
        "cast": "Yash, Srinidhi Shetty, Anant Nag, Achyuth Kumar, Malavika Avinash, Vashishta N Simha",
        "genres": "Action Crime Drama Period Thriller",
        "keywords": "kolar gold fields, rocky bhai, gangster, underworld, gold mine, mass cinema, period action, mother promise, bombay underworld, sandalwood",
        "overview": "In the 1970s, a fierce rebel rises against brutal oppression in the Kolar Gold Fields and becomes the symbol of hope to legions of downtrodden people.",
        "year": 2018,
        "original_language": "kn",
        "languages": "KN, HI, TE, TA, ML",
        "countries": "India",
        "vote_average": 8.2,
        "vote_count": 39000,
        "popularity": 48.0,
        "runtime": 156,
        "movie_id": 9900003
    },
    {
        "title": "Mr. and Mrs. Ramachari",
        "original_title": "Mr. and Mrs. Ramachari",
        "director": "Santhosh Ananddram",
        "cast": "Yash, Radhika Pandit, Srinath, Achyuth Kumar, Malavika Avinash",
        "genres": "Romance Action Drama Comedy",
        "keywords": "rebel youth, college love story, vishnuvardhan tribute, misunderstandings, family drama, sandalwood, romantic action",
        "overview": "Ramachari, a die-hard fan of Vishnuvardhan, falls in love with Divya. However, their contrasting personalities and misunderstandings threaten to tear them apart.",
        "year": 2014,
        "original_language": "kn",
        "languages": "KN",
        "countries": "India",
        "vote_average": 7.8,
        "vote_count": 6500,
        "popularity": 22.0,
        "runtime": 152,
        "movie_id": 9900004
    },
    {
        "title": "Googly",
        "original_title": "Googly",
        "director": "Pavan Wadeyar",
        "cast": "Yash, Kriti Kharbanda, Anant Nag, Sadhu Kokila",
        "genres": "Romance Comedy Drama",
        "keywords": "sharath swathi, college romance, ego clash, youth comedy, misunderstandings, sandalwood, romantic comedy",
        "overview": "Sharath, an eccentric young man, falls in love with Swathi. But a misunderstanding forces them apart until destiny brings them face-to-face years later.",
        "year": 2013,
        "original_language": "kn",
        "languages": "KN",
        "countries": "India",
        "vote_average": 7.6,
        "vote_count": 4800,
        "popularity": 18.0,
        "runtime": 140,
        "movie_id": 9900005
    },
    {
        "title": "Salaar: Part 1 - Ceasefire",
        "original_title": "Salaar",
        "director": "Prashanth Neel",
        "cast": "Prabhas, Prithviraj Sukumaran, Shruti Haasan, Jagapathi Babu, Bobby Simha",
        "genres": "Action Crime Drama Thriller",
        "keywords": "deva, varadharaja mannaar, khansaar, tribal tribes, dynasty ceasefire, mass action, dark underworld, friendship, tollywood, sandalwood",
        "overview": "In the violent city of Khansaar, a gang leader makes a promise to a dying friend and takes on other criminal gangs to secure his rightful place.",
        "year": 2023,
        "original_language": "te",
        "languages": "TE, KN, HI, TA, ML",
        "countries": "India",
        "vote_average": 7.9,
        "vote_count": 31000,
        "popularity": 52.0,
        "runtime": 175,
        "movie_id": 9900006
    },
    {
        "title": "RRR",
        "original_title": "RRR",
        "director": "S.S. Rajamouli",
        "cast": "N.T. Rama Rao Jr., Ram Charan, Alia Bhatt, Ajay Devgn, Olivia Morris, Shriya Saran",
        "genres": "Action Drama Period Epic History",
        "keywords": "komaram bheem, alluri sitarama raju, british raj, freedom fighter, epic friendship, revolution, tollywood, naatu naatu, oscar winner",
        "overview": "A fearless revolutionary and an officer in the British force, who once shared a deep bond, decide to join forces and chart out an inspiring path of freedom against the despotic rulers.",
        "year": 2022,
        "original_language": "te",
        "languages": "TE, HI, TA, KN, ML, EN",
        "countries": "India",
        "vote_average": 8.6,
        "vote_count": 55000,
        "popularity": 65.0,
        "runtime": 187,
        "movie_id": 9900007
    },
    {
        "title": "Pushpa: The Rise",
        "original_title": "Pushpa: The Rise",
        "director": "Sukumar",
        "cast": "Allu Arjun, Rashmika Mandanna, Fahadh Faasil, Sunil, Anasuya Bharadwaj",
        "genres": "Action Crime Drama Thriller",
        "keywords": "pushpa raj, red sandalwood smuggling, seshachalam forests, shekhawat, mass action syndicate, tollywood",
        "overview": "A laborer rises through the ranks of a red sandalwood smuggling syndicate, making powerful enemies along the way.",
        "year": 2021,
        "original_language": "te",
        "languages": "TE, HI, TA, KN, ML",
        "countries": "India",
        "vote_average": 8.0,
        "vote_count": 38000,
        "popularity": 49.0,
        "runtime": 179,
        "movie_id": 9900008
    },
    {
        "title": "Vikram",
        "original_title": "Vikram",
        "director": "Lokesh Kanagaraj",
        "cast": "Kamal Haasan, Vijay Sethupathi, Fahadh Faasil, Suriya, Narain, Kalidas Jayaram",
        "genres": "Action Crime Thriller Gangster Mystery",
        "keywords": "lcu, agent vikram, santhanam, amar, rolex, drug syndicate, black squad, ghost, kollywood, lokesh cinematic universe",
        "overview": "A special agent investigates a murder committed by a masked group of serial killers. However, a tangled maze of clues soon leads him to the drug kingpin of Chennai.",
        "year": 2022,
        "original_language": "ta",
        "languages": "TA, TE, HI, KN, ML",
        "countries": "India",
        "vote_average": 8.3,
        "vote_count": 36000,
        "popularity": 47.0,
        "runtime": 174,
        "movie_id": 9900009
    },
    {
        "title": "Leo",
        "original_title": "Leo",
        "director": "Lokesh Kanagaraj",
        "cast": "Vijay, Trisha Krishnan, Sanjay Dutt, Arjun Sarja, Gautham Vasudev Menon",
        "genres": "Action Crime Thriller Gangster",
        "keywords": "lcu, parthiban, leo das, cafe owner, himachal pradesh, tobacco factory, mass action, kollywood, lokesh cinematic universe",
        "overview": "A mild-mannered cafe owner in Kashmir becomes a local hero after thwarting an attack, but his past soon catches up with him as ruthless gangsters claim he is their former partner.",
        "year": 2023,
        "original_language": "ta",
        "languages": "TA, TE, HI, KN, ML",
        "countries": "India",
        "vote_average": 7.8,
        "vote_count": 29000,
        "popularity": 44.0,
        "runtime": 164,
        "movie_id": 9900010
    },
    {
        "title": "Kaithi",
        "original_title": "Kaithi",
        "director": "Lokesh Kanagaraj",
        "cast": "Karthi, Narain, Dheena, George Maryan, Harish Uthaman",
        "genres": "Action Thriller Crime Suspense",
        "keywords": "lcu, dilli, lorry journey, poisoned police, hospital siege, one night thriller, kollywood, lokesh cinematic universe",
        "overview": "A recently released prisoner races against time to drive a truck full of poisoned cops to the hospital while evading criminals who want to stop him.",
        "year": 2019,
        "original_language": "ta",
        "languages": "TA, TE, HI, KN, ML",
        "countries": "India",
        "vote_average": 8.4,
        "vote_count": 27000,
        "popularity": 38.0,
        "runtime": 145,
        "movie_id": 9900011
    },
    {
        "title": "Jailer",
        "original_title": "Jailer",
        "director": "Nelson Dilipkumar",
        "cast": "Rajinikanth, Vinayakan, Ramya Krishnan, Vasanth Ravi, Mohanlal, Shiva Rajkumar",
        "genres": "Action Crime Comedy Thriller",
        "keywords": "tiger muthuvel pandian, idol smuggling, retired jailer, blast mohan, mass action, kollywood",
        "overview": "A retired jailer goes on a manhunt to find his son's killers. But the road leads him into a familiar, darker world where he must unleash his old lethal instincts.",
        "year": 2023,
        "original_language": "ta",
        "languages": "TA, TE, HI, KN, ML",
        "countries": "India",
        "vote_average": 7.7,
        "vote_count": 28000,
        "popularity": 42.0,
        "runtime": 168,
        "movie_id": 9900012
    },
    {
        "title": "Manjummel Boys",
        "original_title": "Manjummel Boys",
        "director": "Chidambaram",
        "cast": "Soubin Shahir, Sreenath Bhasi, Balu Varghese, Ganapathi, Deepak Parambol",
        "genres": "Adventure Drama Survival Thriller",
        "keywords": "kodaikanal trip, guna caves, devil kitchen, subhash rescue, real life friendship, survival drama, mollywood, friendship goals",
        "overview": "A group of friends from a small town embark on a vacation to Kodaikanal, but when one of them falls deep into the perilous Guna Caves, their bond is tested to the extreme.",
        "year": 2024,
        "original_language": "ml",
        "languages": "ML, TA, TE, KN, HI",
        "countries": "India",
        "vote_average": 8.5,
        "vote_count": 24000,
        "popularity": 41.0,
        "runtime": 135,
        "movie_id": 9900013
    },
    {
        "title": "Oppenheimer",
        "original_title": "Oppenheimer",
        "director": "Christopher Nolan",
        "cast": "Cillian Murphy, Emily Blunt, Matt Damon, Robert Downey Jr., Florence Pugh, Josh Hartnett",
        "genres": "Biography Drama History Science Political",
        "keywords": "j robert oppenheimer, manhattan project, los alamos, atomic bomb, trinity test, lewis strauss, quantum physics, cold war, oscar winner",
        "overview": "The story of American scientist J. Robert Oppenheimer and his role in the development of the atomic bomb during World War II.",
        "year": 2023,
        "original_language": "en",
        "languages": "EN",
        "countries": "United States",
        "vote_average": 8.9,
        "vote_count": 85000,
        "popularity": 75.0,
        "runtime": 180,
        "movie_id": 9900014
    },
    {
        "title": "Dune: Part Two",
        "original_title": "Dune: Part Two",
        "director": "Denis Villeneuve",
        "cast": "Timothee Chalamet, Zendaya, Rebecca Ferguson, Javier Bardem, Austin Butler, Florence Pugh",
        "genres": "Action Adventure Sci-Fi Epic",
        "keywords": "arrakis, paul atreides, fremen, sand worm, spice, prophecy, lisan al gaib, huan harkonnen, sci-fi masterpiece",
        "overview": "Paul Atreides unites with Chani and the Fremen while seeking revenge against the conspirators who destroyed his family.",
        "year": 2024,
        "original_language": "en",
        "languages": "EN",
        "countries": "United States",
        "vote_average": 8.7,
        "vote_count": 78000,
        "popularity": 70.0,
        "runtime": 166,
        "movie_id": 9900015
    },
    {
        "title": "PK",
        "original_title": "PK",
        "director": "Rajkumar Hirani",
        "cast": "Aamir Khan, Anushka Sharma, Sushant Singh Rajput, Boman Irani, Saurabh Shukla",
        "genres": "Comedy Drama Sci-Fi Satire",
        "keywords": "alien visitor, jagat janani, wrong number, godman superstition, missing remote, friendship, bollywood comedy",
        "overview": "An alien on Earth loses the remote control to his spaceship. In his quest to retrieve it, he innocently questions the religious dogmas and superstitions of mankind.",
        "year": 2014,
        "original_language": "hi",
        "languages": "HI",
        "countries": "India",
        "vote_average": 8.1,
        "vote_count": 42000,
        "popularity": 38.0,
        "runtime": 153,
        "movie_id": 9900016
    },
    {
        "title": "Taare Zameen Par",
        "original_title": "Taare Zameen Par",
        "director": "Aamir Khan",
        "cast": "Darsheel Safary, Aamir Khan, Tisca Chopra, Vipin Sharma",
        "genres": "Drama Family Emotional Inspirational",
        "keywords": "ishaan awasthi, ram shankar nikumbh, dyslexia, boarding school, child psychology, painting, heart-touching, bollywood",
        "overview": "An eight-year-old boy is thought to be a lazy trouble-maker, until the new art teacher has the patience and compassion to discover the real problem behind his struggles in school.",
        "year": 2007,
        "original_language": "hi",
        "languages": "HI",
        "countries": "India",
        "vote_average": 8.4,
        "vote_count": 39000,
        "popularity": 35.0,
        "runtime": 165,
        "movie_id": 9900017
    },
    {
        "title": "The Martian",
        "original_title": "The Martian",
        "director": "Ridley Scott",
        "cast": "Matt Damon, Jessica Chastain, Kristen Wiig, Jeff Daniels, Michael Pena",
        "genres": "Adventure Drama Sci-Fi Survival Space",
        "keywords": "stranded on mars, mark watney, growing potatoes on mars, nasa rescue, space survival, hermes crew, science fiction",
        "overview": "An astronaut becomes stranded on Mars after his team assume him dead, and must rely on his ingenuity to find a way to signal to Earth that he is alive.",
        "year": 2015,
        "original_language": "en",
        "languages": "EN",
        "countries": "United States",
        "vote_average": 8.0,
        "vote_count": 68000,
        "popularity": 50.0,
        "runtime": 144,
        "movie_id": 9900018
    },
    {
        "title": "Gravity",
        "original_title": "Gravity",
        "director": "Alfonso Cuaron",
        "cast": "Sandra Bullock, George Clooney, Ed Harris",
        "genres": "Adventure Drama Sci-Fi Thriller Space",
        "keywords": "space debris, space station, astronaut survival, earth orbit, tethered in space, zero gravity",
        "overview": "Two astronauts work together to survive after an accident leaves them stranded in space.",
        "year": 2013,
        "original_language": "en",
        "languages": "EN",
        "countries": "United States",
        "vote_average": 7.7,
        "vote_count": 58000,
        "popularity": 45.0,
        "runtime": 91,
        "movie_id": 9900019
    },
    {
        "title": "Arrival",
        "original_title": "Arrival",
        "director": "Denis Villeneuve",
        "cast": "Amy Adams, Jeremy Renner, Forest Whitaker, Michael Stuhlbarg",
        "genres": "Drama Mystery Sci-Fi Alien",
        "keywords": "linguistics, heptapods, non-linear time, alien communication, louise banks, weapon time, mind-bending sci-fi",
        "overview": "A linguist works with the military to communicate with alien lifeforms after twelve mysterious spacecraft appear around the world.",
        "year": 2016,
        "original_language": "en",
        "languages": "EN",
        "countries": "United States",
        "vote_average": 8.0,
        "vote_count": 64000,
        "popularity": 48.0,
        "runtime": 116,
        "movie_id": 9900020
    },
    {
        "title": "Contact",
        "original_title": "Contact",
        "director": "Robert Zemeckis",
        "cast": "Jodie Foster, Matthew McConaughey, Tom Skerritt, James Woods",
        "genres": "Drama Mystery Sci-Fi Space",
        "keywords": "seti, radio signal from vega, carl sagan, alien contact, prime numbers, wormhole journey, faith and science",
        "overview": "Dr. Ellie Arroway, after years of searching, finds conclusive radio proof of extraterrestrial intelligence, sending her on a journey into the unknown.",
        "year": 1997,
        "original_language": "en",
        "languages": "EN",
        "countries": "United States",
        "vote_average": 7.5,
        "vote_count": 32000,
        "popularity": 30.0,
        "runtime": 150,
        "movie_id": 9900021
    },
    {
        "title": "2001: A Space Odyssey",
        "original_title": "2001: A Space Odyssey",
        "director": "Stanley Kubrick",
        "cast": "Keir Dullea, Gary Lockwood, William Sylvester, Douglas Rain",
        "genres": "Adventure Mystery Sci-Fi Space Epic",
        "keywords": "hal 9000, monolith, jupiter mission, artificial intelligence, space station, star child, stanley kubrick classic",
        "overview": "After uncovering a mysterious artifact on the Moon, a spacecraft is sent to Jupiter to find its origins - a mission overseen by the intelligent supercomputer H.A.L. 9000.",
        "year": 1968,
        "original_language": "en",
        "languages": "EN",
        "countries": "United States",
        "vote_average": 8.3,
        "vote_count": 48000,
        "popularity": 40.0,
        "runtime": 149,
        "movie_id": 9900022
    }
]


def clean_number(val, default=0.0):
    if pd.isna(val) or val is None:
        return default
    s = str(val).strip().replace(',', '').replace('-', '')
    try:
        return float(s) if s else default
    except Exception:
        return default


def clean_year(val, default=2000):
    if pd.isna(val) or val is None:
        return default
    s = str(val).strip()
    match = re.search(r'\b(19\d\d|20\d\d)\b', s)
    if match:
        return int(match.group(1))
    return default


def parse_json_names(json_str, limit=5):
    if not json_str or pd.isna(json_str):
        return []
    try:
        items = json.loads(str(json_str))
        if isinstance(items, list):
            names = [i.get('name', '') for i in items if isinstance(i, dict) and i.get('name')]
            return names[:limit] if limit else names
    except Exception:
        pass
    return []


def parse_directors(crew_json):
    if not crew_json or pd.isna(crew_json):
        return []
    try:
        items = json.loads(str(crew_json))
        if isinstance(items, list):
            return [i.get('name', '') for i in items if isinstance(i, dict) and i.get('job') == 'Director']
    except Exception:
        pass
    return []


def clean_title_canonical(t):
    """Canonicalizes movie titles by removing dubbing and quality suffixes."""
    s = str(t).strip()
    s = re.sub(r'\s*\((hindi|tamil|telugu|kannada|malayalam|bengali|marathi|english|dubbed|eng sub|audio).*?\)', '', s, flags=re.IGNORECASE)
    s = re.sub(r'\s*\[(4k|uhd|4k uhd|hd|eng).*?\]', '', s, flags=re.IGNORECASE)
    return s.strip()


def norm_clean_str(s):
    cleaned = clean_title_canonical(s)
    return re.sub(r'[^a-zA-Z0-9]', '', str(cleaned).lower()).strip()


def sanitize_token(s):
    return re.sub(r'[^a-zA-Z0-9]', '', str(s).lower()).strip()


def clean_genres(g_str):
    s = str(g_str).lower()
    for k, v in GENRE_MAP.items():
        s = s.replace(k, v)
    words = re.findall(r'[a-zA-Z]+', s)
    return [w for w in words if len(w) > 2]


def build_smart_soup(rec):
    tokens = []
    
    # 1. Normalized Genres (3x)
    genres = clean_genres(rec.get('genres', ''))
    for g in genres:
        tokens.extend([f"gen_{g}"] * 3)

    # 2. Directors (4x)
    dirs = [d.strip() for d in str(rec.get('director') or '').split(',') if d.strip()]
    for d in dirs:
        clean_d = sanitize_token(d)
        if clean_d and len(clean_d) > 3:
            tokens.extend([f"dir_{clean_d}"] * 4)

    # 3. Cast (3x for top actors)
    cast_list = [c.strip() for c in str(rec.get('cast') or '').split(',') if c.strip()][:5]
    for c in cast_list:
        clean_c = sanitize_token(c)
        if clean_c and len(clean_c) > 3:
            tokens.extend([f"act_{clean_c}"] * 3)

    # 4. Keywords / Themes (3x)
    kw_raw = str(rec.get('keywords') or '').replace(',', ' ').split()
    clean_kws = [k.lower() for k in kw_raw if len(k) > 2 and k.lower() not in GENERIC_STOPWORDS]
    for k in clean_kws:
        tokens.extend([f"kw_{k}"] * 2)
        tokens.append(k)

    # 5. Language (1x)
    lang = str(rec.get('original_language') or '').lower().strip()
    if lang:
        tokens.append(f"lang_{lang}")

    # 6. Title tokens (2x, stripped of generic stopwords)
    title = str(rec.get('title') or '').lower()
    title_words = re.findall(r'[a-zA-Z0-9]+', title)
    title_clean = [w for w in title_words if len(w) > 1 and w not in GENERIC_STOPWORDS]
    tokens.extend(title_clean * 2)

    # 7. Real Overview (1x, stripped of generic stopwords and synthetic boilerplate)
    overview = str(rec.get('overview') or '').lower()
    if "landmark exploring" not in overview and "premier release" not in overview:
        ov_words = re.findall(r'[a-zA-Z0-9]+', overview)
        ov_clean = [w for w in ov_words if len(w) > 2 and w not in GENERIC_STOPWORDS]
        tokens.extend(ov_clean)

    return " ".join(tokens)


def fuse_all_datasets():
    print("=" * 80, flush=True)
    print("🚀 CineMatch Multi-Source Fusion & Training Engine (Grand Edition)", flush=True)
    print("=" * 80, flush=True)

    all_records = []
    seen_titles = set()

    # -------------------------------------------------------------------------
    # 0. Ingest Curated Landmark Blockbusters FIRST (Highest Quality Priority)
    # -------------------------------------------------------------------------
    print(f"🌟 Ingesting Curated Landmark Blockbusters ({len(CURATED_BLOCKBUSTERS)} titles)...", flush=True)
    for b in CURATED_BLOCKBUSTERS:
        norm_k = norm_clean_str(b["title"])
        seen_titles.add(norm_k)
        rec = dict(b)
        rec["tags"] = build_smart_soup(rec)
        all_records.append(rec)
    print(f"✅ Ingested {len(CURATED_BLOCKBUSTERS)} Curated Blockbusters with rich tags.", flush=True)

    # -------------------------------------------------------------------------
    # 1. Ingest TMDB 5000 Movies & Credits (film-recommendation-engine.ipynb)
    # -------------------------------------------------------------------------
    if os.path.exists(TMDB_MOVIES_PATH):
        print(f"📂 Reading TMDB 5000 Dataset: {TMDB_MOVIES_PATH}...", flush=True)
        m_df = pd.read_csv(TMDB_MOVIES_PATH)
        c_df = pd.read_csv(TMDB_CREDITS_PATH) if os.path.exists(TMDB_CREDITS_PATH) else pd.DataFrame()
        
        if not c_df.empty and 'id' in m_df.columns and 'movie_id' in c_df.columns:
            m_df = m_df.merge(c_df[['movie_id', 'cast', 'crew']], left_on='id', right_on='movie_id', how='left')

        tmdb_count = 0
        for idx, row in m_df.iterrows():
            raw_title = str(row.get('title') or row.get('original_title') or '').strip()
            title = clean_title_canonical(raw_title)
            if not title:
                continue
            norm_k = norm_clean_str(title)
            if not norm_k or norm_k in seen_titles:
                continue
            seen_titles.add(norm_k)

            movie_id = int(row.get('id') or idx + 1)
            overview = str(row.get('overview') or '')
            year_val = clean_year(row.get('release_date'))
            lang_code = str(row.get('original_language') or 'en').lower()
            
            genres_list = parse_json_names(row.get('genres'), limit=4)
            keywords_list = parse_json_names(row.get('keywords'), limit=6)
            countries_list = parse_json_names(row.get('production_countries'), limit=2)
            cast_list = parse_json_names(row.get('cast'), limit=5)
            directors_list = parse_directors(row.get('crew'))

            genres_str = " ".join(genres_list) if genres_list else "Drama"
            cast_str = ", ".join(cast_list)
            dir_str = ", ".join(directors_list[:2])
            country_str = ", ".join(countries_list) if countries_list else "United States"

            rec = {
                "movie_id": movie_id,
                "tmdb_id": str(movie_id),
                "imdb_id": f"tmdb_{movie_id}",
                "title": title,
                "original_title": str(row.get('original_title') or title),
                "overview": overview or f"A landmark cinematic production ({year_val}) directed by {dir_str or 'visionary directors'}.",
                "release_date": str(row.get('release_date') or f"{year_val}-01-01"),
                "year": int(year_val),
                "original_language": lang_code,
                "languages": lang_code.upper(),
                "countries": country_str,
                "genres": genres_str,
                "keywords": " ".join(keywords_list),
                "cast": cast_str,
                "director": dir_str,
                "runtime": int(clean_number(row.get('runtime'), 120)),
                "vote_average": round(float(clean_number(row.get('vote_average'), 7.0)), 1),
                "vote_count": int(clean_number(row.get('vote_count'), 100)),
                "popularity": round(float(clean_number(row.get('popularity'), 10.0)), 2),
                "poster_path": "",
                "backdrop_path": "",
            }
            rec["tags"] = build_smart_soup(rec)
            all_records.append(rec)
            tmdb_count += 1
            
        print(f"✅ Ingested {tmdb_count:,} TMDB 5000 titles.", flush=True)

    # -------------------------------------------------------------------------
    # 2. Ingest Streaming Platforms (Netflix, Amazon Prime, Disney+)
    # -------------------------------------------------------------------------
    stream_sources = [
        ("Netflix", NETFLIX_CSV_PATH, 8100000),
        ("Amazon Prime Video", AMAZON_CSV_PATH, 8300000),
        ("Disney+ Hotstar", DISNEY_CSV_PATH, 8500000)
    ]

    for stream_name, stream_path, id_base in stream_sources:
        if not os.path.exists(stream_path):
            continue
        print(f"📂 Reading {stream_name} Dataset: {stream_path}...", flush=True)
        st_df = pd.read_csv(stream_path)
        st_count = 0

        for idx, row in st_df.iterrows():
            raw_title = str(row.get('title') or '').strip()
            title = clean_title_canonical(raw_title)
            if not title:
                continue
            norm_k = norm_clean_str(title)
            if not norm_k or norm_k in seen_titles:
                continue
            seen_titles.add(norm_k)

            country_raw = str(row.get('country') or 'United States').strip()
            first_country = country_raw.split(',')[0].strip() if country_raw and country_raw != 'nan' else "International"
            
            # Infer language
            lang_code = 'en'
            c_low = country_raw.lower()
            if 'india' in c_low:
                lang_code = 'hi'
            elif 'korea' in c_low:
                lang_code = 'ko'
            elif 'japan' in c_low:
                lang_code = 'ja'
            elif 'france' in c_low:
                lang_code = 'fr'
            elif 'spain' in c_low or 'mexico' in c_low:
                lang_code = 'es'
            elif 'germany' in c_low:
                lang_code = 'de'
            elif 'italy' in c_low:
                lang_code = 'it'

            year_val = clean_year(row.get('release_year'), 2020)
            director = str(row.get('director') or '')
            if director == 'nan':
                director = ''
            cast = str(row.get('cast') or '')
            if cast == 'nan':
                cast = ''
            genres_raw = str(row.get('listed_in') or 'Drama')
            genres_clean = " ".join([g.strip() for g in genres_raw.split(',') if g.strip()])
            desc = str(row.get('description') or '')
            if desc == 'nan':
                desc = ''
            
            dur_str = str(row.get('duration') or '')
            dur_val = 115
            dur_match = re.search(r'(\d+)\s*min', dur_str)
            if dur_match:
                dur_val = int(dur_match.group(1))

            movie_id = id_base + idx
            show_id = str(row.get('show_id') or f"st_{idx}")

            rec = {
                "movie_id": movie_id,
                "tmdb_id": str(movie_id),
                "imdb_id": show_id,
                "title": title,
                "original_title": title,
                "overview": desc or f"A premier {stream_name} release ({year_val}) exploring {genres_clean.lower()}.",
                "release_date": f"{year_val}-01-01",
                "year": int(year_val),
                "original_language": lang_code,
                "languages": lang_code.upper(),
                "countries": first_country,
                "genres": genres_clean,
                "keywords": f"{stream_name} {first_country}",
                "cast": cast,
                "director": director,
                "runtime": int(dur_val),
                "vote_average": 7.4,
                "vote_count": 120,
                "popularity": 15.0,
                "poster_path": "",
                "backdrop_path": "",
            }
            rec["tags"] = build_smart_soup(rec)
            all_records.append(rec)
            st_count += 1

        print(f"✅ Ingested {st_count:,} new {stream_name} titles.", flush=True)

    # -------------------------------------------------------------------------
    # 3. Ingest User Indian Cinema Dataset (Multi-lingual deduplication)
    # -------------------------------------------------------------------------
    if os.path.exists(INDIAN_CSV_PATH):
        print(f"📂 Reading Indian Movies CSV: {INDIAN_CSV_PATH}...", flush=True)
        ind_df = pd.read_csv(INDIAN_CSV_PATH)

        grouped_ind = {}
        for idx, row in ind_df.iterrows():
            raw_name = str(row.get('Movie Name') or '').strip()
            if not raw_name or raw_name == '-':
                continue
            norm_k = norm_clean_str(raw_name)
            if not norm_k:
                continue
            if norm_k not in grouped_ind:
                grouped_ind[norm_k] = []
            grouped_ind[norm_k].append((idx, row))

        ind_count = 0
        for norm_k, group in grouped_ind.items():
            if norm_k in seen_titles:
                continue
            seen_titles.add(norm_k)

            all_langs = []
            best_idx, best_row = group[0]
            best_score = -1

            known_kn = ["kgf", "kantara", "googly", "ramachari", "ramchari", "kirikparty", "charlie777", "vikrantrona", "tagaru", "mufti", "salaga", "dia", "lovemocktail", "rajakumara", "uturn", "rangitaranga", "lucia", "ulidavarukandanthe", "yuvarathnaa", "roberrt", "kurukshetra"]
            known_te = ["rrr", "baahubali", "pushpa", "salaar", "magadheera", "eega", "arjunreddy", "rangasthalam", "hanuman", "kalki", "geethagovindam", "alavaikunthapurramuloo", "sitaramam"]
            known_ta = ["vikram", "jailer", "leo", "kaithi", "master", "ponniyinselvan", "asuran", "superdeluxe", "petta", "mankatha", "mersal", "bigil", "thupakki"]
            known_ml = ["manjummelboys", "lucifer", "drishyam", "kumbalanginights", "premam", "minnalmurali", "rdx", "bramayugam", "premalu", "aavesham", "malik"]

            is_kn = any(k in norm_k for k in known_kn)
            is_te = any(k in norm_k for k in known_te)
            is_ta = any(k in norm_k for k in known_ta)
            is_ml = any(k in norm_k for k in known_ml)

            for g_idx, g_row in group:
                raw_lang = str(g_row.get('Language') or 'hindi').lower().strip()
                l_code = LANG_CODE_MAP.get(raw_lang, 'hi')
                if l_code not in all_langs:
                    all_langs.append(l_code)

                v = int(clean_number(g_row.get('Votes'), 0))
                r = clean_number(g_row.get('Rating(10)'), 0.0)
                cur_score = v * 10 + r

                if is_kn and l_code == 'kn':
                    cur_score += 1000000
                elif is_te and l_code == 'te':
                    cur_score += 1000000
                elif is_ta and l_code == 'ta':
                    cur_score += 1000000
                elif is_ml and l_code == 'ml':
                    cur_score += 1000000

                if cur_score > best_score:
                    best_score = cur_score
                    best_idx, best_row = g_idx, g_row

            raw_name = clean_title_canonical(str(best_row.get('Movie Name') or '').strip())
            raw_lang = str(best_row.get('Language') or 'hindi').lower().strip()
            lang_code = LANG_CODE_MAP.get(raw_lang, 'hi')
            if is_kn:
                lang_code = 'kn'
            elif is_te and not is_kn:
                lang_code = 'te'
            elif is_ta and not is_kn and not is_te:
                lang_code = 'ta'
            elif is_ml and not is_kn and not is_te and not is_ta:
                lang_code = 'ml'

            year_val = clean_year(best_row.get('Year'))
            rating_val = clean_number(best_row.get('Rating(10)'), 7.2)
            votes_val = int(clean_number(best_row.get('Votes'), 150))
            runtime_val = clean_number(str(best_row.get('Timing(min)') or '').replace('min', ''), 140)
            
            raw_genre = str(best_row.get('Genre') or '').replace('-', '').strip()
            genre_str = " ".join([g.strip() for g in raw_genre.split(',') if g.strip()]) if raw_genre else "Action Drama"

            imdb_id = str(best_row.get('ID') or '').strip()
            if not imdb_id or imdb_id == '-':
                imdb_id = f"tt_ind_{best_idx}"

            movie_id = 9000000 + best_idx

            aliases = [raw_name]
            if "k.g.f" in raw_name.lower() or "kgf" in raw_name.lower():
                aliases.extend(["kgf", "kolar gold fields", "rocky bhai", "yash", "prashanth neel"])
            if "kantara" in raw_name.lower():
                aliases.extend(["kantara", "panjurli", "bhoota kola", "rishab shetty"])
            if "ramchari" in raw_name.lower() or "ramachari" in raw_name.lower():
                aliases.extend(["ramachari", "mr and mrs ramachari", "yash", "radhika pandit"])
            if "googly" in raw_name.lower():
                aliases.extend(["googly", "yash", "kriti kharbanda"])

            alias_str = " ".join(aliases)

            rec = {
                "movie_id": movie_id,
                "tmdb_id": str(movie_id),
                "imdb_id": imdb_id,
                "title": raw_name,
                "original_title": raw_name,
                "overview": "",
                "release_date": f"{year_val}-01-01",
                "year": int(year_val),
                "original_language": str(lang_code),
                "languages": ", ".join([l.upper() for l in all_langs]),
                "countries": "India",
                "genres": genre_str,
                "keywords": alias_str,
                "cast": "",
                "director": "",
                "runtime": int(runtime_val) if runtime_val > 0 else 140,
                "vote_average": round(float(rating_val) if rating_val > 0 else 7.4, 1),
                "vote_count": int(votes_val) if votes_val > 0 else 100,
                "popularity": round(float(rating_val * (np.log1p(votes_val) + 1)), 2),
                "poster_path": "",
                "backdrop_path": "",
            }
            rec["tags"] = build_smart_soup(rec)
            all_records.append(rec)
            ind_count += 1

        print(f"✅ Ingested {ind_count:,} distinct Indian titles.", flush=True)

    # -------------------------------------------------------------------------
    # 4. Master Unified DataFrame Construction & Normalization
    # -------------------------------------------------------------------------
    combined_df = pd.DataFrame(all_records)
    
    # Global Deduplication
    combined_df["_clean_title"] = combined_df["title"].astype(str).apply(norm_clean_str)
    combined_df = combined_df.dropna(subset=['movie_id', 'title']).drop_duplicates(subset=['_clean_title']).drop(columns=['_clean_title']).reset_index(drop=True)

    # Sanitization
    combined_df["movie_id"] = pd.to_numeric(combined_df["movie_id"], errors='coerce').fillna(0).astype(np.int64)
    combined_df["year"] = pd.to_numeric(combined_df["year"], errors='coerce').fillna(2000).astype(np.int32)
    combined_df["runtime"] = pd.to_numeric(combined_df["runtime"], errors='coerce').fillna(120).astype(np.int32)
    combined_df["vote_average"] = pd.to_numeric(combined_df["vote_average"], errors='coerce').fillna(7.0).astype(np.float64)
    combined_df["vote_count"] = pd.to_numeric(combined_df["vote_count"], errors='coerce').fillna(50).astype(np.int64)
    combined_df["popularity"] = pd.to_numeric(combined_df["popularity"], errors='coerce').fillna(5.0).astype(np.float64)

    str_cols = ["tmdb_id", "imdb_id", "title", "original_title", "overview", "release_date", "original_language", "languages", "countries", "genres", "keywords", "cast", "director", "poster_path", "backdrop_path", "tags"]
    for sc in str_cols:
        if sc in combined_df.columns:
            combined_df[sc] = combined_df[sc].fillna("").astype(str)

    print("\n" + "=" * 80, flush=True)
    print(f"🎬 Grand CineMatch Unified Catalog: {len(combined_df):,} verified titles!", flush=True)
    print(f"🌐 Languages Represented: {combined_df['original_language'].nunique():,} distinct languages", flush=True)
    print("\n📊 Regional Breakdown:", flush=True)
    for lang, count in combined_df['original_language'].value_counts().head(16).items():
        print(f"   * {str(lang).upper()}: {count:,} movies", flush=True)
    print("=" * 80, flush=True)

    # -------------------------------------------------------------------------
    # 5. Export to Parquet & Pickle
    # -------------------------------------------------------------------------
    print(f"💾 Saving to Parquet: {PARQUET_OUT}...", flush=True)
    combined_df.to_parquet(PARQUET_OUT, index=False, engine="pyarrow")

    print(f"💾 Saving to Pickle: {MOVIES_PKL}...", flush=True)
    with open(MOVIES_PKL, 'wb') as f:
        pickle.dump(combined_df, f, protocol=pickle.HIGHEST_PROTOCOL)

    # -------------------------------------------------------------------------
    # 6. Compute Chunked Top-35 Similarity Graph
    # -------------------------------------------------------------------------
    print("\n🧠 Computing Smart Bi-Gram TF-IDF Embeddings (40,000 features)...", flush=True)
    vectorizer = TfidfVectorizer(
        max_features=40000,
        stop_words="english",
        ngram_range=(1, 2),
        min_df=2
    )
    tfidf_matrix = vectorizer.fit_transform(combined_df["tags"].fillna(""))

    print(f"⚡ Building Top-35 Nearest Neighbors Graph ({len(combined_df):,} nodes)...", flush=True)
    model = NearestNeighbors(
        n_neighbors=min(36, len(combined_df)),
        metric="cosine",
        algorithm="brute",
        n_jobs=-1
    )
    model.fit(tfidf_matrix)

    compact_sim = {}
    batch_size = 2500
    n_samples = tfidf_matrix.shape[0]

    for start_idx in range(0, n_samples, batch_size):
        end_idx = min(start_idx + batch_size, n_samples)
        batch_matrix = tfidf_matrix[start_idx:end_idx]
        distances, indices = model.kneighbors(batch_matrix)

        for b_offset, (dists, idxs) in enumerate(zip(distances, indices)):
            global_row_idx = start_idx + b_offset
            entries = []
            for distance, idx in zip(dists, idxs):
                if int(idx) == global_row_idx:
                    continue
                score = max(0.0, 1.0 - float(distance))
                entries.append((int(idx), round(score, 4)))
            compact_sim[global_row_idx] = entries[:35]

        print(f"  --> Processed {end_idx:,} / {n_samples:,} movie similarity nodes...", flush=True)

    print(f"💾 Saving Top-35 Similarity Graph: {SIM_PKL}...", flush=True)
    with open(SIM_PKL, "wb") as f:
        pickle.dump(compact_sim, f, protocol=pickle.HIGHEST_PROTOCOL)

    print("\n🎉 Grand Multi-Source Catalog Fusion Completed Successfully!", flush=True)


if __name__ == "__main__":
    fuse_all_datasets()
