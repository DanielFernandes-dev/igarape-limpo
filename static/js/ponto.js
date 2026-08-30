const mapa = L.map("mapa-ponto").setView([ponto.lat, ponto.lng], 15);

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
}).addTo(mapa);

L.circleMarker([ponto.lat, ponto.lng], {
    radius: 10,
    color: "#0e7490",
    fillColor: "#0e7490",
    fillOpacity: 0.7,
    weight: 2,
}).addTo(mapa).bindPopup("<strong>Ponto monitorado</strong>").openPopup();
