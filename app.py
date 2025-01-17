import streamlit as st
import pickle
import requests

# Function to fetch movie details like poster, genres, and description
def fetch_movie_details(movie_id):
    api_key = '345627e8aa0cea1b0fbc016806f23346'
    base_url = "https://api.themoviedb.org/3/movie/"
    response = requests.get(f"{base_url}{movie_id}?api_key={api_key}")

    if response.status_code == 200:
        data = response.json()
        poster_url = f"https://image.tmdb.org/t/p/w500{data['poster_path']}"
        genres = [genre['name'] for genre in data.get('genres', [])]
        description = data.get('overview', 'No description available.')
        return poster_url, genres, description
    return None, None, None

# Function to recommend movies
def recommend(movie):
    movie_index = movies_df[movies_df['title'] == movie].index[0]  # Use DataFrame to get the index
    distances = similarity[movie_index]  # Get similarity scores
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movies = []
    recommended_posters = []
    recommended_movie_ids = []

    for i in movie_list:
        movie_id = movies_df.iloc[i[0]].movie_id  # Use the DataFrame to get movie_id
        title = movies_df.iloc[i[0]].title  # Fetch the title
        poster = fetch_movie_details(movie_id)[0]  # Fetch poster
        recommended_movies.append(title)
        recommended_posters.append(poster)
        recommended_movie_ids.append(movie_id)

    return recommended_movies, recommended_posters, recommended_movie_ids

# Load the model and similarity data
with open('Movie_recommended_model.pkl', 'rb') as f:
    movies_df = pickle.load(f)  # Load the DataFrame directly


# Initialize an empty list to combine parts
similarity_combined = []

# Load each part and append to the combined list
for i in range(1, 9):  # Assuming 8 parts
    with open(f'Similarity_part{i}.pkl', 'rb') as b:
        part = pickle.load(b)
        similarity_combined.extend(part)

# Assign the combined data to similarity
similarity = similarity_combined

# Now `similarity` contains the full data loaded from all parts


# Set the page configuration
st.set_page_config(page_title="Movie Recommendation System", page_icon="🎥", layout="wide")

# Apply custom CSS for styling
st.markdown("""
    <style>
        .title {
            font-size: 40px;
            color: #1F8A70;
            font-family: 'Arial', sans-serif;
            font-weight: bold;
            text-align: center;
        }
        .subheader {
            font-size: 25px;
            color: #2F4F4F;
            font-family: 'Arial', sans-serif;
        }
        .movie-name {
            font-size: 18px;
            font-weight: bold;
            text-align: center;
            color: #333;
            cursor: pointer;
            transition: 0.3s;
        }
        .movie-name:hover {
            color: #FF5733;
        }
        .genre {
            font-size: 16px;
            color: #999;
            font-weight: 600;
        }
        .description {
            font-size: 16px;
            color: #555;
            line-height: 1.5;
        }
        .stButton>button {
            background-color: #FF5733;
            color: white;
            font-size: 18px;
            border-radius: 10px;
            padding: 10px;
            cursor: pointer;
            transition: 0.3s;
        }
        .stButton>button:hover {
            background-color: #1F8A70;
        }
        .movie-poster {
            border-radius: 10px;
            box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.1);
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="title">🎬 Movie Recommendation System</div>', unsafe_allow_html=True)

# Movie selection
selected_movie_name = st.selectbox("🔍 Select a movie to get recommendations", movies_df['title'].values)

# Recommendation logic
if st.button('Get Recommendations'):
    names, posters, movie_ids = recommend(selected_movie_name)
    
    # Displaying all recommended movies in a single row
    cols = st.columns(5)  # Create 5 columns for the recommendations
    
    for i in range(len(names)):
        with cols[i]:
            st.markdown(f'<p class="movie-name">{names[i]}</p>', unsafe_allow_html=True)
            st.image(posters[i], caption=names[i], width=200)
            if st.button(f"More Info for {names[i]}", key=f"info_{i}"):  # Button for more information
                poster, genres, description = fetch_movie_details(movie_ids[i])  # Fetch movie details
                st.image(poster, width=250)
                st.markdown(f'<p class="subheader">Genres:</p>', unsafe_allow_html=True)
                st.markdown(f'<p class="genre">{" ,".join(genres)}</p>', unsafe_allow_html=True)
                st.markdown(f'<p class="subheader">Storyline:</p>', unsafe_allow_html=True)
                st.markdown(f'<p class="description">{description}</p>', unsafe_allow_html=True)

