import express from 'express';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import cors from 'cors';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const app = express();
const port = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());
app.use(express.static('public'));

// Routes for recommendations
app.get('/api/recommendations/popular', (req, res) => {
    const recommendations = [
        { artist: "The Beatles", song: "Hey Jude", plays: 1000000 },
        { artist: "Queen", song: "Bohemian Rhapsody", plays: 950000 },
        { artist: "Led Zeppelin", song: "Stairway to Heaven", plays: 900000 }
    ];
    res.json(recommendations);
});

app.get('/api/recommendations/collaborative/:userId', (req, res) => {
    const userId = req.params.userId;
    const recommendations = [
        { artist: "Pink Floyd", song: "Wish You Were Here" },
        { artist: "The Rolling Stones", song: "Paint It Black" },
        { artist: "The Who", song: "Baba O'Riley" }
    ];
    res.json(recommendations);
});

app.get('/api/recommendations/content/:songId', (req, res) => {
    const songId = req.params.songId;
    const recommendations = [
        { artist: "David Bowie", song: "Space Oddity" },
        { artist: "Elton John", song: "Rocket Man" },
        { artist: "Black Sabbath", song: "Paranoid" }
    ];
    res.json(recommendations);
});

// Serve index.html for all other routes
app.get('*', (req, res) => {
    res.sendFile(join(__dirname, 'public', 'index.html'));
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});