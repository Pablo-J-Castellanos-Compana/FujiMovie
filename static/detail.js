const API_BASE = '/api/movies';
let currentMovieId = null;

// Obtener ID de película de la URL al cargar
document.addEventListener('DOMContentLoaded', () => {
    const params = new URLSearchParams(window.location.search);
    currentMovieId = params.get('id');
    
    if (currentMovieId) {
        loadMovieDetail(currentMovieId);
    } else {
        window.location.href = '/';
    }
});

async function loadMovieDetail(movieId) {
    try {
        const response = await fetch(`${API_BASE}/${movieId}`);
        const movie = await response.json();
        
        if (movie.error) {
            document.getElementById('loadingBtn').textContent = 'Película no encontrada';
            return;
        }
        
        displayMovieDetail(movie);
        loadRatings(movieId);
    } catch (error) {
        console.error('Error loading movie:', error);
        document.getElementById('loadingBtn').textContent = 'Error al cargar la película';
    }
}

function displayMovieDetail(movie) {
    document.getElementById('loadingBtn').style.display = 'none';
    document.getElementById('movieDetail').classList.remove('hidden');
    
    document.getElementById('detailTitle').textContent = movie.title;
    document.getElementById('detailYear').textContent = `Año: ${movie.year}`;
    document.getElementById('detailGenre').textContent = movie.genre;
    document.getElementById('detailDescription').textContent = movie.description || 'Sin descripción disponible';
    document.getElementById('avgRating').textContent = `${movie.stars || 0} ⭐`;
}

async function loadRatings(movieId) {
    try {
        const response = await fetch(`${API_BASE}/${movieId}/ratings`);
        const data = await response.json();
        
        document.getElementById('totalRatings').textContent = data.count;
        document.getElementById('avgRating').textContent = `${data.average} ⭐`;
        
        const ratingsList = document.getElementById('ratingsList');
        ratingsList.innerHTML = '';
        
        if (data.ratings && data.ratings.length > 0) {
            data.ratings.forEach((rating, index) => {
                const ratingItem = document.createElement('div');
                ratingItem.className = 'rating-item';
                ratingItem.style.animationDelay = `${index * 0.1}s`;
                ratingItem.innerHTML = `
                    <div class="rating-item-header">
                        <span class="rating-user">${rating.user}</span>
                        <span class="rating-score">${'⭐'.repeat(Math.round(rating.score))} (${rating.score})</span>
                    </div>
                `;
                ratingsList.appendChild(ratingItem);
            });
        } else {
            ratingsList.innerHTML = '<p class="empty-ratings">Sin valoraciones aún</p>';
        }
    } catch (error) {
        console.error('Error loading ratings:', error);
    }
}

async function submitDetailRating() {
    const score = document.querySelector('.star-rating-large input:checked')?.value;
    const user = document.getElementById('detailUserName').value.trim();
    
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
            createDetailExplosion();
            document.getElementById('detailUserName').value = '';
            document.querySelectorAll('.star-rating-large input').forEach(input => input.checked = false);
            loadRatings(currentMovieId);
            showDetailSuccessMessage(`¡${user} valoró la película con ${score} ⭐!`);
        } else {
            alert('Error al valorar la película');
        }
    } catch (error) {
        console.error('Error submitting rating:', error);
        alert('Error al enviar la valoración');
    }
}

function createDetailExplosion() {
    const container = document.getElementById('explosionContainer');
    const centerX = window.innerWidth / 2;
    const centerY = window.innerHeight / 2;
    
    // Anillo de pulso
    const pulseRing = document.createElement('div');
    pulseRing.className = 'pulse-ring';
    pulseRing.style.left = centerX + 'px';
    pulseRing.style.top = centerY + 'px';
    pulseRing.style.width = '60px';
    pulseRing.style.height = '60px';
    pulseRing.style.border = '4px solid #FFD93D';
    pulseRing.style.borderRadius = '50%';
    container.appendChild(pulseRing);
    
    // Confeti
    for (let i = 0; i < 60; i++) {
        const confetti = document.createElement('div');
        confetti.className = 'confetti';
        const colors = ['#FF6B6B', '#4ECDC4', '#FFD93D', '#667eea', '#764ba2', '#FF8E8E'];
        confetti.style.left = centerX + 'px';
        confetti.style.top = centerY + 'px';
        confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
        
        const angle = (Math.PI * 2 * i) / 60;
        const velocity = 6 + Math.random() * 12;
        const tx = Math.cos(angle) * velocity * 60;
        const ty = Math.sin(angle) * velocity * 60 - 250;
        
        confetti.style.setProperty('--tx', tx + 'px');
        confetti.style.setProperty('--ty', ty + 'px');
        
        container.appendChild(confetti);
        
        setTimeout(() => confetti.remove(), 3000);
    }
    
    // Fuegos artificiales
    for (let i = 0; i < 40; i++) {
        const firework = document.createElement('div');
        firework.className = 'firework';
        const colors = ['#FF6B6B', '#FFD93D', '#4ECDC4', '#667eea'];
        firework.style.left = centerX + 'px';
        firework.style.top = centerY + 'px';
        firework.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
        
        const angle = (Math.PI * 2 * i) / 40;
        const velocity = 10 + Math.random() * 14;
        const tx = Math.cos(angle) * velocity * 100;
        const ty = Math.sin(angle) * velocity * 100;
        
        firework.style.setProperty('--tx', tx + 'px');
        firework.style.setProperty('--ty', ty + 'px');
        
        container.appendChild(firework);
        
        setTimeout(() => firework.remove(), 800);
    }
    
    setTimeout(() => pulseRing.remove(), 600);
}

function showDetailSuccessMessage(message) {
    const msg = document.createElement('div');
    msg.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: linear-gradient(135deg, #FF6B6B 0%, #FF8E8E 100%);
        color: white;
        padding: 16px 28px;
        border-radius: 10px;
        box-shadow: 0 8px 25px rgba(255, 107, 107, 0.3);
        z-index: 3000;
        animation: slideInRight 0.5s ease-out;
        font-weight: 600;
        font-size: 1.05rem;
    `;
    msg.textContent = message;
    document.body.appendChild(msg);
    
    setTimeout(() => {
        msg.style.animation = 'slideOutRight 0.5s ease-in forwards';
        setTimeout(() => msg.remove(), 500);
    }, 3500);
}

// Agregar keyframes dinámicos si no existen
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
