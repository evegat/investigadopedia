// Investigadopedia — Ecosistema Abierto para Investigadores de Ciencias Sociales
// Privacidad garantizada: Ejecución en tu navegador, sin almacenamiento de manuscritos ni entrenamiento de IA.

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
        <div class="font-bold text-slate-900">
          ${j.url ? `<a href="${escapeHtml(j.url)}" target="_blank" class="hover:text-indigo-600 hover:underline inline-flex items-center gap-1.5">${escapeHtml(j.title)} <i class="fas fa-arrow-up-right-from-square text-[10px] text-slate-400"></i></a>` : escapeHtml(j.title)}
        </div>
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
    baseVotes: 0,
    tag: "Productividad"
  },
  {
    id: "response_times",
    title: "Estimador de Tiempos de Respuesta y Arbitraje",
    desc: "Muestra meses promedio reportados entre la sumisión inicial, el dictamen y la publicación final para que decidas con base en tus plazos de graduación o postulación a proyectos.",
    baseVotes: 0,
    tag: "Toma de decisiones"
  },
  {
    id: "author_guidelines",
    title: "Pautas de Autor y Enlace directo a OJS",
    desc: "Muestra en un clic el límite de palabras, normas de citación (APA 7, Chicago, Harvard) y link directo a la plataforma de envíos de la revista seleccionada.",
    baseVotes: 0,
    tag: "Facilidad de sumisión"
  },
  {
    id: "predatory_alert",
    title: "Verificador de Integridad y Alerta de Predatoriedad",
    desc: "Compara contra listas de revistas con prácticas dudosas o desindexadas para proteger a los investigadores de editoriales mercenarias.",
    baseVotes: 0,
    tag: "Ética e Integridad"
  },
  {
    id: "multilingual",
    title: "Soporte Multilingüe (Español / Português / English)",
    desc: "Interfaz y taxonomía de revistas completamente traducidas para integrar a la comunidad de investigadores de Brasil y el resto de la región.",
    baseVotes: 0,
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
          <span class="text-xs font-bold text-slate-500"><i class="fas fa-thumbs-up mr-1 text-indigo-500"></i> ${item.baseVotes} votos (locales)</span>
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

// ==========================================
// NAVEGACIÓN ENTRE PESTAÑAS
// ==========================================

function switchTab(tabId) {
  const tabs = ['match', 'catalog', 'roadmap'];
  tabs.forEach(t => {
    const section = document.getElementById(`section-${t}`);
    const deskBtn = document.getElementById(`tab-btn-${t}`);
    const mobBtn = document.getElementById(`mob-tab-btn-${t}`);

    if (t === tabId) {
      if (section) section.classList.remove('hidden');
      if (deskBtn) {
        deskBtn.className = "px-3 py-2 rounded-lg text-indigo-700 bg-indigo-50 font-bold transition-colors";
      }
      if (mobBtn) {
        mobBtn.className = "px-2.5 py-1.5 rounded text-indigo-700 font-bold whitespace-nowrap bg-indigo-50";
      }
    } else {
      if (section) section.classList.add('hidden');
      if (deskBtn) {
        deskBtn.className = "px-3 py-2 rounded-lg text-slate-600 hover:text-slate-900 hover:bg-slate-100 font-semibold transition-colors";
      }
      if (mobBtn) {
        mobBtn.className = "px-2.5 py-1.5 rounded text-slate-600 font-medium whitespace-nowrap";
      }
    }
  });

  window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ==========================================
// CATÁLOGO DE HABILIDADES Y REPOSITORIOS (ESTILO AITMPL)
// ==========================================

const CATALOG_ITEMS = [
  {
    id: "epistemology-audit",
    category: "methods",
    categoryLabel: "Habilidad y Método",
    badgeColor: "bg-blue-50 text-blue-700 border-blue-200",
    type: "Protocolo y Prompt",
    title: "Vigilancia Epistemológica",
    icon: "fa-scale-balanced",
    shortDesc: "Audita manuscritos académicos separando hechos empíricos de inferencias teóricas o supuestos sin respaldo.",
    fullDesc: "Protocolo de auditoría para manuscritos científicos antes de su postulación a comisiones evaluadoras o arbitraje por pares ciegos. Detecta saltos causales injustificados y obliga a desglosar las afirmaciones del artículo en Hechos comprobados, Inferencias analíticas plausibles y Supuestos o brechas teóricas a verificar.",
    tags: ["Epistemología", "Rigor Metodológico", "Arbitraje por Pares", "Auditoría"],
    actionType: "prompt",
    author: "Eduardo Vega / MyWorld",
    promptText: `Actúa como un Auditor Epistemológico y Revisor Metodológico experto en Ciencias Sociales para revistas iberoamericanas de corriente principal.

Tu tarea es revisar críticamente el siguiente borrador o sección de manuscrito, identificando cualquier desliz conceptual o metodológico.

Específicamente, debes clasificar cada afirmación sustantiva del texto en una de estas tres categorías:
1. [HECHO COMPROBADO]: Información sustentada directamente por los datos empíricos presentados en el texto.
2. [INFERENCIA ANALÍTICA]: Deducción o interpretación lógica derivada de los datos, evaluando si el salto inductivo es razonable o excesivo.
3. [SUPUESTO NO CONTRASTADO / BRECHA]: Afirmación que se asume como verdad pero carece de respaldo empírico o cita directa en el manuscrito.

Entrega una matriz con:
- Párrafo o afirmación auditada.
- Clasificación epistemológica.
- Riesgo de objeción por parte de evaluadores ciegos (Bajo / Medio / Alto).
- Recomendación de redacción sobria y anclada.

Aquí está el texto a auditar:
[PEGA TU TEXTO AQUÍ]`
  },
  {
    id: "scielo-redalyc-harvester",
    category: "harvest",
    categoryLabel: "Bases y Cosecha",
    badgeColor: "bg-amber-50 text-amber-700 border-amber-200",
    type: "Estrategia de Cosecha",
    title: "Cosecha Desinsesgada SciELO & Redalyc",
    icon: "fa-wheat-awn",
    shortDesc: "Estrategia de búsqueda sistemática para recuperar literatura regional en español y portugués sin sesgo anglosajón.",
    fullDesc: "Los motores comerciales tradicionales (Scopus y WoS) subrepresentan severamente la producción de América Latina. Este flujo define ecuaciones de búsqueda balanceadas, lematización en español y extracción de descriptores desde SciELO y Redalyc para asegurar que las realidades locales formen parte integral del estado del arte.",
    tags: ["SciELO", "Redalyc", "Acceso Abierto Diamante", "Estado del Arte"],
    actionType: "prompt",
    author: "Investigadopedia",
    promptText: `Actúa como un Bibliotecario Especialista en Bibliometría y Cosecha de Literatura Científica Iberoamericana en Ciencias Sociales.

Ayúdame a formular una estrategia de búsqueda sistemática y desinsesgada sobre el siguiente tema de investigación:
[ESCRIBE AQUÍ TU TEMA O PREGUNTA DE INVESTIGACIÓN]

Genera:
1. Desglose en conceptos clave (Término raíz, sinónimos en español y portugués, descriptores UNESCO / Tesauro de Ciencias Sociales).
2. Ecuación booleana optimizada para el buscador avanzado de SciELO Org (con operadores AND, OR, comillas para frases exactas).
3. Ecuación booleana optimizada para el portal Redalyc.org.
4. Criterios de delimitación temporal y geográfica para evitar sobrerrepresentación de literatura no transferible al contexto regional.`
  },
  {
    id: "prisma-screening",
    category: "methods",
    categoryLabel: "Habilidad y Método",
    badgeColor: "bg-emerald-50 text-emerald-700 border-emerald-200",
    type: "Flujo Metodológico",
    title: "Cribador Sistemático PRISMA 2020",
    icon: "fa-filter-circle-dollar",
    shortDesc: "Flujo reproducible de inclusión y exclusión documental con registro auditable para diagramas de flujo PRISMA.",
    fullDesc: "Guía metodológica para revisiones bibliográficas sistemáticas y de alcance (Scoping Reviews). Cada documento descartado queda codificado con una justificación explícita (duplicación, desfase temporal, diseño metodológico no pertinente o población disímil), garantizando total reproducibilidad ante revisores de revistas indexadas.",
    tags: ["PRISMA 2020", "Revisión Sistemática", "Scoping Review", "Transparencia"],
    actionType: "prompt",
    author: "Investigadopedia",
    promptText: `Actúa como un Metodólogo Experto en Revisiones Sistemáticas bajo la declaración PRISMA 2020 (Preferred Reporting Items for Systematic Reviews and Meta-Analyses).

Tengo un conjunto inicial de registros recuperados para mi revisión sobre:
[TEMA DE LA REVISIÓN]

Necesito que estructures la pauta de cribado (screening) en dos fases:
Fase 1: Cribado por Título y Resumen (Criterios rápidos de exclusión binaria).
Fase 2: Lectura a Texto Completo (Matriz de extracción estructurada).

Para cada exclusión, genera un código normalizado de descarte (ej: EXC-01: No aborda políticas públicas locales; EXC-02: Metodología meramente de opinión sin datos empíricos; EXC-03: Duplicado pre-print).
Adicionalmente, genera la plantilla de tabla para alimentar el diagrama de flujo PRISMA 2020 (Identificación, Cribado, Idoneidad e Inclusión).`
  },
  {
    id: "socratic-tutor",
    category: "tutoring",
    categoryLabel: "Prompts y Tutores",
    badgeColor: "bg-purple-50 text-purple-700 border-purple-200",
    type: "Tutor Mayéutico",
    title: "Auditor Mayéutico de Coherencia",
    icon: "fa-brain",
    shortDesc: "Tutor socrático que interroga la alineación lógica entre problema, teoría, diseño metodológico y conclusiones.",
    fullDesc: "Este agente no redacta el artículo por ti: adopta el rol de un evaluador socrático riguroso y formativo. Lee tu diseño y te hace 4 preguntas punzantes sobre las debilidades lógicas de tu propuesta, ayudándote a blindar tu artículo antes de someterlo al arbitraje ciego.",
    tags: ["Tutoría Socrática", "Coherencia Interna", "Diseño de Tesis", "Prompt"],
    actionType: "prompt",
    author: "Eduardo Vega / MyWorld",
    promptText: `Actúa como un Tutor Socrático y Revisor Metodológico riguroso para tesis y artículos en Ciencias Sociales.

Tu principio rector es: NUNCA escribas el texto por el autor ni le des soluciones hechas. Tu labor es interrogar mayéuticamente la coherencia interna de su investigación.

Lee el siguiente planteamiento (pregunta, objetivo general, marco teórico y diseño metodológico propuesto):
[PEGA AQUÍ TU PREGUNTA, OBJETIVO Y METODOLOGÍA]

Formula exactamente 4 preguntas críticas y orientadas a la acción sobre:
1. Alineación lógica: ¿La técnica propuesta realmente responde a la pregunta planteada, o solo mide un síntoma periférico?
2. Operacionalización: ¿Cómo se traducen los conceptos teóricos abstractos en observaciones empíricas concretas sin perder validez?
3. Amenazas a la validez: ¿Qué explicaciones alternativas podrían justificar los mismos resultados sin que tu hipótesis sea cierta?
4. Limitaciones y sesgos: ¿Qué población o perspectiva queda inadvertidamente invisibilizada por tu muestra?`
  },
  {
    id: "cover-letter-builder",
    category: "tutoring",
    categoryLabel: "Prompts y Tutores",
    badgeColor: "bg-indigo-50 text-indigo-700 border-indigo-200",
    type: "Herramienta Editorial",
    title: "Generador de Carta al Editor (Cover Letter)",
    icon: "fa-envelope-open-text",
    shortDesc: "Plantilla formal para presentar un manuscrito destacando el aporte regional y sugiriendo revisores pares.",
    fullDesc: "Una carta al editor bien fundamentada aumenta notablemente las probabilidades de superar el filtro inicial del equipo editorial. Esta herramienta estructura una justificación sólida de novedad temática y pertinencia para la revista, incorporando la propuesta de evaluadores externos sin conflicto de intereses.",
    tags: ["Postulación", "Comité Editorial", "Cover Letter", "Sumisión"],
    actionType: "prompt",
    author: "Investigadopedia",
    promptText: `Actúa como un Consultor Editorial Académico senior para publicaciones científicas en América Latina.

Ayúdame a redactar una carta formal de presentación (Cover Letter) para enviar a la revista:
- Nombre de la Revista: [NOMBRE DE LA REVISTA]
- Título del manuscrito: [TÍTULO]
- Tipo de contribución: [Artículo de investigación empírica / Ensayo teórico / Revisión sistemática]
- Principales hallazgos y relevancia para los lectores de esta revista: [RESUMEN DE 2-3 LÍNEAS]
- Nombres y afiliaciones de 3 revisores pares sugeridos (sin conflicto de interés): [REVISORES]

Escribe la carta en un tono académico sobrio, directo y formal en español, respetando las normas internacionales de integridad científica (declaración de originalidad, no postulación simultánea y ausencia de conflicto de interés).`
  },
  {
    id: "delaglosa-repo",
    category: "repos",
    categoryLabel: "Observatorios y Repos",
    badgeColor: "bg-blue-50 text-blue-700 border-blue-200",
    type: "Plataforma Abierta",
    title: "De la Glosa a la Calle",
    icon: "fa-landmark",
    shortDesc: "Observatorio cívico de gasto público, compras y presupuesto del Estado chileno.",
    fullDesc: "Plataforma ciudadana y académica que sistematiza millones de transacciones de compras públicas (Mercado Público), transferencias del Estado y ejecución presupuestaria de ministerios y servicios públicos de Chile. Dispone de visualizaciones interactivas y descarga de datos abiertos para investigación empírica en gestión pública y transparencia.",
    tags: ["Gasto Público", "Compras Públicas", "Chile", "Datos Abiertos"],
    actionType: "repo",
    url: "https://delaglosaalacalle.evegat.cl",
    githubUrl: "https://github.com/evegat/delaglosaalacalle",
    author: "Eduardo Vega / MyWorld"
  },
  {
    id: "normatia-repo",
    category: "repos",
    categoryLabel: "Observatorios y Repos",
    badgeColor: "bg-emerald-50 text-emerald-700 border-emerald-200",
    type: "Catastro y Datos",
    title: "Brújula IA Educación Superior",
    icon: "fa-compass",
    shortDesc: "Catastro y análisis comparado de normativas sobre uso ético de inteligencia artificial en universidades.",
    fullDesc: "Repositorio abierto que analiza cómo las instituciones de educación superior en Chile e Iberoamérica están regulando el uso de modelos de lenguaje e inteligencia artificial en la docencia, la evaluación y la investigación científica. Incluye matrices de comparación de directrices éticas y políticas de integridad académica.",
    tags: ["Educación Superior", "Ética en IA", "Integridad Académica", "Normativas"],
    actionType: "repo",
    url: "https://github.com/evegat/brujula-ia-edusuperior",
    githubUrl: "https://github.com/evegat/brujula-ia-edusuperior",
    author: "Eduardo Vega / MyWorld"
  },
  {
    id: "timunicipal-repo",
    category: "repos",
    categoryLabel: "Observatorios y Repos",
    badgeColor: "bg-purple-50 text-purple-700 border-purple-200",
    type: "Plataforma y Datos",
    title: "Observatorio TI Municipal",
    icon: "fa-building-columns",
    shortDesc: "Diagnóstico integral de capacidades tecnológicas y software en los 345 municipios de Chile.",
    fullDesc: "Estudio empírico exhaustivo sobre la infraestructura digital, gobernanza de datos, plataformas de atención ciudadana y ciberseguridad en el nivel municipal chileno. Permite correlacionar indicadores de brecha tecnológica con variables socioeconómicas y territoriales.",
    tags: ["Gobierno Local", "Municipalidades", "Transformación Digital", "Brecha Digital"],
    actionType: "repo",
    url: "https://observatoriotimunicipal.evegat.cl",
    githubUrl: "https://github.com/evegat/observatorio-ti-municipal",
    author: "Eduardo Vega / MyWorld"
  },
  {
    id: "core-repo",
    category: "repos",
    categoryLabel: "Observatorios y Repos",
    badgeColor: "bg-slate-50 text-slate-700 border-slate-200",
    type: "Código Abierto",
    title: "Investigadopedia Core (Python)",
    icon: "fa-code",
    shortDesc: "Motor algorítmico libre en Python para recomendación de revistas, afinidad léxica y sugerencia de evaluadores.",
    fullDesc: "Paquete en Python 3 que implementa algoritmos de similitud textual con lematización y filtrado de palabras vacías en español y portugués, catálogo de revistas diamante y cliente seguro contra OpenAlex. Diseñado con cobertura de pruebas automatizadas y estándares de reproducibilidad científica.",
    tags: ["Python", "Código Abierto", "Bibliometría", "Licencia MIT"],
    actionType: "repo",
    url: "https://investigadopedia.evegat.cl",
    githubUrl: "https://github.com/evegat/investigadopedia",
    author: "Eduardo Vega / MyWorld"
  }
];

let currentCatalogCategory = "all";

function setCatalogCategory(cat) {
  currentCatalogCategory = cat;
  
  // Actualizar estilos de pills
  const pills = document.querySelectorAll('.cat-pill');
  pills.forEach(p => {
    p.className = "cat-pill px-3 py-1.5 rounded-lg font-medium bg-slate-100 hover:bg-slate-200 text-slate-700 transition-all";
  });

  const activePill = document.getElementById(`pill-${cat}`);
  if (activePill) {
    activePill.className = "cat-pill px-3 py-1.5 rounded-lg font-bold bg-indigo-700 text-white transition-all shadow-xs";
  }

  renderCatalog();
}

function filterCatalog() {
  renderCatalog();
}

function resetCatalogFilters() {
  const searchInput = document.getElementById('catalog-search-input');
  if (searchInput) searchInput.value = "";
  setCatalogCategory("all");
}

function renderCatalog() {
  const container = document.getElementById('catalog-cards-container');
  const emptyState = document.getElementById('catalog-empty-state');
  if (!container) return;

  const searchInput = document.getElementById('catalog-search-input');
  const query = searchInput ? searchInput.value.trim().toLowerCase() : "";

  // Conteo por categoría
  const countAll = CATALOG_ITEMS.length;
  const countMethods = CATALOG_ITEMS.filter(i => i.category === 'methods').length;
  const countTutoring = CATALOG_ITEMS.filter(i => i.category === 'tutoring').length;
  const countHarvest = CATALOG_ITEMS.filter(i => i.category === 'harvest').length;
  const countRepos = CATALOG_ITEMS.filter(i => i.category === 'repos').length;

  const elAll = document.getElementById('count-all');
  const elMethods = document.getElementById('count-methods');
  const elTutoring = document.getElementById('count-tutoring');
  const elHarvest = document.getElementById('count-harvest');
  const elRepos = document.getElementById('count-repos');
  const elTotal = document.getElementById('catalog-total-count');

  if (elAll) elAll.innerText = `(${countAll})`;
  if (elMethods) elMethods.innerText = `(${countMethods})`;
  if (elTutoring) elTutoring.innerText = `(${countTutoring})`;
  if (elHarvest) elHarvest.innerText = `(${countHarvest})`;
  if (elRepos) elRepos.innerText = `(${countRepos})`;
  if (elTotal) elTotal.innerText = countAll;

  // Filtrado
  const filtered = CATALOG_ITEMS.filter(item => {
    // Filtro de categoría
    if (currentCatalogCategory !== "all" && item.category !== currentCatalogCategory) {
      return false;
    }
    // Filtro de texto
    if (!query) return true;
    const pool = [
      item.title,
      item.shortDesc,
      item.categoryLabel,
      item.type,
      ...item.tags
    ].join(" ").toLowerCase();
    return pool.includes(query);
  });

  if (filtered.length === 0) {
    container.innerHTML = "";
    if (emptyState) emptyState.classList.remove('hidden');
    return;
  }

  if (emptyState) emptyState.classList.add('hidden');
  container.innerHTML = "";

  filtered.forEach(item => {
    const card = document.createElement('div');
    card.className = "bg-white rounded-xl border border-slate-200 p-5 shadow-xs hover:border-indigo-300 hover:shadow-md transition-all flex flex-col justify-between";

    // Tags
    const tagsHtml = item.tags.map(t => `<span class="bg-slate-100 text-slate-600 px-2 py-0.5 rounded text-[11px] font-medium">#${escapeHtml(t)}</span>`).join(" ");

    // Botones de acción
    let actionsHtml = "";
    if (item.actionType === "prompt") {
      actionsHtml = `
        <div class="flex items-center space-x-2 pt-3 border-t border-slate-100">
          <button onclick="copyPrompt('${escapeHtml(item.id)}')" class="flex-1 py-1.5 px-3 bg-indigo-50 hover:bg-indigo-100 text-indigo-700 font-bold rounded-lg text-xs transition-colors flex items-center justify-center space-x-1.5">
            <i class="fas fa-copy"></i>
            <span>Copiar Prompt</span>
          </button>
          <button onclick="openModal('${escapeHtml(item.id)}')" class="py-1.5 px-3 bg-slate-100 hover:bg-slate-200 text-slate-700 font-medium rounded-lg text-xs transition-colors">
            Ver Ficha
          </button>
        </div>
      `;
    } else {
      actionsHtml = `
        <div class="flex items-center space-x-2 pt-3 border-t border-slate-100">
          <a href="${escapeHtml(item.url)}" target="_blank" class="flex-1 py-1.5 px-3 bg-slate-900 hover:bg-slate-800 text-white font-bold rounded-lg text-xs transition-colors flex items-center justify-center space-x-1.5 text-center">
            <span>Visitar Sitio</span>
            <i class="fas fa-arrow-up-right-from-square text-[10px]"></i>
          </a>
          ${item.githubUrl ? `
            <a href="${escapeHtml(item.githubUrl)}" target="_blank" class="p-1.5 text-slate-600 hover:text-slate-900 bg-slate-100 hover:bg-slate-200 rounded-lg text-xs px-2.5 transition-colors" title="Ver código en GitHub">
              <i class="fab fa-github"></i>
            </a>
          ` : ""}
          <button onclick="openModal('${escapeHtml(item.id)}')" class="py-1.5 px-3 bg-slate-100 hover:bg-slate-200 text-slate-700 font-medium rounded-lg text-xs transition-colors">
            Ficha
          </button>
        </div>
      `;
    }

    card.innerHTML = `
      <div>
        <div class="flex items-center justify-between mb-3">
          <span class="text-[11px] font-bold px-2 py-0.5 rounded-full border ${item.badgeColor}">${escapeHtml(item.categoryLabel)}</span>
          <span class="text-[11px] text-slate-400 font-medium">${escapeHtml(item.type)}</span>
        </div>
        <div class="flex items-start space-x-3 mb-2">
          <div class="w-8 h-8 rounded-lg bg-indigo-50 text-indigo-700 flex items-center justify-center text-sm shrink-0 mt-0.5">
            <i class="fas ${escapeHtml(item.icon)}"></i>
          </div>
          <div>
            <h3 class="font-bold text-slate-900 text-sm leading-snug">${escapeHtml(item.title)}</h3>
          </div>
        </div>
        <p class="text-xs text-slate-600 leading-relaxed mb-4">${escapeHtml(item.shortDesc)}</p>
      </div>

      <div>
        <div class="flex flex-wrap gap-1 mb-3">
          ${tagsHtml}
        </div>
        ${actionsHtml}
      </div>
    `;

    container.appendChild(card);
  });
}

function openModal(id) {
  const item = CATALOG_ITEMS.find(i => i.id === id);
  if (!item) return;

  const modal = document.getElementById('component-modal');
  const icon = document.getElementById('modal-icon');
  const category = document.getElementById('modal-category');
  const type = document.getElementById('modal-type');
  const title = document.getElementById('modal-title');
  const desc = document.getElementById('modal-desc');
  const tagsContainer = document.getElementById('modal-tags-container');
  const actionBox = document.getElementById('modal-action-box');
  const author = document.getElementById('modal-author');

  if (icon) icon.className = `fas ${item.icon}`;
  if (category) {
    category.innerText = item.categoryLabel;
    category.className = `text-xs px-2.5 py-0.5 rounded-full font-bold border ${item.badgeColor}`;
  }
  if (type) type.innerText = item.type;
  if (title) title.innerText = item.title;
  if (desc) desc.innerText = item.fullDesc;
  if (author) author.innerText = item.author;

  if (tagsContainer) {
    tagsContainer.innerHTML = item.tags.map(t => `<span class="bg-slate-100 text-slate-700 px-2.5 py-1 rounded-md text-xs font-medium">#${escapeHtml(t)}</span>`).join(" ");
  }

  if (actionBox) {
    if (item.actionType === "prompt") {
      actionBox.innerHTML = `
        <div class="space-y-2">
          <div class="flex items-center justify-between">
            <span class="font-bold text-slate-900 text-xs">Instrucción para Asistente (Prompt Listo para Usar):</span>
            <button onclick="copyPrompt('${escapeHtml(item.id)}')" class="px-3 py-1 bg-indigo-700 hover:bg-indigo-800 text-white font-bold rounded text-xs flex items-center space-x-1 transition-colors">
              <i class="fas fa-copy mr-1"></i> Copiar Prompt Completo
            </button>
          </div>
          <pre class="bg-slate-900 text-slate-100 p-4 rounded-xl text-[11px] font-mono leading-relaxed overflow-x-auto whitespace-pre-wrap">${escapeHtml(item.promptText)}</pre>
        </div>
      `;
    } else {
      actionBox.innerHTML = `
        <div class="space-y-3">
          <h5 class="font-bold text-slate-900 text-xs">Enlaces y Recursos del Repositorio:</h5>
          <div class="flex flex-wrap gap-2">
            <a href="${escapeHtml(item.url)}" target="_blank" class="px-4 py-2 bg-indigo-700 hover:bg-indigo-800 text-white font-bold rounded-lg text-xs flex items-center space-x-2 transition-colors">
              <i class="fas fa-globe"></i>
              <span>Visitar Plataforma en Vivo</span>
            </a>
            ${item.githubUrl ? `
              <a href="${escapeHtml(item.githubUrl)}" target="_blank" class="px-4 py-2 bg-slate-900 hover:bg-slate-800 text-white font-bold rounded-lg text-xs flex items-center space-x-2 transition-colors">
                <i class="fab fa-github"></i>
                <span>Ver Código en GitHub</span>
              </a>
            ` : ""}
          </div>
        </div>
      `;
    }
  }

  if (modal) modal.classList.remove('hidden');
}

function closeModal() {
  const modal = document.getElementById('component-modal');
  if (modal) modal.classList.add('hidden');
}

function copyPrompt(id) {
  const item = CATALOG_ITEMS.find(i => i.id === id);
  if (!item || !item.promptText) return;

  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(item.promptText).then(() => {
      showToast(`¡Prompt copiado! Puedes pegarlo en tu asistente preferido para iniciar la auditoría.`);
    }).catch(() => {
      fallbackCopy(item.promptText);
    });
  } else {
    fallbackCopy(item.promptText);
  }
}

function fallbackCopy(text) {
  const ta = document.createElement('textarea');
  ta.value = text;
  document.body.appendChild(ta);
  ta.select();
  try {
    document.execCommand('copy');
    showToast(`¡Prompt copiado al portapapeles!`);
  } catch (e) {
    alert("Copia el texto directamente desde la ficha.");
  }
  ta.remove();
}

// Shortcuts de Teclado
window.addEventListener('keydown', (e) => {
  // Ctrl + K o Cmd + K -> Enfocar buscador de catálogo
  if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
    e.preventDefault();
    switchTab('catalog');
    const input = document.getElementById('catalog-search-input');
    if (input) {
      input.focus();
      input.select();
    }
  }

  // Escape -> Cerrar modal
  if (e.key === 'Escape') {
    closeModal();
  }
});

// Cerrar modal al hacer clic en el backdrop
window.addEventListener('click', (e) => {
  const modal = document.getElementById('component-modal');
  if (modal && e.target === modal) {
    closeModal();
  }
});

window.addEventListener('DOMContentLoaded', () => {
  initCatalog();
  renderRoadmap();
  renderCatalog();
});
