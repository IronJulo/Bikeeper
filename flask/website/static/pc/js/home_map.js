const getLatLon = async () => {
    let response = await fetch('/api/bikeeper/get_last_log_position/' + selected_device);
    let last_log = await response.json();
    console.log(last_log);
    if (last_log.response !== "None"){
        let content = JSON.parse(last_log.content_log);
        let lat = content.latitude;
        let lon = content.longitude;
        return [lat, lon];
    } else {
        throw new Error()
    }
}

// Fonction d'initialisation de la carte
async function initMap() {

    try {
        let latlon = await getLatLon();
        let lat = latlon[0];
        let lon = latlon[1];

        let macarte = L.map('map').setView([lat, lon], 11);

        L.tileLayer('https://{s}.tile.openstreetmap.fr/osmfr/{z}/{x}/{y}.png', {

            attribution: 'données © <a href="//osm.org/copyright">OpenStreetMap</a>/ODbL - rendu <a href="//openstreetmap.fr">OSM France</a>',
            minZoom: 1,
            maxZoom: 20
        }).addTo(macarte);
        let marker = L.marker([lat, lon]).addTo(macarte);
    } catch (error) {
        console.log("no information on last device location");
        console.log("Error : "+error);
    }
}

window.onload = function () {
    // Fonction d'initialisation qui s'exécute lorsque le DOM est chargé
    initMap();
};
