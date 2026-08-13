/* reviews.js */
let selectedRating = 0;

// Star input
document.addEventListener('DOMContentLoaded', () => {
  const stars = document.querySelectorAll('#starInput span');
  stars.forEach(s => {
    s.addEventListener('click', () => {
      selectedRating = parseInt(s.dataset.val);
      document.getElementById('ratingVal').value = selectedRating;
      document.getElementById('starErr').style.display = 'none';
      stars.forEach((x, i) => x.classList.toggle('active', i < selectedRating));
    });
    s.addEventListener('mouseenter', () => {
      const hv = parseInt(s.dataset.val);
      stars.forEach((x, i) => x.classList.toggle('active', i < hv));
    });
    s.addEventListener('mouseleave', () => {
      stars.forEach((x, i) => x.classList.toggle('active', i < selectedRating));
    });
  });
  loadReviews();
});

async function submitReview() {
  const name    = document.getElementById('rName').value.trim();
  const review  = document.getElementById('rReview').value.trim();
  const level   = document.getElementById('rLevel').value;
  const msg     = document.getElementById('reviewMsg');
  msg.className = 'form-msg';

  if (!selectedRating) {
    document.getElementById('starErr').style.display = 'block';
    return;
  }
  if (!name) { msg.textContent = 'Please enter your name.'; msg.className = 'form-msg error'; return; }
  if (!review) { msg.textContent = 'Please write a review.'; msg.className = 'form-msg error'; return; }

  try {
    const res  = await fetch('/api/reviews', {
      method: 'POST', headers: {'Content-Type':'application/json'},
      body: JSON.stringify({ name, rating: selectedRating, review, favourite_level: level })
    });
    const data = await res.json();
    if (data.success) {
      msg.textContent = '🌟 Thanks for your review!';
      msg.className   = 'form-msg success';
      document.getElementById('rName').value = '';
      document.getElementById('rReview').value = '';
      document.getElementById('rLevel').value = '';
      selectedRating = 0;
      document.querySelectorAll('#starInput span').forEach(s => s.classList.remove('active'));
      loadReviews();
    } else {
      msg.textContent = data.error || 'Something went wrong.';
      msg.className   = 'form-msg error';
    }
  } catch (e) {
    msg.textContent = 'Server not reachable. Is the server running?';
    msg.className   = 'form-msg error';
  }
}

async function loadReviews() {
  document.getElementById('reviewsLoading').style.display = 'block';
  document.getElementById('reviewsList').style.display    = 'none';
  document.getElementById('reviewsEmpty').style.display   = 'none';
  try {
    const res  = await fetch('/api/reviews');
    const data = await res.json();
    // Update average
    if (data.average) {
      document.getElementById('avgNum').textContent  = data.average + ' / 5';
      document.getElementById('avgStars').textContent = starsStr(Math.round(data.average));
      document.getElementById('avgSub').textContent  = `Based on ${data.total} review${data.total===1?'':'s'}`;
    } else {
      document.getElementById('avgNum').textContent  = '—';
      document.getElementById('avgStars').textContent = '☆☆☆☆☆';
      document.getElementById('avgSub').textContent  = 'No reviews yet — be the first!';
    }
    const list = document.getElementById('reviewsList');
    list.innerHTML = '';
    if (!data.reviews || data.reviews.length === 0) {
      document.getElementById('reviewsEmpty').style.display = 'block';
    } else {
      data.reviews.forEach(r => {
        const d = new Date(r.created_at).toLocaleDateString('en-GB', {day:'numeric',month:'long',year:'numeric'});
        list.innerHTML += `
          <div class="review-card">
            <div class="rc-top">
              <span class="rc-name">${escHtml(r.name)}</span>
              <span class="rc-stars">${starsStr(r.rating)}</span>
              ${r.favourite_level ? `<span class="rc-level">❤️ ${escHtml(r.favourite_level)}</span>` : ''}
            </div>
            <p>${escHtml(r.review)}</p>
            <div class="rc-date">${d}</div>
          </div>`;
      });
      list.style.display = 'grid';
    }
    document.getElementById('reviewsLoading').style.display = 'none';
  } catch (e) {
    document.getElementById('reviewsLoading').textContent = 'Could not load reviews. Is the server running?';
  }
}

function starsStr(n) {
  return '★'.repeat(Math.max(0,Math.min(5,n))) + '☆'.repeat(Math.max(0,5-n));
}
function escHtml(s) {
  return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}
