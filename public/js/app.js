// API endpoints
const API_BASE = 'http://localhost:3000/api';

// Initialize charts with real data
async function initCharts() {
    try {
        const response = await fetch(`${API_BASE}/charts/data`);
        const chartData = await response.json();
        
        // Top Artists Chart
        const artistData = {
            x: chartData.artists.map(a => a.name),
            y: chartData.artists.map(a => a.count),
            type: 'bar',
            orientation: 'h'
        };
        
        Plotly.newPlot('topArtistsChart', [artistData], {
            title: 'Most Popular Artists',
            margin: { t: 30 }
        });

        // Listening Patterns Chart
        const patternData = {
            x: chartData.patterns.plays,
            type: 'histogram',
            nbinsx: 50
        };
        
        Plotly.newPlot('listeningPatternsChart', [patternData], {
            title: 'Distribution of Play Counts',
            margin: { t: 30 }
        });
    } catch (error) {
        console.error('Failed to load chart data:', error);
        showError('charts', 'Failed to load chart data. Please try again later.');
    }
}

// Get popular recommendations
async function getPopularRecommendations() {
    try {
        showLoading('popularSongs');
        const response = await fetch(`${API_BASE}/recommendations/popular`);
        if (!response.ok) throw new Error('Failed to fetch popular recommendations');
        
        const data = await response.json();
        if (!data || !Array.isArray(data)) throw new Error('Invalid data format');
        
        displayRecommendations('popularSongs', data);
    } catch (error) {
        console.error('Error:', error);
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
        showLoading('collaborativeRecs');
        const response = await fetch(`${API_BASE}/recommendations/collaborative/${encodeURIComponent(userId)}`);
        if (!response.ok) throw new Error('Failed to fetch collaborative recommendations');
        
        const data = await response.json();
        if (!data || !Array.isArray(data)) throw new Error('Invalid data format');
        
        displayRecommendations('collaborativeRecs', data);
    } catch (error) {
        console.error('Error:', error);
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
        showLoading('contentRecs');
        const response = await fetch(`${API_BASE}/recommendations/content/${encodeURIComponent(songId)}`);
        if (!response.ok) throw new Error('Failed to fetch content-based recommendations');
        
        const data = await response.json();
        if (!data || !Array.isArray(data)) throw new Error('Invalid data format');
        
        displayRecommendations('contentRecs', data);
    } catch (error) {
        console.error('Error:', error);
        showError('contentRecs', 'Failed to load recommendations');
    }
}

// Display recommendations in the UI
function displayRecommendations(elementId, recommendations) {
    const container = document.getElementById(elementId);
    if (!container) return;
    
    container.innerHTML = '';

    if (recommendations.length === 0) {
        showMessage(elementId, 'No recommendations found');
        return;
    }

    recommendations.forEach(rec => {
        const div = document.createElement('div');
        div.className = 'p-4 bg-gray-50 rounded';
        div.innerHTML = `
            <p class="font-semibold">${escapeHtml(rec.title || 'Unknown Title')}</p>
            <p class="text-sm text-gray-600">${escapeHtml(rec.artist || 'Unknown Artist')}</p>
        `;
        container.appendChild(div);
    });
}

// Helper functions
function showLoading(elementId) {
    const container = document.getElementById(elementId);
    if (container) {
        container.innerHTML = '<div class="flex justify-center"><div class="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900"></div></div>';
    }
}

function showError(elementId, message) {
    const container = document.getElementById(elementId);
    if (container) {
        container.innerHTML = `<div class="p-4 bg-red-50 text-red-700 rounded">${escapeHtml(message)}</div>`;
    }
}

function showMessage(elementId, message) {
    const container = document.getElementById(elementId);
    if (container) {
        container.innerHTML = `<div class="p-4 bg-gray-50 text-gray-700 rounded">${escapeHtml(message)}</div>`;
    }
}

function escapeHtml(unsafe) {
    if (typeof unsafe !== 'string') return '';
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    initCharts().catch(console.error);
    getPopularRecommendations().catch(console.error);
});