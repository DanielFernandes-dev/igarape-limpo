const STATUS_OPERADOR = ["Nova", "Em analise", "Em atendimento", "Resolvida", "Descartada"];
let ocorrenciasOperador = [];

const fila = document.getElementById("operador-fila");
const mensagem = document.getElementById("operador-status");
const filtroStatus = document.getElementById("operador-filtro-status");

async function carregarFila() {
    mensagem.textContent = "Atualizando fila...";
    mensagem.className = "msg ok";
    try {
        const resposta = await fetch("/api/ocorrencias");
        if (!resposta.ok) throw new Error();
        ocorrenciasOperador = (await resposta.json()).ocorrencias;
        atualizarResumo();
        renderizarFila();
        mensagem.textContent = "Fila atualizada.";
    } catch (erro) {
        mensagem.textContent = "Não foi possível carregar a fila.";
        mensagem.className = "msg erro";
    }
}

function atualizarResumo() {
    const quantidade = (status) => ocorrenciasOperador.filter((item) => item.status === status).length;
    document.getElementById("operador-novas").textContent = quantidade("Nova");
    document.getElementById("operador-analise").textContent = quantidade("Em analise");
    document.getElementById("operador-atendimento").textContent = quantidade("Em atendimento");
    document.getElementById("operador-resolvidas").textContent = quantidade("Resolvida");
}

function renderizarFila() {
    const status = document.getElementById("operador-filtro-status").value;
    const nivel = document.getElementById("operador-filtro-nivel").value;
    const busca = document.getElementById("operador-filtro-busca").value.trim().toLowerCase();
    const ordem = document.getElementById("operador-filtro-ordem").value;
    const itens = ocorrenciasOperador.filter((item) => {
        const texto = `${item.local_nome || ""} ${item.ponto_nome || ""} ${item.tipo_residuo || ""}`.toLowerCase();
        return (status === "todos" || item.status === status) && (nivel === "todos" || item.nivel_acumulo === nivel) && (!busca || texto.includes(busca));
    });
    itens.sort((primeiro, segundo) => {
        const diferenca = dataNumerica(segundo) - dataNumerica(primeiro);
        if (ordem === "prioridade") return prioridade(segundo) - prioridade(primeiro) || diferenca;
        return ordem === "antigos" ? -diferenca : diferenca;
    });
    document.getElementById("operador-contador").textContent = `${itens.length} ${itens.length === 1 ? "registro" : "registros"}`;

    if (!itens.length) {
        fila.innerHTML = '<p class="estado-vazio">Nenhuma ocorrência corresponde aos filtros.</p>';
        return;
    }
    fila.innerHTML = itens.map((item) => `
        <article class="operador-item" style="--nivel-cor: ${item.cor || "var(--agua-700)"}">
            <div class="operador-item-principal">
                <div class="operador-item-linha">
                    <span class="operador-nivel">${escapeHtml(item.nivel_acumulo)}</span>
                    <span class="operador-status operador-status-${slug(item.status)}">${escapeHtml(rotuloStatus(item.status))}</span>
                </div>
                <h2>${escapeHtml(item.local_nome || item.ponto_nome || "Local não informado")}</h2>
                <p>${escapeHtml(item.tipo_residuo)} · ${escapeHtml(formatarData(item.data_hora))}</p>
            </div>
            <div class="operador-item-meta">
                <a href="/ocorrencia/${item.id}" class="voltar">Ver detalhes</a>
                <label>Atualizar status <select data-id="${item.id}" class="operador-status-select">${STATUS_OPERADOR.map((opcao) => `<option value="${opcao}" ${opcao === item.status ? "selected" : ""}>${rotuloStatus(opcao)}</option>`).join("")}</select></label>
            </div>
        </article>`).join("");
    fila.querySelectorAll(".operador-status-select").forEach((select) => select.addEventListener("change", atualizarStatus));
}

async function atualizarStatus(evento) {
    const select = evento.currentTarget;
    select.disabled = true;
    try {
        const resposta = await fetch(`/api/ocorrencias/${select.dataset.id}`, { method: "PATCH", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ status: select.value }) });
        if (!resposta.ok) throw new Error();
        const item = ocorrenciasOperador.find((ocorrencia) => String(ocorrencia.id) === select.dataset.id);
        if (item) item.status = select.value;
        atualizarResumo();
        renderizarFila();
        mensagem.textContent = "Status atualizado.";
    } catch (erro) {
        mensagem.textContent = "Não foi possível atualizar o status.";
        mensagem.className = "msg erro";
        select.disabled = false;
    }
}

function formatarData(valor) { return valor ? new Date(valor.replace(" ", "T")).toLocaleDateString("pt-BR") : "Data não informada"; }
function dataNumerica(item) { return item.data_hora ? new Date(item.data_hora.replace(" ", "T")).getTime() : 0; }
function prioridade(item) { return ({ Alto: 3, Medio: 2, Baixo: 1 }[item.nivel_acumulo] || 0) + (item.status === "Nova" ? 1 : 0); }
function slug(valor) { return String(valor || "").toLowerCase().replaceAll(" ", "-"); }
function rotuloStatus(valor) { return valor === "Em analise" ? "Em análise" : valor; }
function escapeHtml(valor) { return String(valor).replace(/[&<>'"]/g, (caractere) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;" }[caractere])); }

document.getElementById("operador-atualizar").addEventListener("click", carregarFila);
[...document.querySelectorAll("[data-filtro-status]")].forEach((botao) => botao.addEventListener("click", () => {
    filtroStatus.value = botao.dataset.filtroStatus;
    renderizarFila();
    document.querySelector(".operador-filtros").scrollIntoView({ behavior: "smooth", block: "start" });
}));
document.getElementById("operador-limpar").addEventListener("click", () => {
    filtroStatus.value = "todos";
    document.getElementById("operador-filtro-nivel").value = "todos";
    document.getElementById("operador-filtro-busca").value = "";
    document.getElementById("operador-filtro-ordem").value = "prioridade";
    renderizarFila();
});
["operador-filtro-status", "operador-filtro-nivel", "operador-filtro-busca", "operador-filtro-ordem"].forEach((id) => document.getElementById(id).addEventListener("input", renderizarFila));
carregarFila();