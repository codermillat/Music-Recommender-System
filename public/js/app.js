// API endpoints
const API_BASE = '/api';

// Get popular recommendations
async function getPopularRecommendations() {
    try {
        const response = await fetch(`${API_BASE}/recommendations/popular`);
        const data = await response.json();
        displayRecommendations('popularSongs', data);
    } catch (error) {
        showError('popularSongs', 'Failed to load recommendations');
    }
}

// Get collaborative filtering recommendations
async function getCollaborativeRecommendations() {
    const userId = document.getElementById('userId').value;
    if (!userId) {
        showError('collaborativeRecs', 'Please enter a user ID');
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/recommendations/collaborative/${userId}`);
        const data = await response.json();
        displayRecommendations('collaborativeRecs', data);
    } catch (error) {
        showError('collaborativeRecs', 'Failed to load recommendations');
    }
}

// Get content-based recommendations
async function getContentBasedRecommendations() {
    const songId = document.getElementById('songId').value;
    if (!songId) {
        showError('contentRecs', 'Please enter a song ID');
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/recommendations/content/${songId}`);
        const data = await response.json();
        displayRecommendations('contentRecs', data);
    } catch (error) {
        showError('contentRecs', 'Failed to load recommendations');
    }
}

// Display recommendations in the UI
function displayRecommendations(elementId, recommendations) {
    const container = document.getElementById(elementId);
    container.innerHTML = '';

    recommendations.forEach(rec => {
        const div = document.createElement('div');
        div.className = 'p-4 bg-gray-50 rounded';
        div.innerHTML = `
            <p class="font-semibold">${escapeHtml(rec.song)}</p>
            <p class="text-sm text-gray-600">${escapeHtml(rec.artist)}</p>
            ${rec.plays ? `<p class="text-xs text-gray-500">${rec.plays.toLocaleString()} plays</p>` : ''}
        `;
        container.appendChild(div);
    });
}

// Helper functions
function showError(elementId, message) {
    const container = document.getElementById(elementId);
    container.innerHTML = `
        <div class="p-4 bg-red-50 text-red-700 rounded">
            ${escapeHtml(message)}
        </div>
    `;
}

function escapeHtml(unsafe) {
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    getPopularRecommendations();
});