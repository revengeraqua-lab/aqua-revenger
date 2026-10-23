// Spread nearby city labels into two readable columns, keeping their true anchors.
export function createGlobePins(root, cities, onSelect) {
  const svg = root.querySelector('.globe-pin-lines');
  const mount = root.querySelector('.globe-pins');
  const ns = 'http://www.w3.org/2000/svg';
  const pins = cities.map((city, i) => {
    const button = document.createElement('button');
    button.type = 'button'; button.className = 'globe-pin'; button.hidden = true;
    button.setAttribute('aria-label', 'Show ' + city.city + ' on globe');
    const number = document.createElement('span'); number.textContent = String(i + 1).padStart(2, '0');
    button.append(number, document.createTextNode(city.city));
    button.addEventListener('click', () => onSelect(i)); mount.append(button);
    const line = document.createElementNS(ns, 'path'); svg.append(line);
    return { city, button, line, i };
  });
  const groups = [pins.filter(p => p.city.state === 'Maharashtra'), pins.filter(p => p.city.state !== 'Maharashtra')];
  groups.forEach(group => group.sort((a, b) => b.city.lat - a.city.lat));
  return {
    update(width, height, selected) {
      svg.setAttribute('viewBox', `0 0 ${width} ${height}`);
      const narrow = width < 400, w = narrow ? 96 : 108, h = narrow ? 24 : 26, gap = narrow ? 5 : 6;
      let shown = 0;
      groups.forEach((group, side) => {
        const visible = group.filter(p => p.city.visible);
        const total = visible.length * h + Math.max(0, visible.length - 1) * gap;
        const mean = visible.reduce((sum, p) => sum + p.city.screen.y, 0) / Math.max(1, visible.length);
        const top = Math.max(16, Math.min(height - total - 16, mean - total / 2));
        const x = side === 0 ? (narrow ? 5 : 10) : width - w - (narrow ? 5 : 10);
        let row = 0;
        group.forEach(pin => {
          const isVisible = pin.city.visible;
          pin.button.hidden = !isVisible; pin.line.style.display = isVisible ? '' : 'none';
          pin.button.setAttribute('aria-pressed', String(pin.i === selected));
          if (!isVisible) return;
          const y = top + row++ * (h + gap), endX = side === 0 ? x + w : x;
          pin.button.style.width = w + 'px'; pin.button.style.height = h + 'px';
          pin.button.style.transform = `translate(${x}px,${y}px)`;
          pin.line.setAttribute('d', `M ${pin.city.screen.x.toFixed(1)} ${pin.city.screen.y.toFixed(1)} L ${endX + (side === 0 ? 10 : -10)} ${y + h / 2} L ${endX} ${y + h / 2}`);
          pin.line.classList.toggle('is-selected', pin.i === selected); shown++;
        });
      });
      root.dataset.visiblePins = String(shown);
    },
    hide() { pins.forEach(pin => { pin.button.hidden = true; pin.line.style.display = 'none'; }); }
  };
}
