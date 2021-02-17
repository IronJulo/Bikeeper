let ctx = document.getElementById('angle').getContext('2d');

const gradientStroke = ctx.createLinearGradient(0, 20, 0, screen.height / 2.45);
gradientStroke.addColorStop(0, "#FF4500");
gradientStroke.addColorStop(0.30, "#FFFF00");
gradientStroke.addColorStop(0.5, "#00FF00");
gradientStroke.addColorStop(0.70, "#FFFF00");
gradientStroke.addColorStop(1, "#FF4500");
var myChart = new Chart(ctx, {
    type: 'line',
    title: 'Angle',
    data: {
        labels: ['Text', 'Text', 'Text', 'Text', 'Text', 'Text', 'Text', 'Text', 'Text', 'Text'],
        datasets: [{
            label: 'Hard',
            data: [12, 19, -45, 25, -15, 3, 28, 52, -25, 48, -13, -3, 15, 34, 52, 28, -14, -33, 0, 42],
            backgroundColor: gradientStroke,
            borderWidth: 1
        },
            {
                label: "Medium",
                backgroundColor: "rgba(255,255,0,1)"
            },
            {
                label: "Easy",
                backgroundColor: "rgba(0,255,0,1)"
            }]
    },
    options: {
        scales: {
            yAxes: [{
                scaleLabel: {
                    display: true,
                    labelString: 'Droite                                    Gauche'
                },
                ticks: {
                    beginAtZero: true
                },

            }]
        },
        elements: {
            point: {
                radius: 0
            }
        }
    }
});

ctx = document.getElementById('speed').getContext('2d');
var myChart = new Chart(ctx, {
    type: 'line',
    title: 'Speed',
    data: {
        labels: ['Text', 'Text', 'Text', 'Text', 'Text', 'Text', 'Text', 'Text', 'Text', 'Text', 'Text', 'Text', 'Text', 'Text', 'Text', 'Text', 'Text', 'Text', 'Text', 'Text',],
        datasets: [{
            fill: false,
            label: 'speed',
            data: [12, 19, 3, 5, 2, 3, 28, 52, -25, 48, -13, -3, 15, 34, 52, 28, -14, -33, 0, 42],
            borderColor: ['rgba(135,206,235,1)'],
            pointBackgroundColor: ['rgba(135,206,235,1)', 'rgba(135,206,235,1)', 'rgba(135,206,235,1)', 'rgba(135,206,235,1)', 'rgba(135,206,235,1)', 'rgba(135,206,235,1)', 'rgba(135,206,235,1)', 'rgba(135,206,235,1)', 'rgba(135,206,235,1)', 'rgba(135,206,235,1)', 'rgba(135,206,235,1)', 'rgba(135,206,235,1)', 'rgba(135,206,235,1)', 'rgba(135,206,235,1)', 'rgba(135,206,235,1)', 'rgba(135,206,235,1)', 'rgba(135,206,235,1)', 'rgba(135,206,235,1)', 'rgba(135,206,235,1)', 'rgba(135,206,235,1)',],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }]
        }
    }
});

let rides = null;
let logs = null;


const loadDateBikeepers = async () => { // updates the others fields to show the devices that have been used at this date
    let date = document.getElementById('ride-date').value;
    const response = await fetch('/api/bikeeper/get_rides_bikeeper_from_user_at_time/' + username_stats + "/" + date);
    const devices = await response.json();
    let form_device_number = document.getElementById('device-number');
    reset_form_by_id('device-number');
    reset_form_by_id('ride-number');
    for (let device of devices) {
        let node = document.createElement("option");
        const response = await fetch('/api/bikeeper/get_bikeer_name_by_id/' + device);
        const device_name = await response.json();
        node.appendChild(document.createTextNode(device_name))
        node.value = device;
        form_device_number.appendChild(node);
    }
    if (devices.length !== 0) {
        await loadRides();
    }
}

const loadRides = async () => { // updates the field "rides" to show rides of a certain device and date
    let date = document.getElementById('ride-date').value;
    let bikeeper = document.getElementById('device-number').value;
    const response_logs = await fetch('/api/bikeeper/get_logs_at_date/' + bikeeper + "/" + date);
    logs = await response_logs.json();
    const response = await fetch('/api/bikeeper/get_rides_from_user_at_time_with_bikeeper/' + username_stats + "/" + bikeeper + "/" + date);
    rides = await response.json();
    console.log(rides);
    reset_form_by_id('ride-number');
    let form_ride_number = document.getElementById('ride-number');
    for (let i = 0; i < rides.length; i++) {
        let node = document.createElement("option");
        node.appendChild(document.createTextNode("Ride " + i))
        node.value = i.toString();
        form_ride_number.appendChild(node);
    }
    if (form_ride_number.value !== "") {
        await drawTrack();
    }
}

function reset_form_by_id(name) {
    let form = document.getElementById(name);
    while (form.firstChild) {
        form.removeChild(form.lastChild);
    }
}

document.getElementById('ride-date').value = new Date().toJSON().slice(0, 10); // setting todays date by default
loadDateBikeepers();

const url = window.location.href;
const arr = url.split("/");
const result = arr[0] + "//" + arr[2];
const myIcon = L.icon({
    iconUrl: result + "/static/pc/assets/logo_bikeeper_without_text.png",
    iconSize: [40, 40],
    iconAnchor: [25, 50],
    popupAnchor: [-3, -76],
});


// On initialise la latitude et la longitude de Paris (centre de la carte)
const lat = 47.902964;
const lon = 1.909251;

const mymap = L.map('my_osm_widget_map', { /* use the same name as your <div id=""> */
    center: [lat, lon], /* set GPS Coordinates */
    zoom: 17, /* define the zoom level */
    zoomControl: true, /* false = no zoom control buttons displayed */
    icon: myIcon,
    scrollWheelZoom: true /* false = scrolling zoom on the map is locked */
});

L.tileLayer('https://{s}.tile.openstreetmap.fr/osmfr/{z}/{x}/{y}.png', { /* set your personal MapBox Access Token */
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

let polyline = null;

const drawTrack = async () => {
    if (polyline != null) {
        polyline.remove();
    }
    let riden_num = document.getElementById('ride-number').value;
    let coordinates = [];
    for (let points of rides[riden_num]) {
        coordinates.push({
            "lat": points.latitude,
            "lng": points.longitude
        })
    }
    console.log(coordinates);
    polyline = L.polyline(coordinates, {weight: 6, color: 'darkred'}).addTo(mymap);

    // zoom the map to the polyline
    mymap.fitBounds(polyline.getBounds());
}