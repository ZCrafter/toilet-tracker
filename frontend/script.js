document.addEventListener('DOMContentLoaded', () => {
  const type = document.getElementById('type');
  const locationFields = document.getElementById('locationFields');
  const sumFields = document.getElementById('sumFields');
  const submitBtn = document.getElementById('submit');
  const statsDiv = document.getElementById('stats');
  const sumStatsDiv = document.getElementById('sumStats');
  const toggleSumStats = document.getElementById('toggleSumStats');
  const darkToggle = document.getElementById('darkToggle');

  const aliases = {
    stephy: 'stephaney',
    steph: 'stephaney',
    stephaney: 'stephaney',
    johnny: 'john',
    jon: 'john'
  };

  function normalizeName(name) {
    return aliases[name.toLowerCase()] || name.toLowerCase();
  }

  type.addEventListener('change', () => {
    const value = type.value;
    locationFields.classList.toggle('hidden', value === 'sum');
    sumFields.classList.toggle('hidden', value !== 'sum');
    submitBtn.className = value;
  });

  submitBtn.addEventListener('click', async () => {
    const t = type.value;
    const now = new Date().toISOString();

    if (t === 'pee' || t === 'poo') {
      const payload = {
        time: now,
        location: document.getElementById('location').value
      };
      await fetch(`http://localhost:8000/${t}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
    } else {
      const names = [
        document.getElementById('name1').value,
        document.getElementById('name2').value,
        document.getElementById('name3').value
      ].filter(Boolean).map(normalizeName);
      const vr = document.getElementById('vr').checked;
      const payload = { time: now, vr, names };
      await fetch('http://localhost:8000/sum', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
    }

    loadStats();
  });

  toggleSumStats.addEventListener('click', () => {
    sumStatsDiv.classList.toggle('hidden');
  });

  darkToggle.addEventListener('change', () => {
    document.documentElement.classList.toggle('dark', darkToggle.checked);
    document.body.style.backgroundColor = darkToggle.checked ? '#121212' : '#fff';
    document.body.style.color = darkToggle.checked ? 'white' : 'black';
  });

  async function loadStats() {
    const res = await fetch('http://localhost:8000/stats');
    const data = await res.json();
    const { pee, poo, sum } = data;

    statsDiv.innerHTML = `
      <p>Pees: ${pee.length}</p>
      <p>Poos: ${poo.length}</p>
      <p>Last Pee: ${pee[pee.length - 1]?.time || 'N/A'}</p>
      <p>Last Poo: ${poo[poo.length - 1]?.time || 'N/A'}</p>
    `;

    const nameCount = {};
    sum.forEach(entry => {
      entry.names.forEach(n => {
        const norm = normalizeName(n);
        nameCount[norm] = (nameCount[norm] || 0) + 1;
      });
    });
    const total = sum.length;
    const namesHTML = Object.entries(nameCount)
      .map(([name, count]) => `<p>${name}: ${(count / total * 100).toFixed(1)}%</p>`)
      .join('');

    sumStatsDiv.innerHTML = `
      <p>Total Sums: ${total}</p>
      <div>${namesHTML}</div>
    `;
  }

  loadStats();
});
