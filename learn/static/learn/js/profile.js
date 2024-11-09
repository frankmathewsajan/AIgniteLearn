//Just scroll even if there isn't content that needs to be scrolled 🤗

const header = document.getElementById('header');

window.addEventListener('mousewheel', event => {
  let delta = (event.wheelDelta + 3) * -1;
  animate(delta > 0, delta);
});

const animate = (check, delta) => {
  const MIN_HEIGHT = 80;
  const HEIGHT = 150;
  const MAX_ZOOM = 3;
  const MAX_BLUR = 3;
  if (check) {
    let blur = 1 + delta / 150 < MAX_BLUR ? Math.ceil(1 + delta / 150) : MAX_BLUR;
    let height = HEIGHT - delta / 10 > MIN_HEIGHT ? Math.ceil(HEIGHT - delta / 10) : MIN_HEIGHT;
    let zoom = 1 + delta / 200 <= MAX_ZOOM ? 1 + delta / 200 : MAX_ZOOM;
    requestAnimationFrame(transform(header, blur, height, zoom));
  } else
  requestAnimationFrame(transform(header, 0, 150, 1));
};

const transform = (element, blur, height, zoom) => {
  element.style.filter = `blur(${blur}px)`;
  element.style.height = `${height}px`;
  element.style.transform = `scale(${zoom},${zoom})`;
};