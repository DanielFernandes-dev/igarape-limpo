const CENTRO_INICIAL = [-3.059860, -60.040980];
const NIVEIS = {
    "Baixo": "#22c55e",
    "Medio": "#eab308",
    "Alto": "#ef4444",
};

const mapa = L.map("mapa").setView(CENTRO_INICIAL, 13);

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
}).addTo(mapa);

const cluster = L.markerClusterGroup({
    chunkedLoading: true,
    maxClusterRadius: 50,
});
mapa.addLayer(cluster);

async function carregarOcorrencias() {
    const params = construirFiltros();
    const url = new URL("/api/ocorrencias", window.location.origin);
    Object.entries(params).forEach(([k, v]) => {
        if (v !== "" && v !== null && v !== undefined) {
            url.searchParams.set(k, v);
        }
    });

    const resp = await fetch(url.toString());
    if (!resp.ok) {
        return;
    }
    const data = await resp.json();
    const ocorrencias = data.ocorrencias || [];
    renderizarOcorrencias(ocorrencias);
    renderizarResumo(ocorrencias);
    renderizarLista(ocorrencias);
}

function construirFiltros() {
    const tipo = (document.getElementById("f-tipo")?.value || "").trim();
    const nivel = (document.getElementById("f-nivel")?.value || "").trim();
    const pontoId = (document.getElementById("f-ponto")?.value || "").trim();
    const inicio = (document.getElementById("f-inicio")?.value || "").trim();
    const fim = (document.getElementById("f-fim")?.value || "").trim();
    const busca = (document.getElementById("f-busca")?.value || "").trim();
    const apenasCriticos = document.getElementById("f-criticos")?.checked;

    const filtros = {};
    if (tipo) filtros.tipo_residuo = tipo;
    if (nivel) filtros.nivel_acumulo = nivel;
    if (pontoId) filtros.ponto_id = pontoId;
    if (inicio) filtros.data_inicio = inicio;
    if (fim) filtros.data_fim = fim;
    if (busca) filtros.busca = busca;
    if (apenasCriticos) filtros.nivel_acumulo = "Alto";

    return filtros;
}

function renderizarOcorrencias(ocorrencias) {
    cluster.clearLayers();

    const camadas = ocorrencias.map((o) => {
        const cor = NIVEIS[o.nivel_acumulo] || "#64748b";
        const marcador = L.circleMarker([o.latitude, o.longitude], {
            radius: 9,
            color: cor,
            fillColor: cor,
            fillOpacity: 0.7,
            weight: 2,
        });
        marcador.bindPopup(criarPopup(o));
        marcador.on("click", () => {
            mapa.setView([o.latitude, o.longitude], 16);
        });
        return marcador;
    });

    cluster.addLayers(camadas);
}

function criarPopup(o) {
    const foto = o.fotografia
        ? `<img src="${o.fotografia}" alt="foto" style="width:100%;max-height:140px;object-fit:cover;border-radius:6px;margin-bottom:6px">`
        : "";
    const pontoLink = o.ponto_id
        ? `<br><a href="/ponto/${o.ponto_id}">Ver ponto monitorado</a>`
        : "";
    const historicoLink = o.ponto_id
        ? ` | <a href="/ponto/${o.ponto_id}">Histórico</a>`
        : "";
    return `
        <strong>Ocorrência #${String(o.id).padStart(3, "0")}</strong><br>
        ${foto}
        <b>Tipo:</b> ${o.tipo_residuo}<br>
        <b>Acúmulo:</b> ${o.nivel_acumulo}<br>
        <b>Data:</b> ${o.data_hora}<br>
        ${pontoLink}
        <a href="/ocorrencia/${o.id}">Ver detalhes</a>${historicoLink}
    `;
}

function renderizarResumo(ocorrencias) {
    document.getElementById("contador-ocorrencias").textContent = ocorrencias.length;

    const pontos = new Set(ocorrencias.map((o) => `${o.latitude.toFixed(4)},${o.longitude.toFixed(4)}`));
    document.getElementById("contador-pontos").textContent = pontos.size;

    const contagem = {};
    ocorrencias.forEach((o) => {
        contagem[o.tipo_residuo] = (contagem[o.tipo_residuo] || 0) + 1;
    });
    const maior = Object.entries(contagem).sort((a, b) => b[1] - a[1])[0];
    document.getElementById("maior-ocorrencia").textContent = maior ? maior[0] : "—";

    const criticos = ocorrencias.filter((o) => o.nivel_acumulo === "Alto").length;
    document.getElementById("pontos-criticos").textContent = criticos;
}

function renderizarLista(ocorrencias) {
    const lista = document.getElementById("lista");
    lista.innerHTML = ocorrencias.map((o) => `
        <li>
            <a href="/ocorrencia/${o.id}">Ocorrência #${String(o.id).padStart(3, "0")}</a>
            <span>${o.tipo_residuo} · ${o.nivel_acumulo} · ${o.data_hora}</span>
        </li>
    `).join("");
}

document.getElementById("form-filtros")?.addEventListener("submit", (e) => {
    e.preventDefault();
    carregarOcorrencias();
});

document.getElementById("btn-limpar-filtros")?.addEventListener("click", () => {
    document.getElementById("form-filtros").reset();
    carregarOcorrencias();
});

carregarOcorrencias();
