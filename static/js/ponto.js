const mapa = L.map("mapa-ponto", { zoomControl: false }).setView([ponto.lat, ponto.lng], 15);
L.control.zoom({ position: "bottomright" }).addTo(mapa);

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
}).addTo(mapa);

L.circleMarker([ponto.lat, ponto.lng], {
    radius: 10,
    color: "#ffffff",
    fillColor: "#14747b",
    fillOpacity: 0.92,
    weight: 3,
}).addTo(mapa).bindPopup("<strong>Ponto monitorado</strong><br><span>Referência do histórico</span>").openPopup();
