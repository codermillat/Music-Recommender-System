const express = require('express');
const { PythonShell } = require('python-shell');
const cors = require('cors');
const path = require('path');

const app = express();
const port = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());
app.use(express.static('public'));

// Error handling middleware
const asyncHandler = fn => (req, res, next) => {
    Promise.resolve(fn(req, res, next)).catch(next);
};

// Get chart data
app.get('/api/charts/data', asyncHandler(async (req, res) => {
    const options = {
        mode: 'json',
        pythonPath: 'python3',
        scriptPath: './',
        args: ['--type', 'charts']
    };

    const results = await PythonShell.run('main.py', options);
    if (!results || !results[0]) {
        throw new Error('No chart data available');
    }
    res.json(results[0]);
}));

// Get popular recommendations
app.get('/api/recommendations/popular', asyncHandler(async (req, res) => {
    const options = {
        mode: 'json',
        pythonPath: 'python3',
        scriptPath: './',
        args: ['--type', 'popular']
    };

    const results = await PythonShell.run('main.py', options);
    if (!results || !results[0]) {
        throw new Error('No recommendations available');
    }
    res.json(results[0]);
}));

// Get collaborative recommendations
app.get('/api/recommendations/collaborative/:userId', asyncHandler(async (req, res) => {
    const options = {
        mode: 'json',
        pythonPath: 'python3',
        scriptPath: './',
        args: ['--type', 'collaborative', '--user', req.params.userId]
    };

    const results = await PythonShell.run('main.py', options);
    if (!results || !results[0]) {
        throw new Error('No recommendations available');
    }
    res.json(results[0]);
}));

// Get content-based recommendations
app.get('/api/recommendations/content/:songId', asyncHandler(async (req, res) => {
    const options = {
        mode: 'json',
        pythonPath: 'python3',
        scriptPath: './',
        args: ['--type', 'content', '--song', req.params.songId]
    };

    const results = await PythonShell.run('main.py', options);
    if (!results || !results[0]) {
        throw new Error('No recommendations available');
    }
    res.json(results[0]);
}));

// Error handling
app.use((err, req, res, next) => {
    console.error(err);
    res.status(500).json({
        error: err.message || 'Internal server error',
        status: 500
    });
});

// Serve index.html for all other routes
app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Start server
app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});