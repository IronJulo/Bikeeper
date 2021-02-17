let ctx = document.getElementById('angle').getContext('2d');

const gradientStroke = ctx.createLinearGradient(0, 20, 0, screen.height / 2.45);
gradientStroke.addColorStop(0, "#FF4500");
gradientStroke.addColorStop(0.30, "#FFFF00");
gradientStroke.addColorStop(0.5, "#00FF00");
gradientStroke.addColorStop(0.70, "#FFFF00");
gradientStroke.addColorStop(1, "#FF4500");

const Angle = new Chart(ctx, { // Angle chart
    type: 'line',
    title: 'Angle',
    data: {
        labels: [],
        datasets: [{
            label: 'Hard',
            data: [],
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

const Speed = new Chart(document.getElementById('speed').getContext('2d'), { // Speed chart
    type: 'line',
    title: 'Speed',
    data: {
        labels: [],
        datasets: [{
            fill: false,
            label: 'speed',
            data: [],
            borderColor: ['rgba(135,206,235,1)'],
            pointBackgroundColor: [],
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

function updateSpeedChart(data, labels) {
    let colors = new Array(data.length).fill('rgba(135,206,235,1)');
    Speed.data.datasets[0].data = data;
    Speed.data.datasets[0].pointBackgroundColor = colors;
    Speed.data.labels = labels;
    document.getElementById("max-speed").innerText = data.reduce((a, b) => { return Math.max(a, b) });
    document.getElementById("average-speed").innerText = data.reduce((a,b) => a + b, 0) / data.length;
    Speed.update();
}

function updateAngleChart(data, labels) {
    let colors = new Array(data.length).fill('rgba(135,206,235,1)');
    Angle.data.datasets[0].data = data;
    Angle.data.datasets[0].pointBackgroundColor = colors;
    Angle.data.labels = labels;
    document.getElementById("max-angle").innerText = data.reduce((a, b) => { return Math.max(a, b) });
    document.getElementById("average-speed").innerText = data.reduce((a,b) => a + b, 0) / data.length;
    Angle.update();
}

let rides = null; // rides data
let logs = null; // logs data


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
        await createTimelineElements();
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
        await displayRideData();
    }
}

const createTimelineElements = async() => {
    let date = document.getElementById('ride-date').value;
    let bikeeper = document.getElementById('device-number').value;
    const response = await fetch('/api/bikeeper/get_logs_at_date/' + bikeeper + "/" + date);
    timeline_logs = await response.json();
    console.log(timeline_logs);
    let div_timeline = document.getElementsByClassName('timeline')[0];
    reset_timeline_by_class('timeline');
    for (const log of timeline_logs.reverse()) {
        let style = document.createElement("style");
        div_timeline.appendChild(style);
        let timeline_event = document.createElement("div");
        timeline_event.classList.add("timeline__event",  "animated", "fadeInUp", "delay-3s", "timeline__event--type1");
        let timeline_event_icon = document.createElement("div");
        timeline_event_icon.classList.add("timeline__event__icon");
        let icon = document.createElement("i");
        icon.classList.add("fa", "fa-info-circle");
        let timeline_date = document.createElement("div");
        timeline_date.classList.add("timeline__event__date");
        let timeline_content = document.createElement("div");
        timeline_content.classList.add("timeline__event__content");
        let timeline_title = document.createElement("div");
        timeline_title.classList.add("timeline__event__title");
        let timeline_description = document.createElement("div");
        timeline_description.classList.add("timeline__event__description");
        let timeline_description_text = document.createElement("p");
        let date_content = document.createTextNode(log.datetime_log);
        div_timeline.appendChild(timeline_event);
        timeline_event.appendChild(timeline_event_icon);
        timeline_event_icon.appendChild(icon);
        timeline_event_icon.appendChild(timeline_date);
        timeline_event.appendChild(timeline_content);
        timeline_content.appendChild(timeline_title);
        timeline_content.appendChild(timeline_description);
        timeline_description.appendChild(timeline_description_text);
        timeline_date.appendChild(date_content);
        if (log.type_log !== "W"){
            let t = "";
            if (log.type_log == "+"){
                if (log.content_log.type == "C"){
                    t = "Un trajet a commencé.";
                }
                else if (log.content_log.type == "D"){
                    t = "Un trajet s'est terminé.";
                }
            }

            let title_content = document.createTextNode("Information")
            timeline_title.appendChild(title_content);
            let style_content = document.createTextNode(":root {\n" +
                "                                    --timeline-main-color: #7BC6E1;\n" +
                "                                }");
            style.appendChild(style_content);
            let timeline_description_text_content = document.createTextNode(t)
            timeline_description_text.appendChild(timeline_description_text_content);
        }
        else{
            let t = "";
            let text_content = "";
            if (log.content_log.type == "V"){
                t = "Vibration détectée";
                text_content = "Une vibration a été détectée sur votre Bikeeper aux coordonnées suivantes :\n" +
                "Longitude : " + log.content_log.longitude + "\n" +
                "Latitude : " + log.content_log.latitude + "\n";
            }
            else if (log.content_log.type == "G"){
                t = "Signal GPS";
                text_content = "Votre Bikeeper a commencé à bouger depuis les coordonnées suivantes :\n" +
                "Longitude : " + log.content_log.longitude + "\n" +
                "Latitude : " + log.content_log.latitude + "\n";
            }
            else if (log.content_log.type == "F"){
                t = "Chute du véhicule";
                text_content = "Votre Bikeeper est tombé aux coordonnées suivantes :\n" +
                "Longitude : " + log.content_log.longitude + "\n" +
                "Latitude : " + log.content_log.latitude + "\n";
            }
            let title_content = document.createTextNode("Alerte - " + t)
            let style_content = document.createTextNode(":root {\n" +
                "                                    --timeline-main-color: #DC1D21;\n" +
                "                                }");
            style.appendChild(style_content);
            timeline_title.appendChild(title_content);
            let timeline_description_text_content = document.createTextNode(text_content);
            timeline_description_text.appendChild(timeline_description_text_content);
        }
    }
}

function reset_timeline_by_class(classe){
    let timeline = document.getElementsByClassName(classe)[0];
    while (timeline.firstChild){
        timeline.removeChild(timeline.lastChild);
    }
}

function reset_form_by_id(name) { // reset a form
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

const displayRideData = async () => { // Called when a user selects a ride display dataon the charts, map and timeline
    if (polyline != null) {
        polyline.remove();
    }
    let riden_num = document.getElementById('ride-number').value;
    let coordinates = [];
    let speeds = [];
    let angles = [];
    let labels = [];
    for (let points of rides[riden_num]) {
        coordinates.push({
            "lat": points.latitude,
            "lng": points.longitude
        });
        speeds.push(points["speed"]);
        angles.push(points["angle"]);
        labels.push(points["datetime_log"].slice(11, 16));
    }
    polyline = L.polyline(coordinates, {weight: 6, color: 'darkred'}).addTo(mymap);

    // zoom the map to the polyline
    mymap.fitBounds(polyline.getBounds());
    updateSpeedChart(speeds, labels);
    updateAngleChart(angles, labels);
}