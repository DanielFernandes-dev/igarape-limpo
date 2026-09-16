const mapa = L.map("mapa-detalhe", { zoomControl: false }).setView([lat, lng], 16);
L.control.zoom({ position: "bottomright" }).addTo(mapa);

L.tileLayer("https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png", {
    maxZoom: 19,
    attribution: '&copy; OpenStreetMap &copy; CARTO',
}).addTo(mapa);

L.circleMarker([lat, lng], {
    radius: 10,
    color: "#ffffff",
    fillColor: cor,
    fillOpacity: 0.92,
    weight: 3,
}).addTo(mapa);
