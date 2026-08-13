# There's Snow Place Like Home — Website

## Quick Start

### Requirements
- Node.js (v16+) installed: https://nodejs.org

### Run the website
1. Double-click **START.bat**  (Windows)
   OR open a terminal in this folder and run:
   ```
   cd backend
   npm install
   node server.js
   ```
2. Open your browser at **http://localhost:3000**

### Project Structure
```
snowplace/
  frontend/          ← All HTML, CSS, JS files
    css/style.css
    js/main.js
    index.html, game.html, levels.html ...
  backend/
    server.js        ← Express API server
    package.json
  database/
    snowplace.db     ← SQLite database (auto-created on first run)
  START.bat          ← One-click launcher (Windows)
```

### API Endpoints
| Method | URL | Description |
|--------|-----|-------------|
| POST | /api/contact | Submit a contact message |
| GET  | /api/reviews | Fetch all reviews |
| POST | /api/reviews | Submit a review |
| GET  | /api/leaderboard | Fetch leaderboard |
| POST | /api/leaderboard | Submit a leaderboard score |
