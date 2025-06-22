// Utilities
function qs(id){ return document.getElementById(id); }
function nowISO() {
  const dt = new Date();
  dt.setMinutes(dt.getMinutes() - dt.getTimezoneOffset());
  return dt.toISOString().slice(0,16);
}

window.onload = () => {
  // set default times
  ['pee-ts','poop-ts','sum-ts'].forEach(id => {
    if (qs(id)) qs(id).value = nowISO();
  });
  // theme toggle
  const toggle = qs('theme-toggle');
  const saved = localStorage.getItem('theme');
  if (saved==='light') document.body.classList.add('light');
  toggle.onclick = () => {
    document.body.classList.toggle('light');
    localStorage.setItem('theme', document.body.classList.contains('light')?'light':'dark');
  };
  // dashboard init
  if (location.pathname === '/dashboard') loadStats();
  const tsBtn = qs('toggle-sum');
  if (tsBtn) tsBtn.onclick = () => {
    const c = qs('sum-content');
    c.classList.toggle('hidden');
    tsBtn.textContent = c.classList.contains('hidden')? 'Show Sum Stats':'Hide Sum Stats';
  };
};

function submitPee(){
  fetch('/api/pee', {
    method:'POST', headers:{'Content-Type':'application/json'},
    body: JSON.stringify({
      ts: qs('pee-ts').value,
      location: qs('pee-loc').value
    })
  }).then(_=> alert('Pee logged!'));
}

function submitPoop(){
  fetch('/api/poop', {
    method:'POST', headers:{'Content-Type':'application/json'},
    body: JSON.stringify({
      ts: qs('poop-ts').value,
      location: qs('poop-loc').value
    })
  }).then(_=> alert('Poop logged!'));
}

function submitSum(){
  fetch('/api/sum', {
    method:'POST', headers:{'Content-Type':'application/json'},
    body: JSON.stringify({
      ts: qs('sum-ts').value,
      vr: qs('sum-vr').checked,
      name1: qs('name1').value,
      name2: qs('name2').value,
      name3: qs('name3').value
    })
  }).then(_=> alert('Sum logged!'));
}

function loadStats(){
  fetch('/api/stats')
    .then(r=> r.json())
    .then(data=>{
      // pee
      qs('pee-avg-interval').textContent = data.pee.avg_interval||'–';
      qs('pee-daily-avg').textContent = data.pee.daily_avg;
      const pl = qs('pee-list');
      data.pee.events.reverse().forEach(e=>{
        const d = new Date(e.ts).toLocaleString();
        pl.innerHTML += `<li>${d} @ ${e.loc}</li>`;
      });
      // poop
      qs('poop-avg-interval').textContent = data.poop.avg_interval||'–';
      qs('poop-daily-avg').textContent = data.poop.daily_avg;
      const pol = qs('poop-list');
      data.poop.events.reverse().forEach(e=>{
        const d = new Date(e.ts).toLocaleString();
        pol.innerHTML += `<li>${d} @ ${e.loc}</li>`;
      });
      // sum
      const sl = qs('sum-list');
      data.sum.names.forEach(n=>{
        sl.innerHTML += `<li>${n.name}: ${n.count} (${n.pct}%)</li>`;
      });
    });
}
