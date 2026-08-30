const COR_TIPOS = "#0e7490";
const CORES_NIVEL = ["#22c55e", "#eab308", "#ef4444"];

async function carregarResumo() {
    const resp = await fetch("/api/dashboard/resumo");
    const r = await resp.json();

    set("d-total-ocorrencias", r.total_ocorrencias);
    set("d-7dias", r.ultimos_7_dias);
    set("d-30dias", r.ultimos_30_dias);
    set("d-pontos-ativos", r.pontos_ativos);
    set("d-pontos-criticos", r.pontos_criticos);
    set("d-residuo", r.residuo_mais_frequente || "—");
    set("d-local", r.local_maior_ocorrencia ? `${r.local_maior_ocorrencia.nome} (${r.local_maior_ocorrencia.quantidade})` : "—");
    set("d-recorrentes", r.ocorrencias_recorrentes);

    graficoBarras("grafico-tipo", "Tipo de resíduo", r.por_tipo, COR_TIPOS);
    graficoPizza("grafico-nivel", r.por_nivel, CORES_NIVEL);
}

async function carregarEvolucao() {
    const resp = await fetch("/api/dashboard/series?dias=30");
    const s = await resp.json();
    const labels = s.pontos.map((p) => p.data.slice(5));
    const valores = s.pontos.map((p) => p.quantidade);
    graficoLinha("grafico-evolucao", labels, valores);
}

async function carregarRanking() {
    const resp = await fetch("/api/dashboard/ranking?limite=8");
    const dados = await resp.json();
    const nomes = dados.ranking.map((r) => r.nome).reverse();
    const valores = dados.ranking.map((r) => r.quantidade).reverse();
    graficoBarrasHorizontal("grafico-ranking", nomes, valores);
}

function set(id, valor) {
    document.getElementById(id).textContent = valor;
}

function graficoBarras(id, rotulo, dados, cor) {
    const chaves = Object.keys(dados);
    const valores = Object.values(dados);
    new Chart(document.getElementById(id), {
        type: "bar",
        data: {
            labels: chaves,
            datasets: [{
                label: rotulo,
                data: valores,
                backgroundColor: cor,
                borderRadius: 6,
            }],
        },
        options: { plugins: { legend: { display: false } } },
    });
}

function graficoPizza(id, dados, cores) {
    const chaves = Object.keys(dados);
    const valores = Object.values(dados);
    new Chart(document.getElementById(id), {
        type: "doughnut",
        data: {
            labels: chaves,
            datasets: [{ data: valores, backgroundColor: cores }],
        },
    });
}

function graficoLinha(id, labels, valores) {
    new Chart(document.getElementById(id), {
        type: "line",
        data: {
            labels: labels,
            datasets: [{
                label: "Ocorrências",
                data: valores,
                borderColor: "#0e7490",
                backgroundColor: "rgba(14,116,144,0.15)",
                fill: true,
                tension: 0.3,
            }],
        },
        options: { plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true, ticks: { precision: 0 } } } },
    });
}

function graficoBarrasHorizontal(id, labels, valores) {
    new Chart(document.getElementById(id), {
        type: "bar",
        data: {
            labels: labels,
            datasets: [{
                label: "Ocorrências",
                data: valores,
                backgroundColor: "#ef4444",
                borderRadius: 6,
            }],
        },
        options: { indexAxis: "y", plugins: { legend: { display: false } }, scales: { x: { beginAtZero: true, ticks: { precision: 0 } } } },
    });
}

carregarResumo();
carregarEvolucao();
carregarRanking();
