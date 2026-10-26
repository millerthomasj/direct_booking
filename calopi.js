/* Calopi-only photo movement. No dependencies or booking integrations. */
(() => {
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  document.querySelectorAll('[data-slider]').forEach(slider => {
    const track = slider.querySelector('.slider-track');
    const frames = [...track.children];
    const caption = slider.querySelector('.slider-caption');
    const announcement = slider.querySelector('.slider-announcement');
    const pause = slider.querySelector('[data-pause]');
    let active = 0, timer, manuallyPaused = false, hover = false, startX, startY;
    const dots = frames.map((frame, index) => {
      const button = document.createElement('button');
      button.type = 'button';
      button.setAttribute('aria-label', `Show photo ${index + 1}: ${frame.querySelector('img').alt}`);
      button.addEventListener('click', () => show(index, true));
      slider.querySelector('.slider-dots').append(button);
      return button;
    });
    const syncTimer = () => {
      clearInterval(timer);
      if (slider.dataset.autoplay === 'true' && !reduced.matches && !manuallyPaused && !hover && !slider.contains(document.activeElement) && !document.hidden) {
        timer = setInterval(() => show(active + 1), 6500);
      }
      pause.hidden = reduced.matches;
      pause.textContent = manuallyPaused ? 'Play' : 'Pause';
      pause.setAttribute('aria-label', manuallyPaused ? 'Play slideshow' : 'Pause slideshow');
      pause.setAttribute('aria-pressed', String(manuallyPaused));
    };
    const show = (index, manual = false) => {
      active = (index + frames.length) % frames.length;
      track.style.transform = `translateX(-${active * 100}%)`;
      frames.forEach((frame, i) => frame.setAttribute('aria-hidden', String(i !== active)));
      dots.forEach((dot, i) => dot.setAttribute('aria-current', String(i === active)));
      caption.textContent = frames[active].dataset.caption;
      if (manual) announcement.textContent = `Photo ${active + 1} of ${frames.length}: ${frames[active].querySelector('img').alt}`;
      slider.dataset.activeSlide = String(active);
      syncTimer();
    };
    slider.querySelector('[data-prev]').addEventListener('click', () => show(active - 1, true));
    slider.querySelector('[data-next]').addEventListener('click', () => show(active + 1, true));
    pause.addEventListener('click', () => { manuallyPaused = !manuallyPaused; syncTimer(); });
    slider.addEventListener('keydown', event => {
      if (event.key === 'ArrowRight' || event.key === 'ArrowLeft') {
        event.preventDefault(); show(active + (event.key === 'ArrowRight' ? 1 : -1), true);
      }
    });
    slider.addEventListener('mouseenter', () => { hover = true; syncTimer(); });
    slider.addEventListener('mouseleave', () => { hover = false; syncTimer(); });
    slider.addEventListener('focusin', syncTimer);
    slider.addEventListener('focusout', () => requestAnimationFrame(syncTimer));
    slider.addEventListener('touchstart', e => {startX = e.changedTouches[0].clientX; startY = e.changedTouches[0].clientY;}, {passive: true});
    slider.addEventListener('touchend', e => {
      const dx = e.changedTouches[0].clientX - startX, dy = e.changedTouches[0].clientY - startY;
      if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy)) show(active + (dx < 0 ? 1 : -1), true);
    }, {passive: true});
    document.addEventListener('visibilitychange', syncTimer);
    reduced.addEventListener('change', syncTimer);
    show(0);
  });
  // Content remains visible without JavaScript and for reduced-motion visitors.
  if (!reduced.matches && 'IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => entries.forEach(entry => {
      if (entry.isIntersecting) {entry.target.classList.add('is-visible'); observer.unobserve(entry.target);}
    }), {threshold: 0.08});
    document.querySelectorAll('[data-reveal]').forEach(el => {el.classList.add('will-reveal'); observer.observe(el);});
  }
})();
