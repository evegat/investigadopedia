const http = require("http");
const fs = require("fs");
const path = require("path");

const root = __dirname;
const port = process.env.PORT || 4177;

function readJson(relativePath) {
  return JSON.parse(fs.readFileSync(path.join(root, relativePath), "utf8"));
}

function send(res, status, body, contentType = "application/json; charset=utf-8") {
  res.writeHead(status, {
    "Content-Type": contentType,
    "Cache-Control": "no-store"
  });
  res.end(body);
}

function auditSelection(payload) {
  const tools = readJson("data/tools.json");
  const selected = tools.find((tool) => tool.id === payload.toolId) || tools[0];
  const stage = payload.stage || "literatura";
  const project = (payload.project || "").trim();
  const missingProject = project.length < 40;

  const warnings = [];
  if (missingProject) {
    warnings.push("La descripcion del proyecto aun es demasiado breve para decidir herramienta con seguridad.");
  }
  if (!selected.stages.includes(stage)) {
    warnings.push(`La herramienta seleccionada no esta clasificada como apoyo principal para la etapa ${stage}.`);
  }
  if (selected.license.includes("cerrada")) {
    warnings.push("Hay dependencia de una plataforma cerrada; documenta terminos, privacidad y posibilidad de reproducir resultados.");
  }

  return {
    selectedTool: selected.name,
    stage,
    verdict: warnings.length ? "usar con resguardos" : "uso razonable para piloto",
    questions: [
      "Que decision metodologica tomara el investigador despues de usar esta herramienta?",
      "Que fuente primaria verificara manualmente antes de citar o concluir?",
      "Que quedara registrado en la ficha de trazabilidad?"
    ],
    warnings,
    guardrail: selected.guardrail,
    exportMarkdown: [
      `# Ficha de seleccion IA - ${selected.name}`,
      "",
      `## Etapa`,
      stage,
      "",
      "## Proyecto",
      project || "Pendiente de describir.",
      "",
      "## Veredicto",
      warnings.length ? "Usar con resguardos. No delegar conclusion ni citas." : "Uso razonable para piloto, con validacion humana.",
      "",
      "## Resguardo requerido",
      selected.guardrail,
      "",
      "## Preguntas de auditoria",
      "- Que decision metodologica tomara el investigador?",
      "- Que evidencia sera verificada manualmente?",
      "- Que decision quedara registrada?"
    ].join("\n")
  };
}

function serveStatic(req, res) {
  const requestPath = req.url === "/" ? "/index.html" : req.url.split("?")[0];
  const filePath = path.normalize(path.join(root, requestPath));
  if (!filePath.startsWith(root)) {
    send(res, 403, "Forbidden", "text/plain; charset=utf-8");
    return;
  }

  fs.readFile(filePath, (err, data) => {
    if (err) {
      send(res, 404, "Not found", "text/plain; charset=utf-8");
      return;
    }
    const ext = path.extname(filePath).toLowerCase();
    const types = {
      ".html": "text/html; charset=utf-8",
      ".css": "text/css; charset=utf-8",
      ".js": "text/javascript; charset=utf-8",
      ".json": "application/json; charset=utf-8"
    };
    send(res, 200, data, types[ext] || "application/octet-stream");
  });
}

const server = http.createServer((req, res) => {
  if (req.url === "/api/tools") {
    send(res, 200, JSON.stringify(readJson("data/tools.json")));
    return;
  }

  if (req.url === "/api/audit" && req.method === "POST") {
    let body = "";
    req.on("data", (chunk) => {
      body += chunk;
    });
    req.on("end", () => {
      try {
        send(res, 200, JSON.stringify(auditSelection(JSON.parse(body || "{}"))));
      } catch (error) {
        send(res, 400, JSON.stringify({ error: error.message }));
      }
    });
    return;
  }

  serveStatic(req, res);
});

server.listen(port, () => {
  console.log(`Investigadopedia Observatorio disponible en http://localhost:${port}`);
});

