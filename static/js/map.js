const CENTRO_INICIAL = [-3.059860, -60.040980];
const NIVEIS = { Baixo: "#22c55e", Medio: "#eab308", Alto: "#ef4444" };
const mapa = L.map("mapa", { zoomControl: false }).setView(CENTRO_INICIAL, 13);

L.control.zoom({ position: "bottomright" }).addTo(mapa);
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
}).addTo(mapa);

const cluster = L.markerClusterGroup({ chunkedLoading: true, maxClusterRadius: 48, showCoverageOnHover: false });
mapa.addLayer(cluster);

async function carregarOcorrencias() {
    const form = document.getElementById("form-filtros");
    const botao = form?.querySelector('button[type="submit"]');
    const status = document.getElementById("resultado-filtros");
    const params = construirFiltros();
    const url = new URL("/api/ocorrencias", window.location.origin);
    Object.entries(params).forEach(([chave, valor]) => url.searchParams.set(chave, valor));
    atualizarExportacoes(url.searchParams);

    if (botao) { botao.disabled = true; botao.textContent = "Atualizando..."; }
    if (status) status.textContent = "Consultando ocorrências...";

    try {
        const resp = await fetch(url.toString());
        const data = await resp.json();
        if (!resp.ok) throw new Error(data.erro || "Não foi possível carregar os dados.");
        const ocorrencias = data.ocorrencias || [];
        renderizarOcorrencias(ocorrencias);
        renderizarResumo(ocorrencias);
        renderizarLista(ocorrencias);
        if (status) status.textContent = `${ocorrencias.length} ${ocorrencias.length === 1 ? "ocorrência encontrada" : "ocorrências encontradas"}.`;
    } catch (erro) {
        cluster.clearLayers();
        renderizarLista([]);
        if (status) status.textContent = erro.message || "Falha ao carregar as ocorrências.";
    } finally {
        if (botao) { botao.disabled = false; botao.textContent = "Aplicar filtros"; }
    }
}

function construirFiltros() {
    const valor = (id) => (document.getElementById(id)?.value || "").trim();
    const filtros = {};
    if (valor("f-tipo")) filtros.tipo_residuo = valor("f-tipo");
    if (valor("f-nivel")) filtros.nivel_acumulo = valor("f-nivel");
    if (valor("f-ponto")) filtros.ponto_id = valor("f-ponto");
    if (valor("f-inicio")) filtros.data_inicio = valor("f-inicio");
    if (valor("f-fim")) filtros.data_fim = valor("f-fim");
    if (valor("f-busca")) filtros.busca = valor("f-busca");
    if (document.getElementById("f-criticos")?.checked) filtros.nivel_acumulo = "Alto";
    return filtros;
}

function atualizarExportacoes(params) {
    const query = params.toString();
    const sufixo = query ? `?${query}` : "";
    document.getElementById("exportar-csv").href = `/api/export/ocorrencias.csv${sufixo}`;
    document.getElementById("exportar-geojson").href = `/api/export/ocorrencias.geojson${sufixo}`;
}

function renderizarOcorrencias(ocorrencias) {
    cluster.clearLayers();
    const camadas = ocorrencias.map((o) => {
        const cor = NIVEIS[o.nivel_acumulo] || "#64748b";
        const marcador = L.circleMarker([o.latitude, o.longitude], { radius: 9, color: "#fff", fillColor: cor, fillOpacity: .92, weight: 3 });
        marcador.bindPopup(criarPopup(o), { maxWidth: 270 });
        marcador.on("click", () => mapa.setView([o.latitude, o.longitude], Math.max(mapa.getZoom(), 15)));
        return marcador;
    });
    cluster.addLayers(camadas);
}

function criarPopup(o) {
    const id = Number(o.id);
    const pontoId = o.ponto_id ? Number(o.ponto_id) : null;
    const foto = o.fotografia ? `<img src="${escapeHtml(o.fotografia)}" alt="Fotografia da ocorrência ${id}" style="width:100%;height:125px;object-fit:cover;border-radius:10px;margin-bottom:8px">` : "";
    const ponto = pontoId ? `<a href="/ponto/${pontoId}">Histórico do ponto</a>` : "";
    return `<div class="popup-ocorrencia">${foto}<small>OCORRÊNCIA #${String(id).padStart(3, "0")}</small><strong style="display:block;margin:3px 0 7px">${escapeHtml(o.local_nome || o.tipo_residuo)}</strong><span>${escapeHtml(o.tipo_residuo)} · ${escapeHtml(o.nivel_acumulo)}</span><br><span>${escapeHtml(formatarData(o.data_hora))}</span><div style="display:flex;gap:10px;margin-top:9px"><a href="/ocorrencia/${id}">Ver detalhes</a>${ponto}</div></div>`;
}

function renderizarResumo(ocorrencias) {
    document.getElementById("contador-ocorrencias").textContent = ocorrencias.length;
    const pontos = new Set(ocorrencias.map((o) => o.ponto_id || `${Number(o.latitude).toFixed(4)},${Number(o.longitude).toFixed(4)}`));
    document.getElementById("contador-pontos").textContent = pontos.size;
    const contagem = {};
    ocorrencias.forEach((o) => { contagem[o.tipo_residuo] = (contagem[o.tipo_residuo] || 0) + 1; });
    const maior = Object.entries(contagem).sort((a, b) => b[1] - a[1])[0];
    document.getElementById("maior-ocorrencia").textContent = maior ? maior[0] : "—";
    document.getElementById("pontos-criticos").textContent = ocorrencias.filter((o) => o.nivel_acumulo === "Alto").length;
}

function renderizarLista(ocorrencias) {
    const lista = document.getElementById("lista");
    lista.replaceChildren();
    if (!ocorrencias.length) {
        const vazio = document.createElement("li");
        vazio.className = "estado-vazio";
        vazio.textContent = "Nenhuma ocorrência corresponde aos filtros selecionados.";
        lista.appendChild(vazio);
        return;
    }
    ocorrencias.forEach((o) => {
        const item = document.createElement("li");
        const link = document.createElement("a");
        link.href = `/ocorrencia/${Number(o.id)}`;
        link.textContent = `Ocorrência #${String(o.id).padStart(3, "0")}`;
        const meta = document.createElement("span");
        meta.textContent = `${o.tipo_residuo} · ${o.nivel_acumulo} · ${formatarData(o.data_hora)}`;
        item.append(link, meta);
        lista.appendChild(item);
    });
}

function formatarData(valor) {
    if (!valor) return "Data não informada";
    const data = new Date(valor.replace(" ", "T"));
    return Number.isNaN(data.getTime()) ? valor : new Intl.DateTimeFormat("pt-BR", { dateStyle: "short", timeStyle: "short" }).format(data);
}

function escapeHtml(valor) {
    return String(valor).replace(/[&<>'"]/g, (caractere) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;" }[caractere]));
}

document.getElementById("form-filtros")?.addEventListener("submit", (e) => { e.preventDefault(); carregarOcorrencias(); });
document.getElementById("btn-limpar-filtros")?.addEventListener("click", () => { document.getElementById("form-filtros").reset(); carregarOcorrencias(); });
carregarOcorrencias();
