const mapa = L.map("mapa-form").setView([-3.059860, -60.040980], 15);

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
}).addTo(mapa);

let marcadorSelecionado = null;

function definirPonto(lat, lng) {
    document.getElementById("latitude").value = lat.toFixed(6);
    document.getElementById("longitude").value = lng.toFixed(6);
    atualizarMarcador(lat, lng);
}

function atualizarMarcador(lat, lng) {
    if (marcadorSelecionado) {
        marcadorSelecionado.setLatLng([lat, lng]);
    } else {
        marcadorSelecionado = L.marker([lat, lng]).addTo(mapa);
    }
    mapa.setView([lat, lng], 16);
}

mapa.on("click", (e) => {
    definirPonto(e.latlng.lat, e.latlng.lng);
    mensagem("Ponto marcado manualmente.", "ok");
});

document.getElementById("btn-localizar").addEventListener("click", () => {
    const msg = document.getElementById("msg-localizacao");
    if (!navigator.geolocation) {
        mensagem("Geolocalização não suportada neste navegador.", "erro", msg);
        return;
    }
    mensagem("Buscando sua localização...", "ok", msg);
    navigator.geolocation.getCurrentPosition(
        (pos) => {
            const { latitude, longitude } = pos.coords;
            definirPonto(latitude, longitude);
            mensagem("Localização obtida com sucesso.", "ok", msg);
        },
        () => {
            mensagem("Não foi possível obter a localização. Clique no mapa para marcar o ponto.", "erro", msg);
        },
        { enableHighAccuracy: true, timeout: 10000 }
    );
});

document.getElementById("ponto_id")?.addEventListener("change", (e) => {
    const opt = e.target.selectedOptions[0];
    if (opt && opt.dataset.lat && opt.dataset.lng) {
        const lat = parseFloat(opt.dataset.lat);
        const lng = parseFloat(opt.dataset.lng);
        definirPonto(lat, lng);
        mensagem(`Ponto monitorado selecionado: ${opt.textContent}`, "ok");
    }
});

const form = document.getElementById("form-ocorrencia");
form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const msg = document.getElementById("msg-form");
    mensagem("Enviando...", "ok", msg);

    const dados = new FormData(form);
    try {
        const resp = await fetch("/api/ocorrencias", {
            method: "POST",
            body: dados,
        });
        const resultado = await resp.json();
        if (!resp.ok) {
            mensagem(resultado.erro || "Erro ao salvar ocorrência.", "erro", msg);
            return;
        }
        mensagem("Ocorrência salva com sucesso!", "ok", msg);
        form.reset();
        if (marcadorSelecionado) {
            mapa.removeLayer(marcadorSelecionado);
            marcadorSelecionado = null;
        }
        setTimeout(() => {
            window.location.href = resultado.url;
        }, 800);
    } catch (erro) {
        mensagem("Erro de conexão ao salvar ocorrência.", "erro", msg);
    }
});

function mensagem(texto, tipo, el) {
    (el || document.getElementById("msg-form")).textContent = texto;
    (el || document.getElementById("msg-form")).className = "msg " + tipo;
}
