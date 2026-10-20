const canvas = document.querySelector('#scope');
const ctx = canvas.getContext('2d');
const scope = canvas.closest('.scope');
const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
const status = document.querySelector('#audio-status');
const readout = {
  clip: document.querySelector('#readout-clip'),
  event: document.querySelector('#readout-event'),
  length: document.querySelector('#readout-length'),
};
// The CRT is dark in both themes, so its colors are fixed rather than themed.
const TRACE = '#ffb000';
const GRATICULE = 'rgba(255, 176, 0, 0.14)';
const PHOSPHOR = 'rgba(10, 13, 11, 0.32)';
const player = new Audio();
player.preload = 'auto';
let audioContext;
let analyzer;
let samples;
let activeButton;
let raf = 0;

function fit() {
  const ratio = Math.min(window.devicePixelRatio || 1, 2);
  const { width, height } = canvas.getBoundingClientRect();
  canvas.width = Math.round(width * ratio);
  canvas.height = Math.round(height * ratio);
}

function graticule() {
  const { width, height } = canvas;
  ctx.save();
  ctx.strokeStyle = GRATICULE;
  ctx.lineWidth = 1;
  ctx.beginPath();
  for (let i = 1; i < 10; i++) { const x = Math.round((width * i) / 10) + 0.5; ctx.moveTo(x, 0); ctx.lineTo(x, height); }
  for (let i = 1; i < 8; i++) { const y = Math.round((height * i) / 8) + 0.5; ctx.moveTo(0, y); ctx.lineTo(width, y); }
  ctx.stroke();
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(0, height / 2); ctx.lineTo(width, height / 2);
  ctx.moveTo(width / 2, 0); ctx.lineTo(width / 2, height);
  ctx.stroke();
  ctx.restore();
}

function stroke(points, gain = 1) {
  const { width, height } = canvas;
  ctx.save();
  ctx.strokeStyle = TRACE;
  ctx.lineWidth = Math.max(2, width / 320);
  ctx.lineJoin = 'round';
  ctx.shadowColor = TRACE;
  ctx.shadowBlur = width / 50;
  ctx.beginPath();
  points.forEach((value, index) => {
    const x = (index / (points.length - 1)) * width;
    const y = height / 2 - Math.max(-1, Math.min(1, value * gain)) * height * 0.42;
    if (index) ctx.lineTo(x, y); else ctx.moveTo(x, y);
  });
  ctx.stroke();
  ctx.restore();
}

function idle() {
  cancelAnimationFrame(raf);
  ctx.fillStyle = '#0a0d0b';
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  graticule();
  // A faint, fixed hum so the standby trace reads as a live instrument.
  stroke(Array.from({ length: 240 }, (_, i) => Math.sin(i * 0.31) * 0.006 + Math.sin(i * 1.7) * 0.004));
}

function live() {
  analyzer.getFloatTimeDomainData(samples);
  ctx.fillStyle = PHOSPHOR;
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  graticule();
  // Speech rarely peaks past a third of full scale, so the live trace is amplified to fill the screen.
  stroke(samples, 2.6);
  raf = requestAnimationFrame(live);
}

// Reduced motion: draw the whole clip's amplitude envelope once instead of animating.
async function envelope(url) {
  const buffer = await audioContext.decodeAudioData(await (await fetch(url)).arrayBuffer());
  const channel = buffer.getChannelData(0);
  const columns = 240;
  const step = Math.floor(channel.length / columns) || 1;
  const peaks = Array.from({ length: columns }, (_, column) => {
    let peak = 0;
    for (let i = column * step; i < (column + 1) * step && i < channel.length; i++) peak = Math.max(peak, Math.abs(channel[i]));
    return peak;
  });
  idle();
  stroke(peaks.flatMap(peak => [peak, -peak]));
}

function ensureAudio() {
  if (audioContext) return audioContext.resume();
  audioContext = new AudioContext();
  analyzer = audioContext.createAnalyser();
  analyzer.fftSize = 2048;
  samples = new Float32Array(analyzer.fftSize);
  audioContext.createMediaElementSource(player).connect(analyzer);
  analyzer.connect(audioContext.destination);
  return audioContext.resume();
}

function settle(message) {
  scope.classList.remove('live');
  activeButton?.classList.remove('playing');
  activeButton = null;
  if (!reducedMotion.matches) idle();
  if (message) status.textContent = message;
}

async function play(button) {
  const url = `audio/${button.dataset.clip}.wav`;
  activeButton?.classList.remove('playing');
  activeButton = button;
  readout.clip.textContent = button.dataset.line;
  readout.event.textContent = button.dataset.event;
  readout.length.textContent = `${button.dataset.length} s`;
  try {
    await ensureAudio();
    player.src = url;
    await player.play();
    if (activeButton !== button) return;
    button.classList.add('playing');
    scope.classList.add('live');
    status.textContent = `Playing: ${button.dataset.line}`;
    cancelAnimationFrame(raf);
    if (reducedMotion.matches) await envelope(url);
    else live();
  } catch {
    if (activeButton === button) settle('Playback unavailable. Check your browser audio settings or try agent-johnny5 preview.');
  }
}

player.addEventListener('ended', () => settle('Preview finished. Need more input? Pick another line.'));
document.querySelectorAll('[data-clip]').forEach(button => button.addEventListener('click', () => play(button)));
const chips = [...document.querySelectorAll('.chip[data-clip]')];
document.querySelector('#random-clip').addEventListener('click', () => play(chips[Math.floor(Math.random() * chips.length)]));

new ResizeObserver(() => { fit(); if (!scope.classList.contains('live')) idle(); }).observe(canvas);
fit();
idle();

document.querySelectorAll('[data-copy]').forEach(button => button.addEventListener('click', async () => {
  const copyStatus = document.querySelector('#copy-status');
  try {
    await navigator.clipboard.writeText(document.getElementById(button.dataset.copy).textContent);
    copyStatus.textContent = 'Commands copied.';
    button.textContent = 'Copied';
    button.classList.add('copied');
    setTimeout(() => { button.textContent = 'Copy'; button.classList.remove('copied'); }, 2000);
  } catch { copyStatus.textContent = 'Clipboard unavailable. Select and copy the commands above.'; }
}));
