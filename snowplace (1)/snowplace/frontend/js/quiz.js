/* quiz.js — 15-question interactive quiz */
const questions = [
  { q: "What is the name of the game?",
    opts: ["Penguin's Adventure","Snow Place Like Home","Arctic Runner","Ice Escape"],
    ans: 1, exp: "<strong>Snow Place Like Home</strong> — a penguin adventure game about making it back to the Arctic." },

  { q: "Who is the main character of the game?",
    opts: ["A polar bear","A cowboy","A penguin","A seal"],
    ans: 2, exp: "The main character is a <strong>penguin</strong> who has been taken far from his Arctic home." },

  { q: "Who is the villain of the game?",
    opts: ["A farmer","A jungle explorer","A cowboy","A scientist"],
    ans: 2, exp: "The villain is a <strong>cowboy</strong> who took the penguin away from the Arctic." },

  { q: "What is Level 1's environment?",
    opts: ["Jungle","Wild West Farm","Arctic","Desert"],
    ans: 3, exp: "<strong>Level 1 is set in the Desert</strong> — the first environment the penguin must travel through." },

  { q: "What is Level 2's environment?",
    opts: ["Desert","Jungle","Farm","Arctic"],
    ans: 1, exp: "<strong>Level 2 is set in the Jungle</strong> — a denser and more dangerous environment than the desert." },

  { q: "What is Level 3's environment?",
    opts: ["Desert","Jungle","Wild West Farm","Arctic"],
    ans: 2, exp: "<strong>Level 3 is set on the Wild West Farm</strong> — the hardest level, where the cowboy is closest." },

  { q: "What are the collectables in the game called?",
    opts: ["Snowballs","Ice cubes","Crystals","Diamonds"],
    ans: 1, exp: "<strong>Ice cubes</strong> are the collectables. They remind the penguin of his Arctic home and boost your score." },

  { q: "What is the final destination the penguin is trying to reach?",
    opts: ["The farm","The jungle","The desert","The Arctic"],
    ans: 3, exp: "The penguin's goal is to reach the <strong>Arctic</strong> — his home that was stolen by the cowboy." },

  { q: "What happens when the penguin loses all health?",
    opts: ["The game pauses","The penguin slows down","It's Game Over","A new life appears"],
    ans: 2, exp: "When all health is gone, it's <strong>Game Over</strong>. You can then restart the level or return to the menu." },

  { q: "What key is used to jump in the game?",
    opts: ["Enter","Arrow Up","SPACE","J"],
    ans: 2, exp: "Press <strong>SPACE</strong> to make the penguin jump over obstacles." },

  { q: "What is Endless Mode?",
    opts: ["A mode with no obstacles","A mode where you play as the cowboy","A survival mode with no finish line","A level editor"],
    ans: 2, exp: "<strong>Endless Mode</strong> is a survival mode where obstacles keep coming indefinitely and the game gets faster over time." },

  { q: "What programming language was the game built with?",
    opts: ["JavaScript","Java","C++","Python"],
    ans: 3, exp: "The game was built using <strong>Python</strong> with the Pygame library." },

  { q: "How many levels does the main game have?",
    opts: ["1","2","3","5"],
    ans: 2, exp: "The main game has <strong>3 levels</strong> — Desert, Jungle and Wild West Farm — plus Endless Mode." },

  { q: "Which level is the hardest?",
    opts: ["Level 1 – Desert","Level 2 – Jungle","Level 3 – Wild West","They are all the same"],
    ans: 2, exp: "<strong>Level 3 – Wild West Farm</strong> is the hardest, featuring the fastest obstacles and the cowboy in pursuit." },

  { q: "How many developers created this game and website?",
    opts: ["1","2","3","4"],
    ans: 3, exp: "Snow Place Like Home was created by a team of <strong>four student developers</strong>." }
];

let qIndex = 0, qScore = 0, answered = false;
let finalScore = 0;

function startQuiz() {
  qIndex = 0; qScore = 0; answered = false;
  document.getElementById('qResult').style.display = 'none';
  document.getElementById('qCounter').parentElement.style.display = 'flex';
  ['qText','qOpts'].forEach(id => document.getElementById(id).style.display = '');
  renderQuestion();
}

function renderQuestion() {
  answered = false;
  const q = questions[qIndex];
  document.getElementById('qCounter').textContent = `Question ${qIndex+1} of ${questions.length}`;
  document.getElementById('qScoreDisplay').textContent = `Score: ${qScore}`;
  document.getElementById('qFill').style.width = `${(qIndex / questions.length) * 100}%`;
  document.getElementById('qText').textContent = q.q;
  document.getElementById('qExp').className = 'q-exp';
  document.getElementById('btnNext').style.display = 'none';

  const opts = document.getElementById('qOpts');
  opts.innerHTML = '';
  q.opts.forEach((o, i) => {
    const btn = document.createElement('button');
    btn.className = 'q-opt';
    btn.textContent = o;
    btn.addEventListener('click', () => selectAnswer(i));
    opts.appendChild(btn);
  });
}

function selectAnswer(i) {
  if (answered) return;
  answered = true;
  const q = questions[qIndex];
  const btns = document.querySelectorAll('.q-opt');
  btns.forEach(b => b.disabled = true);
  if (i === q.ans) { btns[i].classList.add('correct'); qScore++; }
  else { btns[i].classList.add('wrong'); btns[q.ans].classList.add('correct'); }
  document.getElementById('qScoreDisplay').textContent = `Score: ${qScore}`;
  const exp = document.getElementById('qExp');
  exp.innerHTML = q.exp; exp.classList.add('show');
  document.getElementById('btnNext').style.display = 'inline-flex';
}

document.getElementById('btnNext').addEventListener('click', () => {
  qIndex++;
  if (qIndex >= questions.length) showResult();
  else renderQuestion();
});

function showResult() {
  finalScore = qScore;
  document.getElementById('qFill').style.width = '100%';
  document.getElementById('qText').style.display = 'none';
  document.getElementById('qOpts').style.display = 'none';
  document.getElementById('qExp').className = 'q-exp';
  document.getElementById('btnNext').style.display = 'none';
  document.getElementById('qCounter').textContent = 'Quiz Complete!';
  document.getElementById('qScoreDisplay').textContent = `Final: ${qScore}/${questions.length}`;

  document.getElementById('resScore').textContent = `${qScore} / ${questions.length}`;
  let badge, title, sub;
  if (qScore <= 5)       { badge='🐧 Penguin Beginner!';   title='Nice try!';          sub="Keep exploring the website and try again — you'll know the answers next time!"; }
  else if (qScore <= 10) { badge='🌊 Arctic Adventurer!';  title='Good effort!';       sub="You clearly know the basics. A bit more practice and you'll ace it!"; }
  else if (qScore <= 13) { badge='🧊 Penguin Pro!';        title='Impressive!';        sub="You really know your stuff! Only the elite players score this high."; }
  else                   { badge='🏔️ HOMEWARD HERO!';      title='PERFECT (or near)!'; sub="Incredible! You know everything about Snow Place Like Home. The penguin salutes you!"; }

  document.getElementById('resBadge').textContent = badge;
  document.getElementById('resTitle').textContent = title;
  document.getElementById('resSub').textContent = sub;
  document.getElementById('qResult').style.display = 'block';
}

async function saveQuizResult() {
  const name = document.getElementById('quizName').value.trim();
  const msg  = document.getElementById('quizSaveMsg');
  if (!name) { msg.textContent = 'Please enter your name.'; return; }
  try {
    const res = await fetch('/api/quiz', {
      method: 'POST', headers: {'Content-Type':'application/json'},
      body: JSON.stringify({ player_name: name, score: finalScore, total_questions: questions.length })
    });
    const data = await res.json();
    msg.textContent = data.success ? '✅ Result saved!' : (data.error || 'Error saving.');
  } catch (e) { msg.textContent = 'Server not reachable.'; }
}

function restartQuiz() { startQuiz(); }

document.addEventListener('DOMContentLoaded', startQuiz);
