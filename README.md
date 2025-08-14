# Movie Recommender Application

A web application that provides movie recommendations based on a selected movie. The backend is built with FastAPI and the frontend is built with HTML, CSS, and vanilla JavaScript.

## Features

- **Movie Selection**: Choose a movie from a dropdown list populated with available titles.
- **Get Recommendations**: Receive a list of 8 similar movies based on your selection.
- **Dynamic Details**: Movie posters, genres, and descriptions are fetched dynamically from the TMDB API.
- **Containerized**: The entire application is containerized using Docker for easy setup and deployment.

## Tech Stack

- **Backend**: Python, FastAPI
- **Frontend**: HTML, CSS, JavaScript
- **API**: TMDB API for movie details
- **Containerization**: Docker & Docker Compose

## Prerequisites

- Docker and Docker Compose must be installed on your system.
- You must have an API key from [The Movie Database (TMDB)](https://www.themoviedb.org/settings/api).

## How to Run

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/harsh2b/Movie_recommender.git
    cd Movie_recommender
    ```

2.  **Create an environment file:**
    Create a file named `.env` in the root of the project directory and add your TMDB API key like so:
    ```
    TMDB_API_KEY=your_key_here
    ```

3.  **Build and run the application:**
    Use Docker Compose to build the image and run the container in detached mode.
    ```bash
    docker-compose up --build -d
    ```

4.  **Access the application:**
    Open your web browser and navigate to:
    [http://localhost:8082](http://localhost:8082)

## API Endpoints

The application exposes the following API endpoints:

- `GET /api/movies`
  - **Description**: Returns a JSON list of all available movie titles.
  - **Response**: `{"movies": ["Movie 1", "Movie 2", ...]}`

- `GET /api/recommendations`
  - **Description**: Returns movie recommendations for a given title.
  - **Query Parameter**: `movie_title` (e.g., `/api/recommendations?movie_title=Avatar`)
  - **Response**: A JSON object containing a list of recommended movie objects.

- `GET /api/movie/{movie_id}`
  - **Description**: Fetches detailed information for a specific movie by its ID.
  - **Response**: A JSON object containing the movie's ID, title, genres, poster URL, and description.
