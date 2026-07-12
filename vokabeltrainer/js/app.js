// ─────────────────────────────────────────────────────────────────────────────
// WORTSCHATZ – wird zur Laufzeit aus den JSON-Dateien geladen
// (data/vocabulary.json = Nomen/Verben/Adjektive/Phrasen, data/konjugation.json = Konjugationstabellen)
// ─────────────────────────────────────────────────────────────────────────────
let ALL_WORDS = [];

async function loadWords() {
  const [vocabRes, konjRes] = await Promise.all([
    fetch('data/vocabulary.json'),
    fetch('data/konjugation.json')
  ]);
  if (!vocabRes.ok || !konjRes.ok) {
    throw new Error('Konnte Vokabeldaten nicht laden');
  }
  const vocabulary = await vocabRes.json();
  const konjugation = await konjRes.json();
  ALL_WORDS = [...vocabulary, ...konjugation];
}


// ─────────────────────────────────────────────────────────────────────────────
// STATE
// ─────────────────────────────────────────────────────────────────────────────
let mode = 'tippen';
let category = 'all';
let deck = [];
let idx = 0;
let totalAnswered = 0, totalCorrect = 0, streak = 0;
let answered = false;

function filteredDeck() {
  let words = category === 'all' ? [...ALL_WORDS] : ALL_WORDS.filter(w => w.cat === category);
  // shuffle
  for (let i = words.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i+1));
    [words[i], words[j]] = [words[j], words[i]];
  }
  return words;
}

function setMode(m) {
  mode = m;
  document.querySelectorAll('.mode-btn').forEach(b => b.classList.remove('active'));
  event.target.classList.add('active');
  restart();
}

function filterCategory(c) {
  category = c;
  restart();
}

function restart() {
  deck = filteredDeck();
  idx = 0;
  answered = false;
  showCard();
}

function showCard() {
  if (idx >= deck.length) { showResult(); return; }
  const w = deck[idx];
  answered = false;

  const isReverse = mode === 'reverse';
  const question = isReverse ? w.de : w.it;
  const qLang = isReverse ? 'Deutsch → Italiano' : 'Italiano → Deutsch';

  document.getElementById('cat-tag').textContent = w.cat;
  document.getElementById('card-num').textContent = `${idx+1} / ${deck.length}`;
  document.getElementById('q-lang').textContent = qLang;
  document.getElementById('question').innerHTML = question.replace(/(\*.*?\*)/g, '<em>$1</em>');
  document.getElementById('hint').textContent = w.hint || '';
  document.getElementById('progress').style.width = `${(idx/deck.length)*100}%`;

  // hide feedback
  const fb1 = document.getElementById('feedback');
  const fb2 = document.getElementById('feedback2');
  fb1.className = 'feedback';
  fb2.className = 'feedback';

  if (mode === 'multiple') {
    document.getElementById('answer-area').style.display = 'none';
    document.getElementById('choice-area').style.display = 'flex';
    document.getElementById('next-btn').style.display = 'none';
    buildChoices(w, isReverse);
  } else {
    document.getElementById('answer-area').style.display = 'flex';
    document.getElementById('choice-area').style.display = 'none';
    const inp = document.getElementById('answer-input');
    inp.value = '';
    inp.className = 'answer-input';
    inp.disabled = false;
    inp.focus();
    document.getElementById('main-btn').textContent = 'Prüfen →';
  }
}

function buildChoices(current, isReverse) {
  const correctAns = isReverse ? current.it : current.de;
  const pool = ALL_WORDS.filter(w => w !== current && w.cat === current.cat);
  for (let i = pool.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i+1));
    [pool[i], pool[j]] = [pool[j], pool[i]];
  }
  const distractors = pool.slice(0, 3).map(w => isReverse ? w.it : w.de);
  const options = [correctAns, ...distractors].sort(() => Math.random()-0.5);

  const container = document.getElementById('choices');
  container.innerHTML = '';
  options.forEach(opt => {
    const btn = document.createElement('button');
    btn.className = 'choice-btn';
    btn.textContent = opt;
    btn.onclick = () => checkChoice(btn, opt, correctAns);
    container.appendChild(btn);
  });
}

function checkChoice(btn, chosen, correct) {
  if (answered) return;
  answered = true;
  totalAnswered++;

  const allBtns = document.querySelectorAll('.choice-btn');
  allBtns.forEach(b => {
    b.disabled = true;
    if (b.textContent === correct) b.classList.add('correct');
  });

  const fb = document.getElementById('feedback2');
  if (chosen === correct) {
    totalCorrect++;
    streak++;
    btn.classList.add('correct');
    fb.className = 'feedback correct';
    fb.textContent = '✓ Richtig!';
  } else {
    streak = 0;
    btn.classList.add('wrong');
    fb.className = 'feedback wrong';
    fb.innerHTML = `✗ Falsch — richtig: <span class="correct-ans">${correct}</span>`;
  }
  updateStats();
  document.getElementById('next-btn').style.display = 'block';
}

function handleMain() {
  if (answered) { nextCard(); return; }
  checkInput();
}

function handleKey(e) {
  if (e.key !== 'Enter') return;

  const mainBtn = document.getElementById('main-btn');
  const nextBtn = document.getElementById('next-btn');

  // Multiple Choice → eigener Next-Button
  if (nextBtn && nextBtn.style.display !== 'none') {
    nextCard();
    return;
  }

  // Tippen-Modus → Button-Text entscheidet
  if (mainBtn && mainBtn.textContent.includes('Weiter')) {
    nextCard();
  } else {
    handleMain();
  }
}

function checkInput() {
  const inp = document.getElementById('answer-input');
  const fb = document.getElementById('feedback');
  const w = deck[idx];
  const isReverse = mode === 'reverse';
  const correctRaw = isReverse ? w.it : w.de;

  const normalize = s => s.toLowerCase().trim().replace(/\s+/g, ' ');
  const userAns = normalize(inp.value);
  const correct = normalize(correctRaw);

  // Alternativen (z. B. "der Neffe / Enkel")
  const alternatives = correct.split('/').map(s => s.trim());

  // ✅ FIX: leere Eingabe ist IMMER falsch
  let isCorrect = false;

  if (userAns.length > 0) {
    isCorrect =
      alternatives.some(alt => userAns === alt) ||
      alternatives.some(alt => userAns.length > 3 && alt.includes(userAns));
  }

  // Stats & Zustand
  totalAnswered++;
  answered = true;

  if (isCorrect) {
    totalCorrect++;
    streak++;

    inp.className = 'answer-input correct';
    fb.className = 'feedback correct';
    fb.textContent = '✓ Richtig!';
  } else {
    streak = 0;

    inp.className = 'answer-input wrong';
    inp.classList.add('shake');
    setTimeout(() => inp.classList.remove('shake'), 400);

    fb.className = 'feedback wrong';
    fb.innerHTML = `✗ Falsch — richtig: <span class="correct-ans">${correctRaw}</span>`;
  }

  // UI-Update
  inp.disabled = true;

  const mainBtn = document.getElementById('main-btn');
  if (mainBtn) mainBtn.textContent = 'Weiter →';

  const nextBtn = document.getElementById('next-btn');
  if (nextBtn) nextBtn.textContent = 'Weiter →';

  updateStats();
}

function nextCard() {
  idx++;
  answered = false;
  showCard();
}

function skipCard() {
  streak = 0;
  idx++;
  answered = false;
  showCard();
}

function updateStats() {
  document.getElementById('stat-total').textContent = totalAnswered;
  document.getElementById('stat-correct').textContent = totalCorrect;
  const pct = totalAnswered > 0 ? Math.round((totalCorrect/totalAnswered)*100) + '%' : '—';
  document.getElementById('stat-pct').textContent = pct;
  document.getElementById('stat-streak').textContent = streak;
}

function showResult() {
  document.querySelector('.card-wrap').style.display = 'none';
  document.getElementById('answer-area').style.display = 'none';
  document.getElementById('choice-area').style.display = 'none';
  document.getElementById('progress').style.width = '100%';

  const pct = totalAnswered > 0 ? Math.round((totalCorrect/totalAnswered)*100) : 0;
  const screen = document.getElementById('result-screen');
  screen.style.display = 'block';
  document.getElementById('score-circle').textContent = pct + '%';
  let msg = pct >= 90 ? 'Eccellente! Ottimo lavoro! 🎉' :
            pct >= 70 ? 'Molto bene! Continua così!' :
            pct >= 50 ? 'Bene! Ancora un po\' di pratica.' :
            'Riprova! Non mollare! 💪';
  document.getElementById('result-text').textContent = `${totalCorrect} von ${totalAnswered} richtig · ${msg}`;
}

function insertChar(c) {
  const inp = document.getElementById('answer-input');
  const pos = inp.selectionStart;
  inp.value = inp.value.slice(0,pos) + c + inp.value.slice(inp.selectionEnd);
  inp.selectionStart = inp.selectionEnd = pos + 1;
  inp.focus();
}

// Enter-Taste global (funktioniert auch wenn Input disabled ist)
document.addEventListener('keydown', handleKey);

// init – zuerst Daten laden, dann erste Karte anzeigen
loadWords()
  .then(restart)
  .catch(err => {
    console.error(err);
    document.getElementById('question').textContent = 'Fehler beim Laden der Vokabeln.';
  });
