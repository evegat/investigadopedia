const stages = ["formulacion", "literatura", "metodo", "datos", "analisis", "escritura", "auditoria"];

const state = {
  tools: [],
  selectedStage: "literatura",
  selectedTool: null
};

const els = {
  stageNav: document.querySelector("#stageNav"),
  toolList: document.querySelector("#toolList"),
  catalogCount: document.querySelector("#catalogCount"),
  searchInput: document.querySelector("#searchInput"),
  licenseFilter: document.querySelector("#licenseFilter"),
  detailName: document.querySelector("#detailName"),
  detailType: document.querySelector("#detailType"),
  detailMaturity: document.querySelector("#detailMaturity"),
  detailEvidence: document.querySelector("#detailEvidence"),
  detailBestFor: document.querySelector("#detailBestFor"),
  detailRisk: document.querySelector("#detailRisk"),
  detailGuardrail: document.querySelector("#detailGuardrail"),
  detailSource: document.querySelector("#detailSource"),
  projectInput: document.querySelector("#projectInput"),
  auditBtn: document.querySelector("#auditBtn"),
  exportBtn: document.querySelector("#exportBtn"),
  chatLog: document.querySelector("#chatLog")
};

function renderStages() {
  els.stageNav.innerHTML = stages.map((stage) => (
    `<button type="button" class="${stage === state.selectedStage ? "active" : ""}" data-stage="${stage}">${label(stage)}</button>`
  )).join("");
}

function label(value) {
  return value.charAt(0).toUpperCase() + value.slice(1);
}

function filteredTools() {
  const query = els.searchInput.value.trim().toLowerCase();
  const license = els.licenseFilter.value;
  return state.tools.filter((tool) => {
    const matchesStage = tool.stages.includes(state.selectedStage);
    const haystack = [tool.name, tool.type, tool.evidence, tool.bestFor, tool.risk, tool.guardrail].join(" ").toLowerCase();
    const matchesQuery = !query || haystack.includes(query);
    const matchesLicense = license === "all" ||
      (license === "open" && tool.license.toLowerCase().includes("mit")) ||
      (license === "closed" && !tool.license.toLowerCase().includes("mit"));
    return matchesStage && matchesQuery && matchesLicense;
  });
}

function renderTools() {
  const tools = filteredTools();
  els.catalogCount.textContent = `${tools.length} fuentes para ${state.selectedStage}`;
  els.toolList.innerHTML = tools.map((tool) => `
    <article class="tool-card ${state.selectedTool?.id === tool.id ? "selected" : ""}" data-id="${tool.id}">
      <div>
        <h3>${tool.name}</h3>
        <p>${tool.bestFor}</p>
        <div class="tag-row">
          ${tool.stages.map((stage) => `<span class="tag">${label(stage)}</span>`).join("")}
        </div>
      </div>
      <span class="tag">${tool.license.includes("MIT") ? "open" : "cerrada"}</span>
    </article>
  `).join("");

  if (!state.selectedTool && tools[0]) {
    selectTool(tools[0].id);
  }
}

function selectTool(id) {
  state.selectedTool = state.tools.find((tool) => tool.id === id) || null;
  renderDetail();
  renderTools();
}

function renderDetail() {
  const tool = state.selectedTool;
  if (!tool) return;
  els.detailName.textContent = tool.name;
  els.detailType.textContent = `${tool.type} · ${tool.license}`;
  els.detailMaturity.textContent = tool.maturity;
  els.detailEvidence.textContent = tool.evidence;
  els.detailBestFor.textContent = tool.bestFor;
  els.detailRisk.textContent = tool.risk;
  els.detailGuardrail.textContent = tool.guardrail;
  els.detailSource.href = tool.source;
}

function renderAudit(result) {
  els.chatLog.innerHTML = `
    <div class="chat-message">
      <strong>Veredicto:</strong> ${result.verdict}<br>
      <strong>Herramienta:</strong> ${result.selectedTool}<br>
      <strong>Resguardo:</strong> ${result.guardrail}
      ${result.warnings.length ? `<ul>${result.warnings.map((warning) => `<li>${warning}</li>`).join("")}</ul>` : ""}
    </div>
    <div class="chat-message">
      <strong>Preguntas que debe responder el investigador:</strong>
      <ul>${result.questions.map((question) => `<li>${question}</li>`).join("")}</ul>
    </div>
  `;
  state.lastExport = result.exportMarkdown;
}

async function auditSelection() {
  if (!state.selectedTool) return;
  const response = await fetch("/api/audit", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      toolId: state.selectedTool.id,
      stage: state.selectedStage,
      project: els.projectInput.value
    })
  });
  renderAudit(await response.json());
}

function exportFicha() {
  const content = state.lastExport || `# Ficha de seleccion IA\n\nSeleccion: ${state.selectedTool?.name || "pendiente"}`;
  const blob = new Blob([content], { type: "text/markdown" });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = "ficha-seleccion-ia.md";
  anchor.click();
  URL.revokeObjectURL(url);
}

async function init() {
  state.tools = await fetch("/api/tools").then((response) => response.json());
  renderStages();
  renderTools();
  auditSelection();
}

els.stageNav.addEventListener("click", (event) => {
  const button = event.target.closest("button[data-stage]");
  if (!button) return;
  state.selectedStage = button.dataset.stage;
  state.selectedTool = null;
  renderStages();
  renderTools();
});

els.toolList.addEventListener("click", (event) => {
  const card = event.target.closest(".tool-card");
  if (card) selectTool(card.dataset.id);
});

els.searchInput.addEventListener("input", renderTools);
els.licenseFilter.addEventListener("change", renderTools);
els.auditBtn.addEventListener("click", auditSelection);
els.exportBtn.addEventListener("click", exportFicha);

init();

