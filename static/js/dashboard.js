const COR_TIPOS = ["#195343", "#14747b", "#b85f3d", "#6f9271", "#4f7684", "#a47b58", "#71817c"];
const CORES_NIVEL = ["#4aa86b", "#e1a93b", "#cf5d49"];
const status = document.getElementById("dashboard-status");

async function carregarDashboard() {
    status.textContent = "Atualizando indicadores...";
    status.className = "msg ok";
    try {
        const [resumoResp, serieResp, rankingResp] = await Promise.all([
            fetch("/api/dashboard/resumo"), fetch("/api/dashboard/series?dias=30"), fetch("/api/dashboard/ranking?limite=8")
        ]);
        if (!resumoResp.ok || !serieResp.ok || !rankingResp.ok) throw new Error();
        const [r, s, dados] = await Promise.all([resumoResp.json(), serieResp.json(), rankingResp.json()]);

        set("d-total-ocorrencias", r.total_ocorrencias); set("d-7dias", r.ultimos_7_dias); set("d-30dias", r.ultimos_30_dias);
        set("d-pontos-ativos", r.pontos_ativos); set("d-pontos-criticos", r.pontos_criticos); set("d-residuo", r.residuo_mais_frequente || "—");
        set("d-local", r.local_maior_ocorrencia ? `${r.local_maior_ocorrencia.nome} (${r.local_maior_ocorrencia.quantidade})` : "—");
        set("d-recorrentes", r.ocorrencias_recorrentes);

        graficoBarras("grafico-tipo", r.por_tipo); graficoPizza("grafico-nivel", r.por_nivel);
        graficoLinha("grafico-evolucao", s.pontos.map((p) => p.data.slice(5)), s.pontos.map((p) => p.quantidade));
        graficoRanking("grafico-ranking", dados.ranking.map((item) => item.nome).reverse(), dados.ranking.map((item) => item.quantidade).reverse());
        status.textContent = "Indicadores atualizados com os dados mais recentes.";
    } catch (erro) { status.textContent = "Não foi possível carregar o dashboard. Tente atualizar a página."; status.className = "msg erro"; }
}

function set(id, valor) { document.getElementById(id).textContent = valor; }
const opcoesBase = { responsive: true, maintainAspectRatio: false, plugins: { legend: { labels: { color: "#5f716c", font: { family: "Manrope" } } } }, scales: { x: { grid: { display: false }, ticks: { color: "#5f716c" } }, y: { beginAtZero: true, grid: { color: "rgba(23,50,45,.07)" }, ticks: { precision: 0, color: "#5f716c" } } } };

function graficoBarras(id, dados) { new Chart(document.getElementById(id), { type: "bar", data: { labels: Object.keys(dados), datasets: [{ data: Object.values(dados), backgroundColor: COR_TIPOS, borderRadius: 7 }] }, options: { ...opcoesBase, plugins: { legend: { display: false } } } }); }
function graficoPizza(id, dados) { new Chart(document.getElementById(id), { type: "doughnut", data: { labels: Object.keys(dados), datasets: [{ data: Object.values(dados), backgroundColor: CORES_NIVEL, borderWidth: 0 }] }, options: { responsive: true, maintainAspectRatio: false, cutout: "68%", plugins: opcoesBase.plugins } }); }
function graficoLinha(id, labels, valores) { new Chart(document.getElementById(id), { type: "line", data: { labels, datasets: [{ data: valores, borderColor: "#14747b", backgroundColor: "rgba(46,156,160,.12)", fill: true, tension: .35, pointRadius: 2 }] }, options: { ...opcoesBase, plugins: { legend: { display: false } } } }); }
function graficoRanking(id, labels, valores) { new Chart(document.getElementById(id), { type: "bar", data: { labels, datasets: [{ data: valores, backgroundColor: "#b85f3d", borderRadius: 7 }] }, options: { ...opcoesBase, indexAxis: "y", plugins: { legend: { display: false } } } }); }

carregarDashboard();
