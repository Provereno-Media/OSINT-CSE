
let allData = [];
let fuse;

const searchInput = document.getElementById("search");
const categorySelect = document.getElementById("category");
const resultsEl = document.getElementById("results");
const countEl = document.getElementById("count");

fetch("data.json")
  .then(r => r.json())
  .then(data => {
    allData = data;
    const sections = [...new Set(data.map(d => d.section))].sort();
    sections.forEach(s => {
      const opt = document.createElement("option");
      opt.value = s; opt.textContent = s;
      categorySelect.appendChild(opt);
    });
    fuse = new Fuse(allData, {
      keys: ["name", "desc", "section", "region"],
      threshold: 0.35,
      ignoreLocation: true
    });
    render(allData);
  });

function render(items){
  resultsEl.innerHTML = "";
  countEl.textContent = items.length + (items.length === 1 ? " engine" : " engines");
  if(items.length === 0){
    resultsEl.innerHTML = '<p class="empty">No matches. Try a different search term or category.</p>';
    return;
  }
  const frag = document.createDocumentFragment();
  items.forEach(item => {
    const card = document.createElement("div");
    card.className = "card";
    card.innerHTML = `
      <h3><a href="${item.link}" target="_blank" rel="noopener">${escapeHtml(item.name)}</a></h3>
      <p>${escapeHtml(item.desc)}</p>
      <div class="tags">
        <span class="tag">${escapeHtml(item.section)}</span>
        ${item.region ? `<span class="region">${item.region}</span>` : ""}
      </div>
    `;
    frag.appendChild(card);
  });
  resultsEl.appendChild(frag);
}

function escapeHtml(str){
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}

function applyFilters(){
  const q = searchInput.value.trim();
  const cat = categorySelect.value;
  let base = cat ? allData.filter(d => d.section === cat) : allData;
  if(q){
    const searchIn = cat ? base : allData;
    const results = fuse.search(q).map(r => r.item);
    base = cat ? results.filter(d => d.section === cat) : results;
  }
  render(base);
}

searchInput.addEventListener("input", applyFilters);
categorySelect.addEventListener("change", applyFilters);
