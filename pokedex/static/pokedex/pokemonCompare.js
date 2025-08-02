document.addEventListener('DOMContentLoaded', () => {
  const input1   = document.getElementById('poke1-search');
  const data1    = document.getElementById('poke1-datalist');
  const input2   = document.getElementById('poke2-search');
  const data2    = document.getElementById('poke2-datalist');
  const compare  = document.getElementById('compare-btn');
  const resultEl = document.getElementById('compare-result');

  const map1 = new Map();
  const map2 = new Map();

  setupDatalist(input1, data1, map1);
  setupDatalist(input2, data2, map2);

  compare.addEventListener('click', () => {
    const name1 = input1.value.trim();
    const name2 = input2.value.trim();
    const id1   = map1.get(name1);
    const id2   = map2.get(name2);

    if (!id1 || !id2) {
      resultEl.textContent = 'Please select two valid Pokémon from the list.';
      return;
    }
    if (id1 === id2) {
      resultEl.textContent = 'Select two different Pokémon.';
      return;
    }

    fetch(`/api/pokemon/compare/?id1=${id1}&id2=${id2}`)
      .then(r => r.ok ? r.json() : Promise.reject(r.status))
      .then(({ pokemon1, pokemon2 }) => {
        resultEl.innerHTML = `
          <div class="compare-cards">
            
            <div class="card">
              <h3>${pokemon1.name}</h3>
              <img src="${pokemon1.sprite_url}" alt="${pokemon1.name}">
              <ul>
                <li>Height: ${pokemon1.height}</li>
                <li>Weight: ${pokemon1.weight}</li>
                <li>Base Exp: ${pokemon1.base_experience}</li>
                <li>Types: ${pokemon1.types.join(', ')}</li>
                <li>Abilities: ${pokemon1.abilities.join(', ')}</li>
              </ul>
            </div>
            
            <div class="card">
              <h3>${pokemon2.name}</h3>
              <img src="${pokemon2.sprite_url}" alt="${pokemon2.name}">
              <ul>
                <li>Height: ${pokemon2.height}</li>
                <li>Weight: ${pokemon2.weight}</li>
                <li>Base Exp: ${pokemon2.base_experience}</li>
                <li>Types: ${pokemon2.types.join(', ')}</li>
                <li>Abilities: ${pokemon2.abilities.join(', ')}</li>
              </ul>
            </div>
          </div>
        `;
      })
      .catch(err => {
        console.error('Compare error:', err);
        resultEl.textContent = 'Error fetching comparison.';
      });
  });

  function setupDatalist(inputEl, datalistEl, map) {
    function load(q) {
      const url = q
        ? `/api/pokemon/?search=${encodeURIComponent(q)}&page=1&limit=20`
        : `/api/pokemon/?page=1&limit=20`;
      fetch(url)
        .then(r => r.ok ? r.json() : Promise.reject(r.status))
        .then(data => {
          datalistEl.innerHTML = '';
          map.clear();
          data.results.forEach(poke => {
            const opt = document.createElement('option');
            opt.value = poke.name;
            map.set(poke.name, poke.id);
            datalistEl.appendChild(opt);
          });
        })
        .catch(err => console.error('Search error:', err));
    }

    inputEl.addEventListener('input', () => {
      load(inputEl.value.trim());
    });
    inputEl.addEventListener('focus', () => {
      if (!inputEl.value.trim()) load('');
    });
    inputEl.addEventListener('click', () => {
      if (!inputEl.value.trim()) load('');
    });
  }
});