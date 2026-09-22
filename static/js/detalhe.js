const mapa = L.map("mapa-detalhe", { zoomControl: false, attributionControl: false }).setView([lat, lng], 16);
L.control.zoom({ position: "bottomright" }).addTo(mapa);

L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution: '&copy; OpenStreetMap contributors',
}).addTo(mapa);

L.circleMarker([lat, lng], {
    radius: 10,
    color: "#ffffff",
    fillColor: cor,
    fillOpacity: 0.92,
    weight: 3,
}).addTo(mapa);
