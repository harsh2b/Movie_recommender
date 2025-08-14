
import pickle
import requests
import pandas as pd
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# ---------------------
# Load Data
# ---------------------

try:
    with open('Movie_recommended_model.pkl', 'rb') as f:
        movies_df = pickle.load(f)
except FileNotFoundError:
    raise RuntimeError("Could not find 'Movie_recommended_model.pkl'. Make sure the file is in the correct directory.")

try:
    with open('Similarity.pkl', 'rb') as b:
        similarity = pickle.load(b)
except FileNotFoundError:
    raise RuntimeError("Could not find 'Similarity.pkl'. Make sure the file is in the correct directory.")


# ---------------------
# FastAPI App
# ---------------------

app = FastAPI(
    title="Movie Recommendation API",
    description="An API to get movie recommendations and details.",
    version="1.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://recommender.harshkb.shop", "http://recommender.harshkb.shop"],  # Allow your frontend domain (both HTTPS and HTTP)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# ---------------------
# Pydantic Models (for request/response validation)
# ---------------------

class Movie(BaseModel):
    id: str
    title: str
    genres: list[str]
    poster: str
    description: str | None = None

class MovieList(BaseModel):
    movies: list[str]

class RecommendationResponse(BaseModel):
    recommendations: list[Movie]

# ---------------------
# Helper Functions
# ---------------------

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_BASE_URL = "https://api.themoviedb.org/3"

def fetch_movie_details(movie_id: int) -> tuple[str, list[str], str] | tuple[None, None, None]:
    """Fetch movie poster, genres, and description using TMDB API.
    Requires TMDB_API_KEY to be set in .env file.
    """
    if not TMDB_API_KEY:
        print("TMDB_API_KEY not found in .env. Using placeholder data.")
        return "https://via.placeholder.com/500x750/1a0b3d/a855f7?text=No+Image+Available", ["Action", "Adventure", "Sci-Fi"], "This is a placeholder description for the movie."

    try:
        response = requests.get(f"{TMDB_BASE_URL}/movie/{movie_id}?api_key={TMDB_API_KEY}", timeout=10)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()

        poster_path = data.get("poster_path")
        poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else "https://via.placeholder.com/500x750/1a0b3d/a855f7?text=No+Image+Available"
        genres = [genre["name"] for genre in data.get("genres", [])]
        description = data.get("overview", "No description available.")
        
        return poster_url, genres, description
    except requests.exceptions.RequestException as e:
        print(f"Error fetching movie details from TMDB: {e}")
        return None, None, None

# ---------------------
# API Endpoints
# ---------------------

@app.get("/api/movies", response_model=MovieList)
async def get_movie_list():
    """Returns a list of all movie titles."""
    return {"movies": movies_df['title'].tolist()}

@app.get("/api/recommendations", response_model=RecommendationResponse)
async def get_recommendations(movie_title: str):
    """Recommends movies based on a given movie title."""
    if movie_title not in movies_df['title'].values:
        raise HTTPException(status_code=404, detail="Movie not found")

    movie_index = movies_df[movies_df['title'] == movie_title].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:9]

    recommendations = []
    for i in movie_list:
        movie_row = movies_df.iloc[i[0]]
        movie_id = movie_row['movie_id']
        poster, genres, _ = fetch_movie_details(movie_id)
        
        recommendations.append(Movie(
            id=str(movie_id),
            title=movie_row['title'],
            genres=genres if genres else [],
            poster=poster if poster else "https://via.placeholder.com/500x750/1a0b3d/a855f7?text=No+Image+Available"
        ))
    
    return {"recommendations": recommendations}

@app.get("/api/movie/{movie_id}", response_model=Movie)
async def get_movie_details_by_id(movie_id: int):
    """Fetches detailed information for a specific movie by its ID."""
    poster, genres, description = fetch_movie_details(movie_id)
    
    if poster is None:
        raise HTTPException(status_code=404, detail="Movie details not found or could not be fetched.")

    # We need to find the title from our dataframe
    movie_title = movies_df[movies_df['movie_id'] == movie_id]['title'].iloc[0]

    return Movie(
        id=str(movie_id),
        title=movie_title,
        genres=genres if genres else [],
        poster=poster,
        description=description
    )


# Serve static files
app.mount("/", StaticFiles(directory="static", html=True), name="static")

# To run this app, use the command: uvicorn app:app --reload
