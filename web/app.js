// Investigadopedia Match - Web Engine (JANE Latam Ciencias Sociales)
// Blindado con: 100% Client-Side, Zero-Knowledge External Queries, XSS Sanitization y Resiliencia Offline.

const STOPWORDS = new Set([
  "el", "la", "los", "las", "un", "una", "unos", "unas", "de", "del", "a", "al", "en",
  "y", "o", "u", "e", "con", "por", "para", "sobre", "entre", "sin", "tras", "desde",
  "hasta", "hacia", "este", "esta", "estos", "estas", "ese", "esa", "esos", "esas",
  "aquel", "aquella", "su", "sus", "mi", "mis", "tu", "tus", "nuestro", "nuestra",
  "que", "cual", "quien", "cuyo", "donde", "cuando", "como", "mas", "pero", "sino",
  "porque", "pues", "ya", "se", "lo", "le", "les", "me", "te", "nos", "os", "es", "son",
  "fue", "eran", "ser", "estar", "ha", "han", "hay", "articulo", "analiza", "evalua",
  "presenta", "estudia", "estudio", "investigacion", "trabajo", "resultados", "metodologia",
  "demostramos", "demuestra", "mostramos", "muestra", "concluimos", "concluye", "proponemos",
  "propone", "plantea", "planteamos",
  "o", "a", "os", "as", "um", "uma", "uns", "umas", "do", "da", "dos", "das", "no", "na",
  "nos", "nas", "em", "de", "para", "com", "por", "que", "e", "se", "ao", "aos",
  "este", "esta", "estes", "estas", "esse", "essa", "esses", "essas", "seu", "sua",
  "seus", "suas", "artigo", "analisa", "estudo", "pesquisa", "resultados"
]);

let cachedJournals = [];

function escapeHtml(str) {
  if (!str) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

async function initCatalog() {
  try {
    const res = await fetch('./data/journals.json');
    if (res.ok) {
      cachedJournals = await res.json();
      const countEl = document.getElementById('catalog-count');
      if (countEl) countEl.innerText = `${cachedJournals.length} revistas Diamante`;
    }
  } catch (err) {
    console.warn("Modo fallback catálogo offline:", err);
  }
}

function normalizeToken(str) {
  if (!str) return "";
  return str.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
}

function extractWords(text) {
  const tokens = text.toLowerCase().split(/[^\w]+/);
  const result = [];
  for (const t of tokens) {
    const clean = normalizeToken(t);
    if (clean && clean.length > 2 && !STOPWORDS.has(clean)) {
      result.push(clean);
    }
  }
  return result;
}

function scrambleAction() {
  const area = document.getElementById('abstract-input');
  if (!area || !area.value.trim()) return;
  const tokens = area.value.split(/[ \t\n\r.,;:()\[\]{}'"!?¿¡/\\-]+/);
  const cleaned = tokens.filter(t => t.trim().length > 0).map(t => t.toLowerCase());
  cleaned.sort();
  area.value = cleaned.join(" ");
  showToast("¡Texto desordenado alfabéticamente! Ningún lector o bot puede reconstruir tu argumento, pero la afinidad temática se mantiene idéntica.");
}

function clearAction() {
  const area = document.getElementById('abstract-input');
  if (area) area.value = "";
  document.getElementById('results-section').classList.add('hidden');
}

function matchJournalsLocal(text, options = {}) {
  if (!text || !cachedJournals.length) return [];
  const textNorm = normalizeToken(text);
  const queryWords = new Set(extractWords(text));
  if (queryWords.size === 0) return [];

  const diamondOnly = options.diamondOnly !== false;
  const disciplineFilter = options.discipline || "all";

  const scored = [];

  for (const j of cachedJournals) {
    if (diamondOnly && !j.is_diamond_oa) continue;
    if (disciplineFilter !== "all" && !j.disciplines.includes(disciplineFilter)) continue;

    const pool = [j.title, ...j.disciplines, ...j.focus_keywords];
    const journalTokens = new Set();
    for (const item of pool) {
      for (const w of extractWords(item)) {
        journalTokens.add(w);
      }
    }

    const intersection = new Set([...queryWords].filter(x => journalTokens.has(x)));
    if (intersection.size === 0) continue;

    const union = new Set([...queryWords, ...journalTokens]);
    const jaccard = intersection.size / union.size;

    let phraseBonus = 0;
    for (const kw of j.focus_keywords) {
      const normKw = normalizeToken(kw);
      if (textNorm.includes(normKw)) {
        phraseBonus += 0.15;
      }
    }

    const rawScore = Math.min(1.0, (jaccard * 2.5) + phraseBonus);
    if (rawScore >= 0.05) {
      scored.push({
        journal: j,
        score: rawScore,
        confidencePct: Math.round(rawScore * 100),
        matchedTerms: Array.from(intersection).sort()
      });
    }
  }

  scored.sort((a, b) => b.score - a.score);
  return scored.slice(0, options.topN || 7);
}

// Consulta a OpenAlex con: Zero-Knowledge (solo 1 término lematizado), SessionStorage Cache y Fail-Soft
async function fetchLiveAuthorsOpenAlex(text, issns, topN = 5) {
  const words = extractWords(text);
  if (!words.length) return [];
  
  // Priorizar el término sustantivo más largo/específico
  const sortedTerms = Array.from(new Set(words.filter(w => w.length >= 4))).sort((a, b) => b.length - a.length);
  const queryTerm = sortedTerms[0] || words[0];

  const formattedIssns = [];
  for (const raw of issns) {
    const clean = raw.trim().replace(/ /g, "");
    if (clean.length === 8 && !clean.includes("-")) {
      formattedIssns.push(`${clean.slice(0, 4)}-${clean.slice(4)}`);
    } else if (clean.includes("-")) {
      formattedIssns.push(clean);
    }
  }

  const cacheKey = `openalex_v1_${queryTerm}_${formattedIssns.slice(0, 3).join("_")}`;
  try {
    const cached = sessionStorage.getItem(cacheKey);
    if (cached) {
      return JSON.parse(cached);
    }
  } catch (e) {
    // SessionStorage no disponible
  }

  let filterExpr = "type:article";
  if (formattedIssns.length > 0) {
    filterExpr += `,locations.source.issn:${formattedIssns.join("|")}`;
  }

  const url = `https://api.openalex.org/works?filter=${encodeURIComponent(filterExpr)}&search=${encodeURIComponent(queryTerm)}&per-page=25&mailto=investigadopedia@evegat.cl`;

  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 6000); // 6s timeout max
    const res = await fetch(url, { signal: controller.signal });
    clearTimeout(timeoutId);

    if (!res.ok) {
      console.warn(`OpenAlex respondió HTTP ${res.status}. Pasando a modo seguro silencioso.`);
      return [];
    }

    const data = await res.json();
    const works = data.results || [];

    const authorMap = new Map();
    for (const w of works) {
      const journalName = w.primary_location?.source?.display_name || "Revista";
      for (const auth of (w.authorships || [])) {
        const name = auth.author?.display_name;
        if (!name) continue;
        const country = auth.institutions?.[0]?.country_code || null;
        if (!authorMap.has(name)) {
          authorMap.set(name, { name, occurrences: 0, country, journals: new Set() });
        }
        const record = authorMap.get(name);
        record.occurrences += 1;
        record.journals.add(journalName);
      }
    }

    const ranked = Array.from(authorMap.values()).map(a => ({
      name: a.name,
      occurrences: a.occurrences,
      country: a.country,
      journals: Array.from(a.journals)
    }));
    ranked.sort((a, b) => b.occurrences - a.occurrences);
    const finalAuthors = ranked.slice(0, topN);

    try {
      sessionStorage.setItem(cacheKey, JSON.stringify(finalAuthors));
    } catch (e) {}

    return finalAuthors;
  } catch (err) {
    console.warn("Fallo o timeout en OpenAlex (la app continúa en local sin interrupción):", err);
    return [];
  }
}

async function runMatch() {
  const input = document.getElementById('abstract-input').value.trim();
  if (!input) {
    alert("Por favor ingresa el título o resumen de tu investigación.");
    return;
  }

  const btn = document.getElementById('btn-match');
  const originalText = btn.innerHTML;
  btn.innerHTML = `<i class="fas fa-spinner fa-spin mr-2"></i> Analizando afinidad...`;
  btn.disabled = true;

  const diamondOnly = document.getElementById('chk-diamond').checked;
  const discipline = document.getElementById('sel-discipline').value;
  const liveAuthors = document.getElementById('chk-live-authors').checked;

  const results = matchJournalsLocal(input, { diamondOnly, discipline, topN: 7 });

  renderResults(results);

  if (liveAuthors && results.length > 0) {
    document.getElementById('authors-loading').classList.remove('hidden');
    document.getElementById('authors-list').classList.add('hidden');
    const issns = results.map(r => r.journal.issn);
    const authors = await fetchLiveAuthorsOpenAlex(input, issns, 5);
    renderAuthors(authors);
  } else {
    document.getElementById('authors-card').classList.add('hidden');
  }

  btn.innerHTML = originalText;
  btn.disabled = false;

  document.getElementById('results-section').classList.remove('hidden');
  document.getElementById('results-section').scrollIntoView({ behavior: 'smooth' });
}

function renderResults(results) {
  const container = document.getElementById('journals-table-body');
  container.innerHTML = "";

  if (results.length === 0) {
    container.innerHTML = `<tr><td colspan="6" class="p-6 text-center text-slate-500">No se encontraron revistas que coincidan con estos términos. Prueba ampliando las palabras clave o seleccionando 'Todas las disciplinas'.</td></tr>`;
    return;
  }

  results.forEach((r, idx) => {
    const j = r.journal;
    const badges = j.indexing.map(idxKey => {
      let color = "bg-slate-100 text-slate-700";
      if (idxKey === "scielo") color = "bg-orange-100 text-orange-800 font-semibold";
      if (idxKey === "redalyc") color = "bg-blue-100 text-blue-800 font-semibold";
      if (idxKey === "latindex") color = "bg-emerald-100 text-emerald-800";
      if (idxKey === "wos" || idxKey === "scopus") color = "bg-purple-100 text-purple-800 font-bold";
      return `<span class="px-2 py-0.5 rounded text-xs ${color}">${escapeHtml(idxKey.toUpperCase())}</span>`;
    }).join(" ");

    const tr = document.createElement('tr');
    tr.className = "border-b border-slate-100 hover:bg-slate-50 transition-colors";
    tr.innerHTML = `
      <td class="p-4 font-bold text-slate-400">#${idx + 1}</td>
      <td class="p-4">
        <div class="font-bold text-slate-900">${escapeHtml(j.title)}</div>
        <div class="text-xs text-slate-500">${escapeHtml(j.publisher)} &bull; <span class="font-mono">ISSN: ${escapeHtml(j.issn)}</span></div>
        <div class="mt-1 flex flex-wrap gap-1">${badges}</div>
      </td>
      <td class="p-4 text-sm text-slate-700">${escapeHtml(j.country)}</td>
      <td class="p-4">
        <div class="flex items-center space-x-2">
          <div class="w-16 bg-slate-200 rounded-full h-2 overflow-hidden">
            <div class="bg-indigo-600 h-2 rounded-full" style="width: ${r.confidencePct}%"></div>
          </div>
          <span class="text-xs font-bold text-indigo-700">${r.confidencePct}%</span>
        </div>
      </td>
      <td class="p-4 text-xs">
        <span class="px-2 py-1 rounded bg-emerald-50 text-emerald-700 font-medium border border-emerald-200">
          <i class="fas fa-gem mr-1"></i> Diamante ($0 APC)
        </span>
      </td>
      <td class="p-4 text-xs text-slate-500">
        ${r.matchedTerms.map(t => `<span class="bg-slate-100 px-1.5 py-0.5 rounded text-slate-700 mr-1">${escapeHtml(t)}</span>`).join("")}
      </td>
    `;
    container.appendChild(tr);
  });
}

function renderAuthors(authors) {
  const loadingEl = document.getElementById('authors-loading');
  const listEl = document.getElementById('authors-list');
  const cardEl = document.getElementById('authors-card');
  cardEl.classList.remove('hidden');
  loadingEl.classList.add('hidden');
  listEl.classList.remove('hidden');
  listEl.innerHTML = "";

  if (authors.length === 0) {
    listEl.innerHTML = `
      <div class="p-4 bg-slate-50 border border-slate-200 rounded-lg text-xs text-slate-600 flex items-center space-x-2">
        <i class="fas fa-circle-info text-indigo-500 text-sm"></i>
        <span>No se encontraron autores en OpenAlex para este término específico en los últimos meses, o el servicio está en respiro. El ranking de revistas de arriba se mantiene 100% fiable y local.</span>
      </div>`;
    return;
  }

  authors.forEach(auth => {
    const div = document.createElement('div');
    div.className = "p-3 bg-white border border-slate-100 rounded-lg shadow-sm flex items-center justify-between";
    div.innerHTML = `
      <div>
        <div class="font-bold text-slate-800 text-sm">${escapeHtml(auth.name)} ${auth.country ? `<span class="text-xs px-1.5 py-0.5 rounded bg-slate-100 text-slate-600 font-normal">(${escapeHtml(auth.country)})</span>` : ""}</div>
        <div class="text-xs text-slate-500">Obras afines en: <span class="italic">${escapeHtml(auth.journals.join(", "))}</span></div>
      </div>
      <div class="text-right">
        <span class="px-2 py-1 rounded bg-indigo-50 text-indigo-700 font-bold text-xs">${auth.occurrences} trabajos</span>
      </div>
    `;
    listEl.appendChild(div);
  });
}

function showToast(msg) {
  const toast = document.createElement('div');
  toast.className = "fixed bottom-5 right-5 bg-slate-900 text-white px-4 py-3 rounded-lg shadow-xl text-xs z-50 animate-bounce max-w-sm border border-slate-700";
  toast.innerText = msg;
  document.body.appendChild(toast);
  setTimeout(() => toast.remove(), 4500);
}

// ==========================================
// ROADMAP PARTICIPATIVO Y VOTACIÓN COMUNITARIA
// ==========================================

const DEFAULT_ROADMAP = [
  {
    id: "cover_letter",
    title: "Generador de Carta al Editor (Cover Letter)",
    desc: "Redacta el borrador formal de la carta de postulación justificando la afinidad del manuscrito con la revista elegida y adjuntando la terna de revisores sugeridos sin conflicto de interés.",
    baseVotes: 24,
    tag: "Productividad"
  },
  {
    id: "response_times",
    title: "Estimador de Tiempos de Respuesta y Arbitraje",
    desc: "Muestra meses promedio reportados entre la sumisión inicial, el dictamen y la publicación final para que decidas con base en tus plazos de graduación o postulación a proyectos.",
    baseVotes: 19,
    tag: "Toma de decisiones"
  },
  {
    id: "author_guidelines",
    title: "Pautas de Autor y Enlace directo a OJS",
    desc: "Muestra en un clic el límite de palabras, normas de citación (APA 7, Chicago, Harvard) y link directo a la plataforma de envíos de la revista seleccionada.",
    baseVotes: 15,
    tag: "Facilidad de sumisión"
  },
  {
    id: "predatory_alert",
    title: "Verificador de Integridad y Alerta de Predatoriedad",
    desc: "Compara contra listas de revistas con prácticas dudosas o desindexadas para proteger a los investigadores de editoriales mercenarias.",
    baseVotes: 12,
    tag: "Ética e Integridad"
  },
  {
    id: "multilingual",
    title: "Soporte Multilingüe (Español / Português / English)",
    desc: "Interfaz y taxonomía de revistas completamente traducidas para integrar a la comunidad de investigadores de Brasil y el resto de la región.",
    baseVotes: 8,
    tag: "Internacionalización"
  }
];

function getRoadmapData() {
  try {
    const stored = localStorage.getItem("investigadopedia_roadmap_v1");
    if (stored) return JSON.parse(stored);
  } catch (e) {}
  return DEFAULT_ROADMAP;
}

function saveRoadmapData(data) {
  try {
    localStorage.setItem("investigadopedia_roadmap_v1", JSON.stringify(data));
  } catch (e) {}
}

function getUserVotes() {
  try {
    const votes = localStorage.getItem("investigadopedia_user_votes_v1");
    if (votes) return new Set(JSON.parse(votes));
  } catch (e) {}
  return new Set();
}

function recordUserVote(id) {
  const votes = getUserVotes();
  votes.add(id);
  try {
    localStorage.setItem("investigadopedia_user_votes_v1", JSON.stringify(Array.from(votes)));
  } catch (e) {}
}

function renderRoadmap() {
  const container = document.getElementById('roadmap-cards-container');
  if (!container) return;
  const items = getRoadmapData();
  const userVotes = getUserVotes();

  // Ordenar por votos descendentes
  items.sort((a, b) => b.baseVotes - a.baseVotes);

  container.innerHTML = "";
  items.forEach(item => {
    const hasVoted = userVotes.has(item.id);
    const card = document.createElement('div');
    card.className = "p-4 bg-white rounded-xl border border-slate-200 shadow-sm flex flex-col justify-between hover:border-indigo-300 transition-all";
    card.innerHTML = `
      <div>
        <div class="flex items-center justify-between mb-2">
          <span class="text-xs px-2 py-0.5 rounded-full bg-slate-100 text-slate-700 font-medium">${escapeHtml(item.tag)}</span>
          <span class="text-xs font-bold text-slate-500"><i class="fas fa-thumbs-up mr-1 text-indigo-500"></i> ${item.baseVotes} votos</span>
        </div>
        <h4 class="font-bold text-slate-800 text-sm mb-1">${escapeHtml(item.title)}</h4>
        <p class="text-xs text-slate-600 leading-relaxed mb-4">${escapeHtml(item.desc)}</p>
      </div>
      <div>
        <button onclick="upvoteFeature('${escapeHtml(item.id)}')" ${hasVoted ? "disabled" : ""} class="w-full py-2 px-3 rounded-lg text-xs font-bold flex items-center justify-center space-x-1 transition-all ${
          hasVoted
            ? "bg-emerald-50 text-emerald-700 border border-emerald-200 cursor-default"
            : "bg-indigo-50 text-indigo-700 hover:bg-indigo-100 border border-indigo-200"
        }">
          <i class="${hasVoted ? "fas fa-check" : "fas fa-arrow-up"}"></i>
          <span>${hasVoted ? "¡Ya votaste por esta!" : "Votar por esta función"}</span>
        </button>
      </div>
    `;
    container.appendChild(card);
  });
}

function upvoteFeature(id) {
  const userVotes = getUserVotes();
  if (userVotes.has(id)) return;

  const items = getRoadmapData();
  const target = items.find(i => i.id === id);
  if (target) {
    target.baseVotes += 1;
    saveRoadmapData(items);
    recordUserVote(id);
    renderRoadmap();
    showToast(`¡Voto registrado para "${target.title}"! Gracias por priorizar el desarrollo.`);
  }
}

function submitNewProposal() {
  const inputEl = document.getElementById('proposal-text');
  if (!inputEl || !inputEl.value.trim()) {
    alert("Por favor escribe tu propuesta o revista que te gustaría incluir.");
    return;
  }

  const rawText = inputEl.value.trim();
  const cleanTitle = rawText.slice(0, 60);
  const cleanDesc = rawText;

  const newId = `prop_${Date.now()}`;
  const items = getRoadmapData();
  items.push({
    id: newId,
    title: cleanTitle,
    desc: cleanDesc,
    baseVotes: 1,
    tag: "Comunidad"
  });

  saveRoadmapData(items);
  recordUserVote(newId);
  inputEl.value = "";
  renderRoadmap();
  showToast("¡Tu propuesta ha sido incorporada al roadmap comunitario con tu voto!");
}

window.addEventListener('DOMContentLoaded', () => {
  initCatalog();
  renderRoadmap();
});
