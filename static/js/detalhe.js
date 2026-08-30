const mapa = L.map("mapa-detalhe").setView([lat, lng], 16);

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
}).addTo(mapa);

L.circleMarker([lat, lng], {
    radius: 10,
    color: cor,
    fillColor: cor,
    fillOpacity: 0.7,
    weight: 2,
}).addTo(mapa);
