const mapa = L.map("mapa-ponto", { zoomControl: false }).setView([ponto.lat, ponto.lng], 15);
L.control.zoom({ position: "bottomright" }).addTo(mapa);

L.tileLayer("https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png", {
    maxZoom: 19,
    attribution: '&copy; OpenStreetMap &copy; CARTO',
}).addTo(mapa);

L.circleMarker([ponto.lat, ponto.lng], {
    radius: 10,
    color: "#ffffff",
    fillColor: "#94d4b2",
    fillOpacity: 0.92,
    weight: 3,
}).addTo(mapa).bindPopup("<strong>Ponto monitorado</strong><br><span>Referência do histórico</span>").openPopup();
