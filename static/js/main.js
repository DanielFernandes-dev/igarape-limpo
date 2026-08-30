const mapa = L.map("mapa-form", { zoomControl: false }).setView([-3.059860, -60.040980], 15);
L.control.zoom({ position: "bottomright" }).addTo(mapa);
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", { maxZoom: 19, attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>' }).addTo(mapa);

let marcadorSelecionado = null;
function definirPonto(lat, lng) {
    document.getElementById("latitude").value = lat.toFixed(6);
    document.getElementById("longitude").value = lng.toFixed(6);
    if (marcadorSelecionado) marcadorSelecionado.setLatLng([lat, lng]);
    else marcadorSelecionado = L.marker([lat, lng]).addTo(mapa);
    mapa.setView([lat, lng], 16);
}

mapa.on("click", (e) => { definirPonto(e.latlng.lat, e.latlng.lng); mensagem("Ponto marcado manualmente.", "ok", document.getElementById("msg-localizacao")); });

document.getElementById("btn-localizar").addEventListener("click", (e) => {
    const botao = e.currentTarget;
    const msg = document.getElementById("msg-localizacao");
    if (!navigator.geolocation) { mensagem("Este navegador não oferece geolocalização. Marque o ponto no mapa.", "erro", msg); return; }
    botao.disabled = true; botao.textContent = "Localizando...";
    mensagem("Aguardando autorização de localização...", "ok", msg);
    navigator.geolocation.getCurrentPosition(
        ({ coords }) => {
            definirPonto(coords.latitude, coords.longitude);
            mensagem("Localização obtida. Confirme o ponto no mapa.", "ok", msg);
            botao.disabled = false; botao.textContent = "Usar minha localização";
        },
        (erro) => {
            const texto = erro.code === erro.PERMISSION_DENIED ? "Permissão de localização negada. Clique no mapa para marcar manualmente." : "Não foi possível obter a localização. Marque o ponto no mapa.";
            mensagem(texto, "erro", msg);
            botao.disabled = false; botao.textContent = "Usar minha localização";
        },
        { enableHighAccuracy: true, timeout: 10000 }
    );
});

document.getElementById("ponto_id")?.addEventListener("change", (e) => {
    const opt = e.target.selectedOptions[0];
    if (opt?.dataset.lat && opt?.dataset.lng) { definirPonto(parseFloat(opt.dataset.lat), parseFloat(opt.dataset.lng)); mensagem(`Ponto selecionado: ${opt.textContent}`, "ok", document.getElementById("msg-localizacao")); }
});

document.getElementById("fotografia")?.addEventListener("change", (e) => {
    const preview = document.getElementById("preview-foto");
    const arquivo = e.target.files[0];
    if (!arquivo) { preview.removeAttribute("src"); preview.classList.remove("visivel"); return; }
    preview.src = URL.createObjectURL(arquivo);
    preview.classList.add("visivel");
});

const form = document.getElementById("form-ocorrencia");
form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const msg = document.getElementById("msg-form");
    const botao = document.getElementById("btn-salvar");
    botao.disabled = true; botao.textContent = "Salvando registro...";
    mensagem("Enviando dados e validando a fotografia...", "ok", msg);
    try {
        const resp = await fetch("/api/ocorrencias", { method: "POST", body: new FormData(form) });
        const resultado = await resp.json();
        if (!resp.ok) { mensagem(resultado.erro || "Erro ao salvar ocorrência.", "erro", msg); return; }
        mensagem("Ocorrência salva. Abrindo o registro...", "ok", msg);
        window.location.href = resultado.url;
    } catch (erro) { mensagem("Não foi possível conectar ao servidor. Seus dados não foram enviados.", "erro", msg); }
    finally { botao.disabled = false; botao.textContent = "Salvar ocorrência"; }
});

function mensagem(texto, tipo, el) { el.textContent = texto; el.className = `msg ${tipo}`; }
