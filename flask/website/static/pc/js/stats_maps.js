const url = window.location.href;
const arr = url.split("/");
const result = arr[0] + "//" + arr[2];
const myIcon = L.icon({
    iconUrl: result + "/static/pc/assets/logo_bikeeper_without_text.png",
    iconSize: [40, 40],
    iconAnchor: [25, 50],
    popupAnchor: [-3, -76],
});


const lat = 47.902964;
const lon = 1.909251;

const mymap = L.map('my_osm_widget_map', { /* use the same name as your <div id=""> */
    center: [lat, lon],
    zoom: 17,
    zoomControl: true,
    icon: myIcon,
    scrollWheelZoom: true
});

const EXTERNAL_SERVER = 'https://{s}.tile.openstreetmap.fr/osmfr/{z}/{x}/{y}.png'
const LOCAL_SERVER = 'http://thegostisdead.dynns.com:8589/styles/osm-bright/{z}/{x}/{y}.png'

$('input[type=radio][name=localonline]').change(function () {
    selectServer();
});

function selectServer() {
    let a = $("input:checked")

    if (a[0].id === "online") {
 console.log("Button offline clicked !")
        let layer = L.geoJson();
        layer.clearLayers(); // inherited from LayerGroup

        L.tileLayer(LOCAL_SERVER, { /* set your personal MapBox Access Token */
            maxZoom: 20, /* zoom limit of the map */
            attribution: 'Données &copy; Contributeurs <a href="http://openstreetmap.org">OpenStreetMap</a> + ' +
                '<a href="http://mapbox.com">Mapbox</a> | ' +
                '<a href="https://creativecommons.org/licenses/by/2.0/">CC-BY</a> ' +
                'Offline MAP', /* set the map's caption */
            id: 'mapbox.streets' /* mapbox.light / dark / streets / outdoors / satellite */
        }).addTo(mymap);
    } else {
        let layer = L.geoJson();
        layer.clearLayers();
        console.log("Button online clicked !")
        L.tileLayer(EXTERNAL_SERVER, { /* set your personal MapBox Access Token */
            maxZoom: 20, /* zoom limit of the map */
            attribution: 'Données &copy; Contributeurs <a href="http://openstreetmap.org">OpenStreetMap</a> + ' +
                '<a href="http://mapbox.com">Mapbox</a> | ' +
                '<a href="https://creativecommons.org/licenses/by/2.0/">CC-BY</a> ' +
                'Online MAP', /* set the map's caption */
            id: 'mapbox.streets' /* mapbox.light / dark / streets / outdoors / satellite */
        }).addTo(mymap);
    }

}

L.tileLayer(LOCAL_SERVER, { /* set your personal MapBox Access Token */
    maxZoom: 20, /* zoom limit of the map */
    attribution: 'Données &copy; Contributeurs <a href="http://openstreetmap.org">OpenStreetMap</a> + ' +
        '<a href="http://mapbox.com">Mapbox</a> | ' +
        '<a href="https://creativecommons.org/licenses/by/2.0/">CC-BY</a> ' +
        'Guillaume Rouan 2016', /* set the map's caption */
    id: 'mapbox.streets' /* mapbox.light / dark / streets / outdoors / satellite */
}).addTo(mymap);

L.marker([lat, lon], {
    icon: myIcon
}).addTo(mymap); /* set your location's GPS Coordinates : [LAT,LON] */
