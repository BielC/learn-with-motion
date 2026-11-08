/* Inline this file into a standalone lesson. Topic-specific scenes stay in render(). */
window.createMotionPlayer = function createMotionPlayer(options) {
  const { audio, cues, duration, render, root = document, onError = console.error } = options;
  if (!audio || !cues?.length || !(duration > 0) || typeof render !== 'function') {
    throw new Error('Supply an audio element, measured cues, duration and render(t, context).');
  }
  const find = id => root.querySelector(`#${id}`);
  const controls = Object.assign({
    play: find('play'), replay: find('replay'), seek: find('seek'),
    back: find('back'), forward: find('forward'), speed: find('speed'),
    voice: find('voice'), clock: find('clock'), caption: find('caption'),
  }, options.controls);
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const clamp = t => Math.max(0, Math.min(duration, Number(t) || 0));
  const fmt = t => `${Math.floor(t / 60)}:${String(Math.floor(t % 60)).padStart(2, '0')}`;
  const state = { time: 0, playing: false, exporting: false };
  const listeners = [];
  let raf = null, generation = 0, destroyed = false;
  function listen(target, event, handler) {
    if (!target) return;
    target.addEventListener(event, handler);
    listeners.push(() => target.removeEventListener(event, handler));
  }
  function cancelLoop() { if (raf !== null) cancelAnimationFrame(raf); raf = null; }
  function syncControls() {
    if (controls.seek) controls.seek.value = state.time;
    if (controls.clock) controls.clock.textContent = `${fmt(state.time)} / ${fmt(duration)}`;
    if (controls.play) controls.play.textContent = state.playing ? 'Pause' : state.time >= duration - .05 ? 'Replay' : 'Play';
  }
  function draw(t) {
    state.time = clamp(t);
    const index = Math.max(0, cues.findLastIndex(c => c.start <= state.time));
    const cue = cues[index];
    const progress = Math.max(0, Math.min(1, (state.time - cue.start) / Math.max(.001, cue.voiceEnd - cue.start)));
    const frame = { cue, index, progress, reducedMotion: reduced.matches && !state.exporting, exporting: state.exporting };
    render(state.time, frame);
    if (controls.caption) controls.caption.textContent = options.captionText ? options.captionText(state.time, frame) : cue.cap || '';
    syncControls();
  }
  function loop() {
    raf = null;
    if (!state.playing || state.exporting || destroyed) return;
    draw(audio.currentTime);
    raf = requestAnimationFrame(loop);
  }
  function pause() {
    generation++;
    state.playing = false;
    audio.pause();
    cancelLoop();
    if (!state.exporting && !destroyed) draw(audio.currentTime);
  }
  function seek(t) {
    if (state.exporting || destroyed) return;
    audio.currentTime = clamp(t);
    draw(t);
  }
  async function play() {
    if (state.exporting || destroyed || state.playing) return;
    if (state.time >= duration - .05) seek(0);
    const request = ++generation;
    state.playing = true;
    syncControls();
    try {
      await audio.play();
      if (request !== generation || !state.playing || state.exporting || destroyed) return;
      cancelLoop();
      raf = requestAnimationFrame(loop);
    } catch (error) {
      if (request !== generation) return;
      state.playing = false;
      syncControls();
      onError(error);
    }
  }
  function exportFrame(t) {
    if (destroyed) throw new Error('Player was destroyed.');
    if (!state.exporting) {
      pause();
      state.exporting = true;
      document.body.classList.add('export');
    }
    draw(t);
    return state.time;
  }
  if (controls.seek) { controls.seek.min = 0; controls.seek.max = duration; }
  listen(controls.play, 'click', () => state.playing ? pause() : play());
  listen(controls.replay, 'click', () => { if (!state.exporting) { pause(); seek(0); play(); } });
  listen(controls.back, 'click', () => seek(state.time - 5));
  listen(controls.forward, 'click', () => seek(state.time + 5));
  listen(controls.seek, 'input', () => seek(controls.seek.value));
  listen(controls.speed, 'change', () => { if (!state.exporting) audio.playbackRate = Number(controls.speed.value); });
  listen(controls.voice, 'click', () => {
    audio.muted = !audio.muted;
    controls.voice.setAttribute('aria-pressed', String(!audio.muted));
    controls.voice.textContent = audio.muted ? 'Voice off' : 'Voice on';
  });
  listen(audio, 'ended', () => { if (!state.exporting) { pause(); draw(duration); } });
  listen(audio, 'seeked', () => { if (!state.exporting) draw(audio.currentTime); });
  listen(reduced, 'change', () => { if (!state.exporting) draw(state.time); });
  listen(document, 'keydown', e => {
    if (state.exporting || e.altKey || e.ctrlKey || e.metaKey || e.target.closest('input,select,textarea,summary,a,button,[contenteditable]')) return;
    if (e.code === 'Space') { e.preventDefault(); state.playing ? pause() : play(); }
    if (e.key === 'ArrowLeft') { e.preventDefault(); seek(state.time - 5); }
    if (e.key === 'ArrowRight') { e.preventDefault(); seek(state.time + 5); }
  });
  listen(window, 'resize', () => { if (!state.exporting) draw(state.time); });
  const api = {
    duration, cues, play, pause, seek, frame: seek, render: draw, exportFrame,
    get time() { return state.time; }, get playing() { return state.playing; },
    get exporting() { return state.exporting; },
    exitExport() { state.exporting = false; document.body.classList.remove('export'); seek(state.time); },
    destroy() { pause(); destroyed = true; listeners.splice(0).forEach(remove => remove()); },
  };
  draw(0);
  return api;
};
