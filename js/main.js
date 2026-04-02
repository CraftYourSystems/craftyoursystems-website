/* ==============================
   AURORA CANVAS — smooth blobs
============================== */
const ac = document.getElementById('aurora'), ax = ac.getContext('2d');
let AW, AH, mxN = 0.5, myN = 0.5;

function resizeAurora() {
  AW = ac.width = ac.offsetWidth;
  AH = ac.height = ac.offsetHeight;
}
resizeAurora();
window.addEventListener('resize', resizeAurora);

document.getElementById('hero').addEventListener('mousemove', e => {
  const r = document.getElementById('hero').getBoundingClientRect();
  mxN = (e.clientX - r.left) / r.width;
  myN = (e.clientY - r.top) / r.height;
});

const blobs = [
  { bx: .25, by: .35, ax: .22, ay: .18, sx: .0008, sy: .0011, t: 0,   hue: 220, size: .52 },
  { bx: .70, by: .55, ax: .18, ay: .22, sx: .0011, sy: .0009, t: 2.1, hue: 250, size: .48 },
  { bx: .50, by: .15, ax: .20, ay: .15, sx: .0007, sy: .0013, t: 4.3, hue: 200, size: .40 },
  { bx: .15, by: .70, ax: .14, ay: .20, sx: .0013, sy: .0007, t: 1.5, hue: 270, size: .36 },
  { bx: .85, by: .25, ax: .16, ay: .18, sx: .0009, sy: .0012, t: 3.2, hue: 230, size: .32 },
];

let frame = 0;
function drawAurora() {
  frame++;
  ax.clearRect(0, 0, AW, AH);
  ax.fillStyle = '#ffffff';
  ax.fillRect(0, 0, AW, AH);

  blobs.forEach(b => {
    b.t += 1;
    const driftX = Math.sin(b.t * b.sx) * b.ax;
    const driftY = Math.cos(b.t * b.sy) * b.ay;
    const cx = (b.bx + driftX + (mxN - 0.5) * 0.12) * AW;
    const cy = (b.by + driftY + (myN - 0.5) * 0.10) * AH;
    const r = b.size * Math.min(AW, AH);
    const g = ax.createRadialGradient(cx, cy, 0, cx, cy, r);
    g.addColorStop(0,   `hsla(${b.hue},85%,68%,0.30)`);
    g.addColorStop(0.4, `hsla(${b.hue},80%,65%,0.14)`);
    g.addColorStop(1,   `hsla(${b.hue},75%,62%,0.00)`);
    ax.beginPath();
    ax.ellipse(cx, cy, r, r * 0.75, b.t * 0.003, 0, Math.PI * 2);
    ax.fillStyle = g;
    ax.fill();
  });

  if (frame % 2 === 0) {
    const lx = mxN * AW, ly = myN * AH;
    for (let i = 1; i <= 3; i++) {
      const rad = 40 + i * 55 + Math.sin(frame * 0.04 + i) * 12;
      ax.beginPath();
      ax.arc(lx, ly, rad, 0, Math.PI * 2);
      ax.strokeStyle = `rgba(37,99,235,${0.06 - i * 0.015})`;
      ax.lineWidth = 1;
      ax.stroke();
    }
  }
  requestAnimationFrame(drawAurora);
}
drawAurora();

/* ==============================
   CURSOR — fixed: visible on interactive elements
============================== */
const cur = document.getElementById('cur'), ring = document.getElementById('cur-ring');
let mx = 0, my = 0, rrx = 0, rry = 0;

document.addEventListener('mousemove', e => {
  mx = e.clientX; my = e.clientY;
  cur.style.left = mx + 'px';
  cur.style.top = my + 'px';
});
document.addEventListener('mousedown', () => document.body.classList.add('click'));
document.addEventListener('mouseup', () => document.body.classList.remove('click'));

// Lag ring animation
(function rloop() {
  rrx += (mx - rrx) * .07;
  rry += (my - rry) * .07;
  ring.style.transform = `translate(calc(-50% + ${rrx - mx}px),calc(-50% + ${rry - my}px))`;
  requestAnimationFrame(rloop);
})();

// Add hover class but keep custom cursor visible — the fix!
// We hide the native cursor on body via CSS cursor:none
// On hover elements we set cursor:default so the browser doesn't fight us
// but the custom cursor overlay still renders on top
document.querySelectorAll('a,button,.fcard,.tcard,.pcard,.acard,.contact-card,input,textarea').forEach(el => {
  el.addEventListener('mouseenter', () => {
    document.body.classList.add('hov');
    // Ensure element doesn't show system cursor
    el.style.cursor = 'none';
  });
  el.addEventListener('mouseleave', () => {
    document.body.classList.remove('hov');
    el.style.cursor = '';
  });
});

/* ==============================
   NAV
============================== */
const ham = document.getElementById('ham'), mm = document.getElementById('mm');
ham.addEventListener('click', () => { ham.classList.toggle('open'); mm.classList.toggle('open'); });
function closeMM() { ham.classList.remove('open'); mm.classList.remove('open'); }
window.addEventListener('scroll', () => document.getElementById('nav').classList.toggle('sc', scrollY > 40));

/* ==============================
   HERO TITLE
============================== */
[{ t: 'Modern Websites', a: false }, { t: 'Built for', a: false }, { t: 'Real Businesses.', a: true }].forEach((w, i) => {
  const s = document.createElement('span');
  s.className = 'word' + (w.a ? ' acc' : '');
  s.textContent = i < 2 ? w.t + ' ' : w.t;
  s.style.animationDelay = (.36 + i * .18) + 's';
  document.getElementById('ht').appendChild(s);
});

/* ==============================
   SERVICES
============================== */
[
  { i: '🌐', t: 'Business Websites', d: 'Modern, mobile-friendly websites designed to represent your brand and convert visitors into customers.' },
  { i: '🎯', t: 'Landing Pages', d: 'Focused landing pages built to support marketing campaigns and increase conversions for your business.' },
  { i: '📊', t: 'Admin Dashboards', d: 'Clean dashboards that give businesses real-time insights and control over their operations.' },
  { i: '🧩', t: 'Custom Web Platforms', d: 'Tailored web applications designed around your specific workflows and unique business needs.' }
].forEach((s, i) => {
  const d = document.createElement('div');
  d.className = 'fcard';
  d.style.transitionDelay = (i * .1) + 's';
  d.innerHTML = `<div class="ficon">${s.i}</div><h3>${s.t}</h3><p>${s.d}</p>`;
  document.getElementById('fg').appendChild(d);
});

/* ==============================
   PORTFOLIO — add more projects here
============================== */
const PROJECTS = [
  { title: "Return Spark", desc: "The official website for a small startup company to give customised return gifts and buy gifts", tags: ["HTML", "CSS", "JavaScript"], live: "", github: "", image: "images/Return_Spark.jpg", gradient: "linear-gradient(135deg,#2563eb,#7c3aed)", emoji: "🌐", status: "live" },
  { title: "RS Calligraphy Studio", desc: "Full Stack web app with integrated frontend and backend, including payment processing using Razorpay.and user and database management", tags: ["Flask", "PostgreSQL", "JWT","Razorpay"], live: "", github: "", image: "images/RS_Calligraphy_Studio.jpg", gradient: "linear-gradient(135deg,#059669,#0891b2)", emoji: "✍️", status: "wip" },
  // Add more: { title:"", desc:"", tags:[], live:"", github:"", image:"", gradient:"linear-gradient(135deg,#f59e0b,#ef4444)", emoji:"🚀", status:"live" }
];

const sL = { live: "🟢 Live", wip: "🟡 In Progress", done: "🔵 Completed" };
PROJECTS.forEach((p, i) => {
  const c = document.createElement('div');
  c.className = 'pcard';
  c.style.transitionDelay = (i * .1) + 's';
  const thumb = p.image
    ? `<img src="${p.image}" alt="${p.title}" onerror="this.parentElement.innerHTML='<div class=pthumb-grad style=&quot;background:${p.gradient}&quot;>${p.emoji}</div>'">`
    : `<div class="pthumb-grad" style="background:${p.gradient}">${p.emoji}</div>`;
  const lb = p.live ? `<a href="${p.live}" target="_blank" class="povbtn">View Live ↗</a>` : '';
  const gb = p.github ? `<a href="${p.github}" target="_blank" class="povbtn gh">GitHub</a>` : '';
  c.innerHTML = `<div class="pthumb">${thumb}<div class="poverlay">${lb}${gb}</div></div><div class="pinfo"><div class="ptags">${p.tags.map(t => `<span class="ptag">${t}</span>`).join('')}</div><h3>${p.title}</h3><p>${p.desc}</p><div class="pstatus ${p.status}">${sL[p.status]}</div></div>`;
  document.getElementById('pg').appendChild(c);
});

/* ==============================
   TEAM
============================== */
[
  { n: 'Samrat',   r: 'Frontend & UI',      c: 'KLH Bachupally',       l: 'S' },
  { n: 'Abhijyuth',r: 'Backend & API',      c: 'Vasavi College of Engg.',l:'A' },
  { n: 'Saaketh',  r: 'Systems & Logic',    c: 'CBIT',                 l: 'S' },
  { n: 'Shravanth',r: 'Product & Strategy', c: 'IIIT Hyderabad',       l: 'S' },
  { n: 'Karthik',  r: 'Developer',          c: 'KLH Aziz Nagar',       l: 'K' }
].forEach((m, i) => {
  const d = document.createElement('div');
  d.className = 'tcard';
  d.style.transitionDelay = (i * .08) + 's';
  d.innerHTML = `<div class="avatar">${m.l}</div><h4>${m.n}</h4><div class="role">${m.r}</div><div class="college">${m.c}</div>`;
  document.getElementById('tg').appendChild(d);
});

/* ==============================
   SCROLL REVEAL + TILT
============================== */
const obs = new IntersectionObserver(e => e.forEach(el => { if (el.isIntersecting) el.target.classList.add('vis'); }), { threshold: .1 });
document.querySelectorAll('.rv,.fcard,.tcard,.pcard').forEach(el => obs.observe(el));

if (window.matchMedia('(hover:hover)').matches) {
  document.querySelectorAll('.fcard').forEach(card => {
    card.addEventListener('mousemove', e => {
      const r = card.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - .5, y = (e.clientY - r.top) / r.height - .5;
      card.style.transform = `translateY(-8px) rotateX(${-y * 7}deg) rotateY(${x * 7}deg)`;
    });
    card.addEventListener('mouseleave', () => card.style.transform = '');
  });
}

/* ==============================
   AUTH STATE
============================== */
const API = 'http://localhost:5000'; // ← change to your deployed backend URL
let _pendingSubmit = false;

function getToken() { return sessionStorage.getItem('cys_tok') || ''; }
function getEmail() { return sessionStorage.getItem('cys_em') || ''; }
function setSession(tok, em) { sessionStorage.setItem('cys_tok', tok); sessionStorage.setItem('cys_em', em); refreshAuthUI(); }
function clearSession() { sessionStorage.removeItem('cys_tok'); sessionStorage.removeItem('cys_em'); refreshAuthUI(); }

function refreshAuthUI() {
  const tok = getToken(), em = getEmail();
  const btn = document.getElementById('nav-login-btn'), lbl = document.getElementById('nav-login-label');
  const lb = document.getElementById('logged-bar'), ll = document.getElementById('logged-label');
  if (tok) {
    btn.classList.add('logged'); lbl.textContent = em.split('@')[0];
    lb.style.display = 'flex'; ll.textContent = 'Sending as ' + em;
  } else {
    btn.classList.remove('logged'); lbl.textContent = 'Log In';
    lb.style.display = 'none';
  }
}
refreshAuthUI();

function handleNavLogin() { getToken() ? doLogout() : openModal(); }
function doLogout() { clearSession(); showCfStatus('Logged out.', 'ok'); }

/* ==============================
   AUTH MODAL
============================== */
function openModal() { document.getElementById('auth-modal').classList.add('open'); }
function closeModal() { document.getElementById('auth-modal').classList.remove('open'); }
document.addEventListener('keydown', e => { if (e.key === 'Escape') closeModal(); });

function switchMTab(t) {
  document.querySelectorAll('.mtab').forEach((b, i) => b.classList.toggle('active', i === (t === 'login' ? 0 : 1)));
  document.getElementById('mp-login').classList.toggle('active', t === 'login');
  document.getElementById('mp-signup').classList.toggle('active', t === 'signup');
  document.getElementById('modal-footer-txt').innerHTML = t === 'login'
    ? "Don't have an account? <a onclick=\"switchMTab('signup')\">Sign Up free</a>"
    : "Already have an account? <a onclick=\"switchMTab('login')\">Log In</a>";
}

async function doSignup() {
  const btn = document.getElementById('signup-btn'), st = document.getElementById('signup-status');
  const email = document.getElementById('su-email').value, pass = document.getElementById('su-pass').value;
  if (!email || !pass) { showSt(st, 'Please fill in all fields.', 'err'); return; }
  btn.disabled = true; btn.textContent = 'Creating...';
  try {
    const res = await fetch(`${API}/signup`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ email, password: pass }) });
    const data = await res.json();
    if (res.ok) { showSt(st, '✅ Account created! Logging you in...', 'ok'); setTimeout(() => switchMTab('login'), 1200); }
    else showSt(st, '❌ ' + data.message, 'err');
  } catch { showSt(st, '❌ Cannot reach server (backend offline).', 'err'); }
  finally { btn.disabled = false; btn.textContent = 'Create Account →'; }
}

async function doLogin() {
  const btn = document.getElementById('login-btn'), st = document.getElementById('login-status');
  const email = document.getElementById('li-email').value, pass = document.getElementById('li-pass').value;
  if (!email || !pass) { showSt(st, 'Please enter email and password.', 'err'); return; }
  btn.disabled = true; btn.textContent = 'Logging in...';
  try {
    const res = await fetch(`${API}/login`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ email, password: pass }) });
    const data = await res.json();
    if (res.ok) { setSession(data.token, email); closeModal(); if (_pendingSubmit) { _pendingSubmit = false; submitForm(); } }
    else showSt(st, '❌ ' + data.message, 'err');
  } catch { showSt(st, '❌ Cannot reach server (backend offline).', 'err'); }
  finally { btn.disabled = false; btn.textContent = 'Log In →'; }
}

/* ==============================
   CONTACT FORM FLOW
============================== */
function handleFormSend() {
  if (getToken()) { submitForm(); }
  else { _pendingSubmit = true; openModal(); }
}

async function submitForm() {
  const btn = document.getElementById('cf-submit');
  const name = document.getElementById('cf-name').value;
  const email = document.getElementById('cf-email').value;
  const subject = document.getElementById('cf-subject').value;
  const msg = document.getElementById('cf-msg').value;
  if (!name || !email || !msg) { showCfStatus('Please fill in your name, email and message.', 'err'); return; }
  btn.disabled = true; btn.textContent = 'Sending...';
  try {
    const res = await fetch(`${API}/submit-form`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + getToken() },
      body: JSON.stringify({ subject: `[${name}] ${subject}`, message: `From: ${email}\n\n${msg}` })
    });
    const data = await res.json();
    if (res.ok) {
      showCfStatus("✅ Message sent! We'll get back to you within 24 hours.", 'ok');
      document.getElementById('cf-name').value = '';
      document.getElementById('cf-email').value = '';
      document.getElementById('cf-subject').value = '';
      document.getElementById('cf-msg').value = '';
    } else if (res.status === 401) { clearSession(); showCfStatus('❌ Session expired. Please log in again.', 'err'); }
    else showCfStatus('❌ ' + data.message, 'err');
  } catch {
    showCfStatus('❌ Server offline. Try WhatsApp below or email us directly.', 'err');
  } finally {
    btn.disabled = false; btn.textContent = 'Send Message →';
  }
}

function showCfStatus(msg, type) {
  const el = document.getElementById('cf-status');
  el.textContent = msg; el.className = 'auth-status ' + type; el.style.display = 'block';
  setTimeout(() => el.style.display = 'none', 6000);
}
function showSt(el, msg, type) { el.textContent = msg; el.className = 'auth-status ' + type; el.style.display = 'block'; }
