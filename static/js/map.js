const CENTRO_INICIAL = [-3.059860, -60.040980];
const NIVEIS = {
    "Baixo": "#22c55e",
    "Medio": "#eab308",
    "Alto": "#ef4444",
};

const mapa = L.map("mapa").setView(CENTRO_INICIAL, 15);

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
}).addTo(mapa);

async function carregarOcorrencias() {
    const resp = await fetch("/api/ocorrencias");
    const ocorrencias = await resp.json();
    renderizarOcorrencias(ocorrencias);
    renderizarResumo(ocorrencias);
    renderizarLista(ocorrencias);
}

function renderizarOcorrencias(ocorrencias) {
    ocorrencias.forEach((o) => {
        const cor = NIVEIS[o.nivel_acumulo] || "#64748b";
        const marcador = L.circleMarker([o.latitude, o.longitude], {
            radius: 9,
            color: cor,
            fillColor: cor,
            fillOpacity: 0.7,
            weight: 2,
        });
        marcador.bindPopup(criarPopup(o));
        marcador.addTo(mapa);
    });
}

function criarPopup(o) {
    const foto = o.fotografia
        ? `<img src="${o.fotografia}" alt="foto" style="width:100%;max-height:140px;object-fit:cover;border-radius:6px;margin-bottom:6px">`
        : "";
    return `
        <strong>Ocorrência #${String(o.id).padStart(3, "0")}</strong><br>
        ${foto}
        <b>Tipo:</b> ${o.tipo_residuo}<br>
        <b>Acúmulo:</b> ${o.nivel_acumulo}<br>
        <b>Data:</b> ${o.data_hora}<br>
        <a href="/ocorrencia/${o.id}">Ver detalhes</a>
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

carregarOcorrencias();
