const getLatLon = async () => {
    let response = await fetch('/api/bikeeper/get_last_log_position/' + selected_device);
    let last_log = await response.json();
    let content = JSON.parse(last_log.content_log);
    let lat = content.latitude;
    let lon = content.longitude;
    return [lat, lon];
}

// Fonction d'initialisation de la carte
async function initMap() {

    let latlon = await getLatLon();
    let lat = latlon[0];
    let lon = latlon[1];
    // Créer l'objet "macarte" et l'insèrer dans l'élément HTML qui a l'ID "map"
    let macarte = L.map('map').setView([lat, lon], 11);
    // Leaflet ne récupère pas les cartes (tiles) sur un serveur par défaut. Nous devons lui préciser où nous souhaitons les récupérer. Ici, openstreetmap.fr
    //L.tileLayer('http://167.71.142.2:8080/styles/klokantech-basic/{z}/{x}/{y}.png', {
    L.tileLayer('https://{s}.tile.openstreetmap.fr/osmfr/{z}/{x}/{y}.png', {
        // Il est toujours bien de laisser le lien vers la source des données
        attribution: 'données © <a href="//osm.org/copyright">OpenStreetMap</a>/ODbL - rendu <a href="//openstreetmap.fr">OSM France</a>',
        minZoom: 1,
        maxZoom: 20
    }).addTo(macarte);
    let marker = L.marker([lat, lon]).addTo(macarte);
}

window.onload = function () {
    // Fonction d'initialisation qui s'exécute lorsque le DOM est chargé
    initMap();
};
