/* =========================================
   1. CUSTOM CURSOR LOGIC
   ========================================= */
const cur = document.getElementById('cur');
const ring = document.getElementById('cur-ring');

let mx = 0, my = 0, rx = 0, ry = 0;

document.addEventListener('mousemove', e => {
  mx = e.clientX;
  my = e.clientY;
  cur.style.left = mx + 'px';
  cur.style.top = my + 'px';
});

document.addEventListener('mousedown', () => document.body.classList.add('click'));
document.addEventListener('mouseup', () => document.body.classList.remove('click'));

(function loop() {
  rx += (mx - rx) * 0.1;
  ry += (my - ry) * 0.1;
  
  const ringParent = document.getElementById('cur-ring').parentElement;
  ringParent.style.left = rx + 'px';
  ringParent.style.top = ry + 'px';
  
  requestAnimationFrame(loop);
})();

let rrx = 0, rry = 0;
(function rloop() {
  rrx += (mx - rrx) * 0.07;
  rry += (my - rry) * 0.07;
  
  ring.style.transform = `translate(calc(-50% + ${rrx - mx}px), calc(-50% + ${rry - my}px))`;
  
  requestAnimationFrame(rloop);
})();

document.querySelectorAll('a, button, .fcard, .tcard, input, textarea').forEach(el => {
  el.addEventListener('mouseenter', () => document.body.classList.add('hov'));
  el.addEventListener('mouseleave', () => document.body.classList.remove('hov'));
});


/* =========================================
   2. MOBILE MENU & NAVBAR SCROLL
   ========================================= */
const ham = document.getElementById('ham');
const mm = document.getElementById('mm');

ham.addEventListener('click', () => {
  ham.classList.toggle('open');
  mm.classList.toggle('open');
});

function closeMM() {
  ham.classList.remove('open');
  mm.classList.remove('open');
}

window.addEventListener('scroll', () => {
  document.getElementById('nav').classList.toggle('sc', window.scrollY > 40);
});


/* =========================================
   3. DYNAMIC CONTENT GENERATION
   ========================================= */

// Hero Title Animation
const words = [
  { t: 'Modern Websites', a: false }, 
  { t: 'Built for', a: false }, 
  { t: 'Real Businesses.', a: true }
];
const ht = document.getElementById('ht');

words.forEach((w, i) => {
  const s = document.createElement('span');
  s.className = 'word' + (w.a ? ' acc' : '');
  s.textContent = (i < words.length - 1 ? w.t + ' ' : w.t);
  s.style.animationDelay = (0.36 + i * 0.18) + 's';
  ht.appendChild(s);
});

// Inject Services Data
const svcs = [
  { i: '🌐', t: 'Business Websites', d: 'Modern, mobile-friendly websites designed to represent your brand and convert visitors into customers.' },
  { i: '🎯', t: 'Landing Pages', d: 'Focused landing pages built to support marketing campaigns and increase conversions for your business.' },
  { i: '📊', t: 'Admin Dashboards', d: 'Clean dashboards that give businesses real-time insights and control over their operations.' },
  { i: '🧩', t: 'Custom Web Platforms', d: 'Tailored web applications designed around your specific workflows and unique business needs.' }
];
const fg = document.getElementById('fg');

svcs.forEach((s, i) => {
  const d = document.createElement('div');
  d.className = 'fcard';
  d.style.transitionDelay = (i * 0.1) + 's';
  d.innerHTML = `<div class="ficon">${s.i}</div><h3>${s.t}</h3><p>${s.d}</p>`;
  fg.appendChild(d);
});

// Inject Team Data
const team = [
  { n: 'Samrat', r: 'Frontend & UI', c: 'KLH Bachupally', l: 'S' },
  { n: 'Abhijyuth', r: 'Backend & API', c: 'Vasavi College of Engg.', l: 'A' },
  { n: 'Saaketh', r: 'Systems & Logic', c: 'CBIT', l: 'S' },
  { n: 'Shravanth', r: 'Product & Strategy', c: 'IIIT Hyderabad', l: 'S' },
  { n: 'Karthik', r: 'Developer', c: 'KLH Aziz Nagar', l: 'K' }
];
const tg = document.getElementById('tg');

team.forEach((m, i) => {
  const d = document.createElement('div');
  d.className = 'tcard';
  d.style.transitionDelay = (i * 0.08) + 's';
  d.innerHTML = `<div class="avatar">${m.l}</div><h4>${m.n}</h4><div class="role">${m.r}</div><div class="college">${m.c}</div>`;
  tg.appendChild(d);
});


/* =========================================
   4. SCROLL REVEAL & TILT EFFECTS
   ========================================= */
const obs = new IntersectionObserver(entries => {
  entries.forEach(el => {
    if (el.isIntersecting) el.target.classList.add('vis');
  });
}, { threshold: 0.1 });

document.querySelectorAll('.rv, .fcard, .tcard').forEach(el => obs.observe(el));

if (window.matchMedia('(hover: hover)').matches) {
  document.querySelectorAll('.fcard').forEach(card => {
    card.addEventListener('mousemove', e => {
      const r = card.getBoundingClientRect();
      const x = (e.clientX - r.left) / r.width - 0.5;
      const y = (e.clientY - r.top) / r.height - 0.5;
      card.style.transform = `translateY(-8px) rotateX(${-y * 7}deg) rotateY(${x * 7}deg)`;
    });
    
    card.addEventListener('mouseleave', () => {
      card.style.transform = '';
    });
  });
}