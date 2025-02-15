import streamlit as st 
import pickle
import requests



api_key = st.secrets["api_key"]

# ---------------------
# Helper Functions
# ---------------------
def fetch_movie_details(movie_id):
    """Fetch movie poster, genres, and description using TMDB API."""
    api_key = 'TMDB_API_KEY'
    base_url = "https://api.themoviedb.org/3/movie/"
    response = requests.get(f"{base_url}{movie_id}?api_key={api_key}")

    if response.status_code == 200:
        data = response.json()
        poster_url = f"https://image.tmdb.org/t/p/w500{data.get('poster_path', '')}"
        genres = [genre['name'] for genre in data.get('genres', [])]
        description = data.get('overview', 'No description available.')
        return poster_url, genres, description
    return None, None, None

def recommend(movie_title, top_n=5):
    """Recommend movies based on similarity."""
    if movie_title not in movies_df['title'].values:
        return [], [], [], []
    
    movie_index = movies_df[movies_df['title'] == movie_title].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:top_n+1]
    
    recommendations = []
    posters = []
    movie_ids = []
    genres_list = []
    
    for i in movie_list:
        movie_row = movies_df.iloc[i[0]]
        # Using the 'movie_id' column
        movie_id = movie_row['movie_id']
        poster, genres, _ = fetch_movie_details(movie_id)
        
        recommendations.append(movie_row['title'])
        posters.append(poster)
        movie_ids.append(movie_id)
        genres_list.append(genres)
    
    return recommendations, posters, movie_ids, genres_list

# ---------------------
# Load Data
# ---------------------
with open('Movie_recommended_model.pkl', 'rb') as f:
    movies_df = pickle.load(f)

similarity_combined = []
for i in range(1, 9):
    with open(f'Similarity_{i}.pkl', 'rb') as b:
        similarity_combined.extend(pickle.load(b))

similarity = similarity_combined

# ---------------------
# Styling & Config
# ---------------------
st.set_page_config(page_title="Movie Recommendation System", page_icon="🎥", layout="wide")

# Updated CSS to force a true black background and modern cyan accent colors.
st.markdown("""
    <style>
        /* Force black background for the main app */
        .stApp, .reportview-container {
            background-color: #000 !important;
        }
        /* Sidebar background */
        .sidebar .sidebar-content {
            background-color: #111 !important;
        }
        /* General text styling */
        body, .block-container {
            color: #e0e0e0;
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        }
        /* Override label color for selectbox and other form elements */
        label {
            color: #00bcd4 !important;
            font-weight: 500;
        }
        /* Title styling */
        .title {
            font-size: 48px; 
            color: #00bcd4;
            text-align: center;
            margin-top: 20px;
            margin-bottom: 20px;
        }
        /* Movie title styling */
        .movie-title {
            font-size: 20px; 
            color: #ffffff;
            text-align: center;
            margin-top: 10px;
        }
        /* Highlighted genre styling */
        .genre {
            font-size: 14px; 
            color: #00bcd4; /* Modern cyan accent color */
            text-align: center;
            font-weight: bold;
            background-color: #222;
            padding: 4px 8px;
            border-radius: 4px;
            display: inline-block;
            margin-top: 5px;
        }
        /* Button styling */
        .stButton>button {
            background-color: #00bcd4;
            color: #ffffff;
            font-size: 16px;
            border: none;
            padding: 8px 16px;
            border-radius: 8px;
            cursor: pointer;
            margin-top: 10px;
        }
        .stButton>button:hover {
            background-color: #0097a7;
        }
        /* Movie poster styling */
        .movie-poster {
            border-radius: 10px; 
            box-shadow: 0px 4px 15px rgba(255, 255, 255, 0.2);
        }
    </style>
""", unsafe_allow_html=True)

# ---------------------
# Main Recommendation Page
# ---------------------
st.markdown('<div class="title">🎬 Movie Recommendation System</div>', unsafe_allow_html=True)

# Movie selection (the label "🔍 Select a movie" now appears in modern cyan)
title_selected = st.selectbox("🔍 Select a movie", movies_df['title'].values)

# Get recommendations (default 5 recommendations)
if st.button('Get Recommendations'):
    names, posters, movie_ids, genres_list = recommend(title_selected, top_n=5)
    
    cols = st.columns(min(len(names), 5))
    for i in range(len(names)):
        with cols[i % 5]:
            st.markdown(f'<p class="movie-title">{names[i]}</p>', unsafe_allow_html=True)
            if posters[i]:
                st.image(posters[i], caption=names[i], width=200)
            if genres_list[i]:
                genres_formatted = ", ".join(genres_list[i])
                st.markdown(f'<p class="genre">Genres: {genres_formatted}</p>', unsafe_allow_html=True)
