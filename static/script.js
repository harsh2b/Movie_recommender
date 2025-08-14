// CineVerse Movie Recommendation System
// JavaScript functionality with backend integration points

class CineVerseApp {
    constructor() {
        this.movieSelect = document.getElementById('movieSelect');
        this.recommendBtn = document.getElementById('getRecommendations');
        this.moviesGrid = document.getElementById('moviesGrid');
        this.loadingContainer = document.getElementById('loadingContainer');
        this.recommendationsSection = document.getElementById('recommendationsSection');
        
        this.init();
    }

    init() {
        // Load initial movie list for dropdown
        this.loadMovieList();
        
        // Event listeners
        this.recommendBtn.addEventListener('click', () => this.getRecommendations());
        this.movieSelect.addEventListener('change', () => this.onMovieSelect());
        
        // Add keyboard support
        this.movieSelect.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                this.getRecommendations();
            }
        });
    }

    // ========================================
    // BACKEND INTEGRATION POINT #1
    // Load movie list for dropdown selection
    // ========================================
    async loadMovieList() {
        try {
            // TODO: Replace this with your actual backend API call
            // Example API call:
            // const response = await fetch('/api/movies/popular');
            // const movies = await response.json();
            
            const response = await fetch('/api/movies');
            const data = await response.json();
            this.populateMovieDropdown(data.movies.map(title => ({ id: title, title: title })));
            
        } catch (error) {
            console.error('Error loading movie list:', error);
            this.showError('Failed to load movie list');
        }
    }

    populateMovieDropdown(movies) {
        // Clear existing options except the first one
        const firstOption = this.movieSelect.querySelector('option[value=""]');
        this.movieSelect.innerHTML = '';
        this.movieSelect.appendChild(firstOption);
        
        // Add movie options
        movies.forEach(movie => {
            const option = document.createElement('option');
            option.value = movie.id;
            option.textContent = movie.title;
            this.movieSelect.appendChild(option);
        });
    }

    onMovieSelect() {
        const selectedMovie = this.movieSelect.value;
        if (selectedMovie) {
            this.recommendBtn.disabled = false;
            this.recommendBtn.style.opacity = '1';
        } else {
            this.recommendBtn.disabled = true;
            this.recommendBtn.style.opacity = '0.6';
        }
    }

    // ========================================
    // BACKEND INTEGRATION POINT #2
    // Get movie recommendations based on selected movie
    // ========================================
    async getRecommendations() {
        const selectedMovie = this.movieSelect.value;
        
        if (!selectedMovie) {
            this.showError('Please select a movie first');
            return;
        }

        this.showLoading(true);

        try {
            // TODO: Replace this with your actual backend API call
            // Example API call:
            // const response = await fetch(`/api/recommendations/${selectedMovie}`, {
            //     method: 'POST',
            //     headers: {
            //         'Content-Type': 'application/json',
            //     },
            //     body: JSON.stringify({
            //         movie_id: selectedMovie,
            //         user_preferences: this.getUserPreferences(), // if you have user preferences
            //         limit: 10 // number of recommendations
            //     })
            // });
            // const recommendations = await response.json();

            const response = await fetch(`/api/recommendations?movie_title=${encodeURIComponent(selectedMovie)}`);
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Failed to fetch recommendations');
            }
            const data = await response.json();
            
            this.displayRecommendations(data.recommendations);
            
        } catch (error) {
            console.error('Error getting recommendations:', error);
            this.showError('Failed to get recommendations. Please try again.');
        } finally {
            this.showLoading(false);
        }
    }

    

    displayRecommendations(recommendations) {
        this.moviesGrid.innerHTML = '';
        
        recommendations.forEach(movie => {
            const movieCard = this.createMovieCard(movie);
            this.moviesGrid.appendChild(movieCard);
        });

        // Scroll to recommendations
        this.recommendationsSection.scrollIntoView({ 
            behavior: 'smooth',
            block: 'start'
        });
    }

    createMovieCard(movie) {
        const card = document.createElement('div');
        card.className = 'movie-card';
        card.setAttribute('data-movie-id', movie.id);
        
        // Add click event for movie details
        card.addEventListener('click', () => this.onMovieClick(movie));
        
        card.innerHTML = `
            <div class="movie-poster">
                <img src="${movie.poster}" 
                     alt="${movie.title} Poster"
                     onerror="this.src='https://via.placeholder.com/300x450/1a1a2e/ffffff?text=No+Image'">
                <div class="movie-overlay">
                    </div>
            </div>
            <div class="movie-info">
                <h3 class="movie-title">${movie.title}</h3>
                <div class="movie-genres">
                    ${movie.genres.map(genre => `<span class="genre-tag">${genre}</span>`).join('')}
                </div>
            </div>
        `;
        
        return card;
    }

    // ========================================
    // BACKEND INTEGRATION POINT #4
    // Handle movie click for detailed view
    // ========================================
    async onMovieClick(movie) {
        try {
            const response = await fetch(`/api/movie/${movie.id}`);
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Failed to fetch movie details');
            }
            const movieDetails = await response.json();
            alert(`Movie Details:\nTitle: ${movieDetails.title}\nGenres: ${movieDetails.genres.join(', ')}\nDescription: ${movieDetails.description}`);
        } catch (error) {
            console.error('Error fetching movie details:', error);
            this.showError('Failed to get movie details. Please try again.');
        }
    }

    // ========================================
    // UTILITY FUNCTIONS
    // ========================================
    showLoading(show) {
        if (show) {
            this.loadingContainer.style.display = 'block';
            this.recommendationsSection.style.display = 'none';
        } else {
            this.loadingContainer.style.display = 'none';
            this.recommendationsSection.style.display = 'block';
        }
    }

    showError(message) {
        // TODO: Implement proper error handling UI
        // You could create a toast notification or error modal
        alert(message);
    }

    

    // ========================================
    // ADDITIONAL BACKEND INTEGRATION POINTS
    // ========================================
    
    // User preferences (if you want to implement user accounts)
    getUserPreferences() {
        // TODO: Get user preferences from backend or local storage
        // return {
        //     favorite_genres: ['Action', 'Sci-Fi'],
        //     preferred_rating_min: 7.0,
        //     preferred_year_range: [2010, 2023],
        //     language: 'en'
        // };
        return {};
    }

    // Rating system
    async rateMovie(movieId, rating) {
        // TODO: Send rating to backend
        // const response = await fetch(`/api/movies/${movieId}/rate`, {
        //     method: 'POST',
        //     headers: { 'Content-Type': 'application/json' },
        //     body: JSON.stringify({ rating: rating })
        // });
        console.log(`Rating movie ${movieId}: ${rating}`);
    }

    // Watchlist functionality
    async addToWatchlist(movieId) {
        // TODO: Add movie to user's watchlist
        // const response = await fetch(`/api/watchlist/add`, {
        //     method: 'POST',
        //     headers: { 'Content-Type': 'application/json' },
        //     body: JSON.stringify({ movie_id: movieId })
        // });
        console.log(`Added movie ${movieId} to watchlist`);
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new CineVerseApp();
});

// ========================================
// BACKEND API ENDPOINTS YOU NEED TO IMPLEMENT:
// ========================================
/*

1. GET /api/movies/popular
   - Returns list of popular movies for dropdown
   - Response: [{ id: string, title: string }, ...]

2. POST /api/recommendations/{movie_id}
   - Returns movie recommendations based on selected movie
   - Request body: { movie_id: string, user_preferences?: object, limit?: number }
   - Response: [{ id: string, title: string, rating: string, genres: string[], poster_url?: string }, ...]

3. GET /api/movies/{movie_id}/poster
   - Returns movie poster image URL or serves the image directly

4. GET /api/movies/{movie_id}
   - Returns detailed movie information
   - Response: { id: string, title: string, description: string, rating: string, genres: string[], year: number, ... }

5. POST /api/movies/{movie_id}/rate (optional)
   - Allows users to rate movies
   - Request body: { rating: number }

6. POST /api/watchlist/add (optional)
   - Adds movie to user's watchlist
   - Request body: { movie_id: string }

7. GET /api/user/preferences (optional)
   - Returns user preferences for personalized recommendations
   - Response: { favorite_genres: string[], preferred_rating_min: number, ... }

*/

