/* leaderboard.js — Endless Mode leaderboard */
async function loadLeaderboard() {
  document.getElementById('lbLoading').style.display = 'block';
  document.getElementById('lbTableWrap').style.display = 'none';
  try {
    const res  = await fetch('/api/leaderboard');
    const data = await res.json();
    const rows = data.leaderboard || [];
    const body = document.getElementById('lbBody');
    const empty = document.getElementById('lbEmpty');
    body.innerHTML = '';
    if (rows.length === 0) {
      empty.style.display = 'block';
    } else {
      empty.style.display = 'none';
      const medals = ['🥇','🥈','🥉'];
      rows.forEach((r, i) => {
        const rank = i < 3
          ? `<span class="rank-${['gold','silver','bronze'][i]}">${medals[i]}</span>`
          : `<span style="font-weight:700;color:var(--text-lt);">#${i+1}</span>`;
        const mins = Math.floor(r.survival_time / 60);
        const secs = r.survival_time % 60;
        const time = r.survival_time > 0 ? `${mins}m ${secs}s` : '—';
        body.innerHTML += `<tr>
          <td>${rank}</td>
          <td style="font-weight:700;">${escHtml(r.player_name)}</td>
          <td style="font-weight:800;color:var(--blue);">${r.score.toLocaleString()}</td>
          <td>${r.ice_cubes > 0 ? '🧊 ' + r.ice_cubes : '—'}</td>
          <td>${time}</td>
        </tr>`;
      });
      // Update top stats
      if (rows.length > 0) {
        const el = document.getElementById('highScore');
        if (el) el.textContent = rows[0].score.toLocaleString();
        const maxTime = Math.max(...rows.map(r => r.survival_time));
        const lr = document.getElementById('longestRun');
        if (lr) lr.textContent = maxTime > 0 ? Math.floor(maxTime/60)+'m '+maxTime%60+'s' : '—';
        const maxCubes = Math.max(...rows.map(r => r.ice_cubes));
        const mc = document.getElementById('mostCubes');
        if (mc) mc.textContent = maxCubes > 0 ? maxCubes : '—';
      }
    }
    document.getElementById('lbLoading').style.display = 'none';
    document.getElementById('lbTableWrap').style.display = 'block';
  } catch (e) {
    document.getElementById('lbLoading').textContent = 'Could not load leaderboard. Make sure the server is running.';
  }
}

async function submitScore() {
  const name  = document.getElementById('lbName').value.trim();
  const score = document.getElementById('lbScore').value;
  const cubes = document.getElementById('lbCubes').value || 0;
  const time  = document.getElementById('lbTime').value || 0;
  const msg   = document.getElementById('lbMsg');
  msg.className = 'form-msg';
  if (!name || !score) {
    msg.textContent = 'Please enter your name and score.';
    msg.className = 'form-msg error';
    return;
  }
  try {
    const res  = await fetch('/api/leaderboard', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ player_name: name, score: parseInt(score), ice_cubes: parseInt(cubes), survival_time: parseInt(time) })
    });
    const data = await res.json();
    if (data.success) {
      msg.textContent = '🏆 Score submitted! Great run!';
      msg.className = 'form-msg success';
      document.getElementById('lbName').value = '';
      document.getElementById('lbScore').value = '';
      document.getElementById('lbCubes').value = '';
      document.getElementById('lbTime').value = '';
      loadLeaderboard();
    } else {
      msg.textContent = data.error || 'Something went wrong.';
      msg.className = 'form-msg error';
    }
  } catch (e) {
    msg.textContent = 'Server not reachable. Is the server running?';
    msg.className = 'form-msg error';
  }
}

function escHtml(str) {
  return String(str).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

// Auto-load on page ready
document.addEventListener('DOMContentLoaded', loadLeaderboard);
