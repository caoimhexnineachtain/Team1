'use strict';
const express = require('express');
const cors    = require('cors');
const path    = require('path');
const Database = require('better-sqlite3');

const app  = express();
const PORT = process.env.PORT || 3000;

// ── Middleware ────────────────────────────────────────────────
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Serve frontend static files
app.use(express.static(path.join(__dirname, '..', 'frontend')));

// ── Database setup ────────────────────────────────────────────
const dbPath = path.join(__dirname, '..', 'database', 'snowplace.db');
const db = new Database(dbPath);

db.exec(`
  CREATE TABLE IF NOT EXISTS contact_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    subject TEXT NOT NULL,
    message TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
  );

  CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    rating INTEGER NOT NULL CHECK(rating BETWEEN 1 AND 5),
    review TEXT NOT NULL,
    favourite_level TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
  );

  CREATE TABLE IF NOT EXISTS leaderboard (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_name TEXT NOT NULL,
    score INTEGER NOT NULL,
    ice_cubes INTEGER NOT NULL DEFAULT 0,
    survival_time INTEGER NOT NULL DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
  );
`);

// ── Helpers ───────────────────────────────────────────────────
function sanitize(str) {
  return String(str || '').trim().slice(0, 2000);
}
function isValidEmail(e) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(e);
}

// ── CONTACT routes ────────────────────────────────────────────
app.post('/api/contact', (req, res) => {
  const { name, email, subject, message } = req.body;
  if (!name || !email || !subject || !message) {
    return res.status(400).json({ error: 'All fields are required.' });
  }
  if (!isValidEmail(email)) {
    return res.status(400).json({ error: 'Please enter a valid email address.' });
  }
  const stmt = db.prepare(
    'INSERT INTO contact_messages (name, email, subject, message) VALUES (?, ?, ?, ?)'
  );
  stmt.run(sanitize(name), sanitize(email), sanitize(subject), sanitize(message));
  res.json({ success: true, message: "Thanks! Your message has been sent." });
});

// ── REVIEWS routes ─────────────────────────────────────────────
app.get('/api/reviews', (req, res) => {
  const rows = db.prepare(
    'SELECT * FROM reviews ORDER BY created_at DESC LIMIT 50'
  ).all();
  const avg = db.prepare('SELECT AVG(rating) as avg, COUNT(*) as total FROM reviews').get();
  res.json({
    reviews: rows,
    average: avg.avg ? parseFloat(avg.avg).toFixed(1) : null,
    total: avg.total
  });
});

app.post('/api/reviews', (req, res) => {
  const { name, rating, review, favourite_level } = req.body;
  if (!name || !rating || !review) {
    return res.status(400).json({ error: 'Name, rating and review are required.' });
  }
  const r = parseInt(rating);
  if (isNaN(r) || r < 1 || r > 5) {
    return res.status(400).json({ error: 'Rating must be between 1 and 5.' });
  }
  const stmt = db.prepare(
    'INSERT INTO reviews (name, rating, review, favourite_level) VALUES (?, ?, ?, ?)'
  );
  stmt.run(sanitize(name), r, sanitize(review), sanitize(favourite_level || ''));
  res.json({ success: true, message: 'Review submitted! Thank you.' });
});

// ── LEADERBOARD routes ─────────────────────────────────────────
app.get('/api/leaderboard', (req, res) => {
  const rows = db.prepare(
    'SELECT * FROM leaderboard ORDER BY score DESC LIMIT 20'
  ).all();
  res.json({ leaderboard: rows });
});

app.post('/api/leaderboard', (req, res) => {
  const { player_name, score, ice_cubes, survival_time } = req.body;
  if (!player_name || score === undefined) {
    return res.status(400).json({ error: 'player_name and score are required.' });
  }
  db.prepare(
    'INSERT INTO leaderboard (player_name, score, ice_cubes, survival_time) VALUES (?, ?, ?, ?)'
  ).run(sanitize(player_name), parseInt(score), parseInt(ice_cubes) || 0, parseInt(survival_time) || 0);
  res.json({ success: true });
});

// ── Catch-all: serve index.html ────────────────────────────────
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, '..', 'frontend', 'index.html'));
});

app.listen(PORT, () => {
  console.log(`🐧 Snow Place Like Home server running at http://localhost:${PORT}`);
});
