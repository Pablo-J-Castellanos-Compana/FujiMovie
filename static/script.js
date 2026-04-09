let currentMovieId = null;
const API_BASE = '/api/movies';

// Cargar películas al iniciar
document.addEventListener('DOMContentLoaded', () => {
    loadMovies();
    
    // Event listeners para búsqueda y filtros
    document.getElementById('searchInput').addEventListener('input', filterMovies);
    document.getElementById('genreFilter').addEventListener('change', filterMovies);
});

async function loadMovies() {
    try {
        const response = await fetch(`${API_BASE}`);
        const movies = await response.json();
        displayMovies(movies);
    } catch (error) {
        console.error('Error loading movies:', error);
        document.getElementById('moviesContainer').innerHTML = 
            '<div class="loading">Error al cargar películas</div>';
    }
}

function displayMovies(movies) {
    const container = document.getElementById('moviesContainer');
    container.innerHTML = '';
    
    if (movies.length === 0) {
        container.innerHTML = '<div class="loading">No se encontraron películas</div>';
        return;
    }
    
    movies.forEach((movie, index) => {
        const card = createMovieCard(movie);
        container.appendChild(card);
        // Animación staggered
        setTimeout(() => {
            card.style.animation = 'cardEnter 0.5s ease-out forwards';
        }, index * 50);
    });
}

function createMovieCard(movie) {
    const card = document.createElement('div');
    card.className = 'movie-card';
    card.onclick = () => window.location.href = `/detail.html?id=${movie.id}`;
    card.style.cursor = 'pointer';
    card.innerHTML = `
        <div class="movie-poster">🎬</div>
        <div class="movie-content">
            <h3 class="movie-title">${movie.title}</h3>
            <div class="movie-meta">
                <span>${movie.year}</span>
                <span class="movie-genre">${movie.genre}</span>
            </div>
            <p class="movie-description">${movie.description || 'Sin descripción'}</p>
            <div class="rating-section">
                <span class="rating-display">★ ${movie.stars || 0}</span>
                <span class="rating-count" data-movie-id="${movie.id}">0 valoraciones</span>
            </div>
            <div class="button-group">
                <button class="btn btn-rate" onclick="event.stopPropagation(); openRatingModal(${movie.id}, '${movie.title}')">
                    💫 Valorar
                </button>
                <button class="btn btn-library" onclick="event.stopPropagation(); addToLibrary(${movie.id})">
                    📚 Biblioteca
                </button>
            </div>
        </div>
    `;
    
    // Cargar contador de valoraciones
    fetchRatingCount(movie.id, card);
    
    return card;
}

async function fetchRatingCount(movieId, card) {
    try {
        const response = await fetch(`${API_BASE}/${movieId}/ratings`);
        const data = await response.json();
        const countElement = card.querySelector(`[data-movie-id="${movieId}"]`);
        if (countElement) {
            countElement.textContent = `${data.count} ${data.count === 1 ? 'valoración' : 'valoraciones'}`;
        }
    } catch (error) {
        console.error('Error fetching rating count:', error);
    }
}

function openRatingModal(movieId, movieTitle) {
    currentMovieId = movieId;
    document.getElementById('movieTitle').textContent = movieTitle;
    document.getElementById('ratingModal').classList.remove('hidden');
    document.getElementById('userName').value = '';
    document.querySelectorAll('.star-rating input').forEach(input => input.checked = false);
}

function closeRatingModal() {
    document.getElementById('ratingModal').classList.add('hidden');
    currentMovieId = null;
}

async function submitRating() {
    const score = document.querySelector('.star-rating input:checked')?.value;
    const user = document.getElementById('userName').value.trim();
    
    if (!score) {
        alert('Por favor, selecciona una calificación');
        return;
    }
    
    if (!user) {
        alert('Por favor, ingresa tu nombre');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/${currentMovieId}/rate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                user: user,
                score: parseFloat(score)
            })
        });
        
        if (response.ok) {
            createExplosion();
            closeRatingModal();
            loadMovies();
            showSuccessMessage(`¡${user} ha valorado la película con ${score} ⭐!`);
        } else {
            alert('Error al valorar la película');
        }
    } catch (error) {
        console.error('Error submitting rating:', error);
        alert('Error al enviar la valoración');
    }
}

function createExplosion() {
    const container = document.getElementById('explosionContainer');
    const centerX = window.innerWidth / 2;
    const centerY = window.innerHeight / 2;
    
    // Crear anillo de pulso
    const pulseRing = document.createElement('div');
    pulseRing.className = 'pulse-ring';
    pulseRing.style.left = centerX + 'px';
    pulseRing.style.top = centerY + 'px';
    pulseRing.style.width = '50px';
    pulseRing.style.height = '50px';
    pulseRing.style.border = '3px solid #FFD93D';
    pulseRing.style.borderRadius = '50%';
    container.appendChild(pulseRing);
    
    // Crear confeti y fuegos artificiales
    for (let i = 0; i < 50; i++) {
        // Confeti
        const confetti = document.createElement('div');
        confetti.className = 'confetti';
        const colors = ['#FF6B6B', '#4ECDC4', '#FFD93D', '#667eea', '#764ba2', '#FF8E8E'];
        confetti.style.left = centerX + 'px';
        confetti.style.top = centerY + 'px';
        confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
        
        const angle = (Math.PI * 2 * i) / 50;
        const velocity = 5 + Math.random() * 10;
        const tx = Math.cos(angle) * velocity * 50;
        const ty = Math.sin(angle) * velocity * 50 - 200;
        
        confetti.style.setProperty('--tx', tx + 'px');
        confetti.style.setProperty('--ty', ty + 'px');
        
        container.appendChild(confetti);
        
        setTimeout(() => confetti.remove(), 3000);
    }
    
    // Crear fuegos artificiales adicionales
    for (let i = 0; i < 30; i++) {
        const firework = document.createElement('div');
        firework.className = 'firework';
        const colors = ['#FF6B6B', '#FFD93D', '#4ECDC4', '#667eea'];
        firework.style.left = centerX + 'px';
        firework.style.top = centerY + 'px';
        firework.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
        
        const angle = (Math.PI * 2 * i) / 30;
        const velocity = 8 + Math.random() * 12;
        const tx = Math.cos(angle) * velocity * 80;
        const ty = Math.sin(angle) * velocity * 80;
        
        firework.style.setProperty('--tx', tx + 'px');
        firework.style.setProperty('--ty', ty + 'px');
        
        container.appendChild(firework);
        
        setTimeout(() => firework.remove(), 800);
    }
    
    setTimeout(() => pulseRing.remove(), 600);
}

function showSuccessMessage(message) {
    const msg = document.createElement('div');
    msg.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: linear-gradient(135deg, #FF6B6B 0%, #FF8E8E 100%);
        color: white;
        padding: 15px 25px;
        border-radius: 10px;
        box-shadow: 0 6px 20px rgba(255, 107, 107, 0.3);
        z-index: 3000;
        animation: slideInRight 0.5s ease-out;
        font-weight: 600;
    `;
    msg.textContent = message;
    document.body.appendChild(msg);
    
    setTimeout(() => {
        msg.style.animation = 'slideOutRight 0.5s ease-in forwards';
        setTimeout(() => msg.remove(), 500);
    }, 3000);
}

function filterMovies() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const genreFilter = document.getElementById('genreFilter').value;
    const cards = document.querySelectorAll('.movie-card');
    
    cards.forEach(card => {
        const title = card.querySelector('.movie-title').textContent.toLowerCase();
        const genre = card.querySelector('.movie-genre').textContent;
        
        const matchesSearch = title.includes(searchTerm);
        const matchesGenre = !genreFilter || genre === genreFilter;
        
        if (matchesSearch && matchesGenre) {
            card.style.display = '';
            setTimeout(() => {
                card.style.animation = 'cardEnter 0.5s ease-out forwards';
            }, 10);
        } else {
            card.style.display = 'none';
        }
    });
}

function addToLibrary(movieId) {
    console.log('Añadido a biblioteca:', movieId);
    alert('Película añadida a tu biblioteca');
}

// Agregar keyframes dinámicos
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(100px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideOutRight {
        from {
            opacity: 1;
            transform: translateX(0);
        }
        to {
            opacity: 0;
            transform: translateX(100px);
        }
    }
`;
document.head.appendChild(style);
