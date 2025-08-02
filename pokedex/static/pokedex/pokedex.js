document.addEventListener('DOMContentLoaded', () => {
  const listEl        = document.getElementById('pokemon-list');
  const detailEl      = document.getElementById('pokemon-detail');
  const prevBtn       = document.getElementById('prev-btn');
  const nextBtn       = document.getElementById('next-btn');
  const pageIndicator = document.getElementById('page-indicator');

  // Filter inputs
  const searchInput   = document.getElementById('search-input');
  const typeSelect    = document.getElementById('type-select');
  const abilitySelect = document.getElementById('ability-select');
  const applyBtn      = document.getElementById('apply-filters');
  const clearBtn      = document.getElementById('clear-filters');

  let currentPage = 1;
  const limit = 20;
  let totalPages = 1;

  function loadOptions(url, selectEl) {
    fetch(url)
      .then(r => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        return r.json();
      })
      .then(data => {
        selectEl.innerHTML = '';
        data.forEach(item => {
          const opt = document.createElement('option');
          opt.value = item.name;
          opt.textContent = item.name;
          selectEl.appendChild(opt);
        });
      })
      .catch(err => {
        console.error(`Error loading options from ${url}:`, err);
      });
  }

  loadOptions('/api/types/',    typeSelect);
  loadOptions('/api/abilities/', abilitySelect);

  function fetchList(page) {
    const params = new URLSearchParams();
    params.set('page',  page);
    params.set('limit', limit);

    const searchVal = searchInput.value.trim();
    if (searchVal) params.set('search', searchVal);

    Array.from(typeSelect.selectedOptions).forEach(opt =>
      params.append('type', opt.value)
    );
    Array.from(abilitySelect.selectedOptions).forEach(opt =>
      params.append('ability', opt.value)
    );

    fetch(`/api/pokemon/?${params.toString()}`)
      .then(r => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        return r.json();
      })
      .then(data => {
        listEl.innerHTML = '';
        data.results.forEach(poke => {
          const li = document.createElement('li');
          const a  = document.createElement('a');
          a.href        = '#';
          a.textContent = poke.name;
          a.dataset.id  = poke.id;
          a.addEventListener('click', e => {
            e.preventDefault();
            fetchDetail(e.target.dataset.id);
          });
          li.appendChild(a);
          listEl.appendChild(li);
        });

        totalPages = Math.ceil(data.count / limit);
        currentPage = page;
        pageIndicator.textContent = `Page ${currentPage} of ${totalPages}`;
        prevBtn.disabled = currentPage <= 1;
        nextBtn.disabled = currentPage >= totalPages;
      })
      .catch(err => {
        console.error('Error fetching list:', err);
        listEl.innerHTML = '<li>Error loading data</li>';
      });
  }

  function fetchDetail(id) {
    fetch(`/api/pokemon/${id}/`)
      .then(r => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        return r.json();
      })
      .then(p => {
        let html = `
          <h3>${p.name}</h3>
          <img class="sprite" src="${p.sprite_url}" alt="${p.name}">
          <ul>
            <li><strong>Height:</strong> ${p.height}</li>
            <li><strong>Weight:</strong> ${p.weight}</li>
            <li><strong>Base Exp:</strong> ${p.base_experience}</li>
            <li><strong>Types:</strong> ${p.types.join(', ')}</li>
            <li><strong>Abilities:</strong> ${p.abilities.join(', ')}</li>
          </ul>
        `;

        if (p.evolution && p.evolution.length) {
          html += '<h3>Evolution Chain</h3>';
          html += '<p class="evolution-chain">' + p.evolution.join(' → ') + '</p>';
        } else {
          html += '<p><em>No evolution chain available.</em></p>';
        }

        detailEl.innerHTML = html;
      })
      .catch(err => {
        console.error('Error fetching detail:', err);
        detailEl.innerHTML = '<p>Error loading detail</p>';
      });
  }

  prevBtn.addEventListener('click', () => {
    if (currentPage > 1) fetchList(currentPage - 1);
  });
  nextBtn.addEventListener('click', () => {
    if (currentPage < totalPages) fetchList(currentPage + 1);
  });
  applyBtn.addEventListener('click', () => fetchList(1));
  clearBtn.addEventListener('click', () => {
    searchInput.value = '';
    Array.from(typeSelect.options).forEach(o => o.selected = false);
    Array.from(abilitySelect.options).forEach(o => o.selected = false);
    fetchList(1);
  });

  fetchList(currentPage);
});