const mapa = L.map("mapa-detalhe", { zoomControl: false }).setView([lat, lng], 16);
L.control.zoom({ position: "bottomright" }).addTo(mapa);

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
}).addTo(mapa);

L.circleMarker([lat, lng], {
    radius: 10,
    color: "#ffffff",
    fillColor: cor,
    fillOpacity: 0.92,
    weight: 3,
}).addTo(mapa);
