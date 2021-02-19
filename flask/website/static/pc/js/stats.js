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


const updateHeaderInfo = async () => {
    let bikeeper = document.getElementById('device-number').value;
    let response = await fetch('/api/bikeeper/get_last_ride_bikeeper/' + bikeeper);
    const last_ride = await response.json();
    document.getElementById("last-ride").innerText = last_ride.datetime_log;
    document.getElementById("last-ride-duration").innerText = last_ride.total_time;

    response = await fetch('/api/bikeeper/get_battery_level/' + bikeeper);
    const battery_info = await response.json();

    let img_name;
    const level_avg = (battery_info.level[0] + battery_info.level[1]) / 2;
    if (level_avg > 90) {
        img_name = '/static/pc/assets/battery_full_charge.png';
    } else if (level_avg > 75) {
        img_name = '/static/pc/assets/battery_75_charge.png';
    } else if (level_avg > 50) {
        img_name = '/static/pc/assets/battery_50_charge.png';
    } else if (level_avg > 25) {
        img_name = '/static/pc/assets/battery_25_charge.png';
    } else {
        img_name = '/static/pc/assets/battery_low_charge.png';
    }

    document.getElementById("battery-img").src = img_name;
    if (battery_info.charge === "t") {
        document.getElementById("is-charging").innerText = "The battery is charging"
    } else if (battery_info.charge === "f") {
        document.getElementById("is-charging").innerText = "The battery isn't charging"
    }
}

function updateSpeedChart(data, labels) {
    let colors = new Array(data.length).fill('rgba(135,206,235,1)');
    Speed.data.datasets[0].data = data;
    Speed.data.datasets[0].pointBackgroundColor = colors;
    Speed.data.labels = labels;
    document.getElementById("max-speed").innerText = data.reduce((a, b) => {
        return Math.max(a, b)
    });
    document.getElementById("average-speed").innerText = (data.reduce((a, b) => a + b, 0) / data.length).toString();
    Speed.update();
}

function updateAngleChart(data, labels) {
    let colors = new Array(data.length).fill('rgba(135,206,235,1)');
    Angle.data.datasets[0].data = data;
    Angle.data.datasets[0].pointBackgroundColor = colors;
    Angle.data.labels = labels;
    document.getElementById("max-angle").innerText = data.reduce((a, b) => {
        return Math.max(a, b)
    });
    document.getElementById("average-angle").innerText = (data.reduce((a, b) => a + b, 0) / data.length).toString();
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
        await updateHeaderInfo();
    }
}

const loadRides = async () => { // updates the field "rides" to show rides of a certain device and date
    let date = document.getElementById('ride-date').value;
    let bikeeper = document.getElementById('device-number').value;
    const response_logs = await fetch('/api/bikeeper/get_logs_at_date/' + bikeeper + "/" + date);
    logs = await response_logs.json();
    const response = await fetch('/api/bikeeper/get_rides_from_user_at_time_with_bikeeper/' + username_stats + "/" + bikeeper + "/" + date);
    rides = await response.json();
    reset_form_by_id('ride-number');
    let form_ride_number = document.getElementById('ride-number');
    for (let i = 0; i < rides.length; i++) {
        let node = document.createElement("option");
        node.appendChild(document.createTextNode("Ride " + i))
        node.value = i.toString();
        form_ride_number.appendChild(node);
    }
    await updateHeaderInfo();
    if (form_ride_number.value !== "") {
        await displayRideData();
    }
}

const createTimelineElements = async () => {
    let date = document.getElementById('ride-date').value;
    let bikeeper = document.getElementById('device-number').value;
    const response = await fetch('/api/bikeeper/get_logs_at_date/' + bikeeper + "/" + date);
    let timeline_logs = await response.json();
    const allowed_logs = ["W", "+"]
    let div_timeline = document.getElementsByClassName('timeline')[0];
    reset_timeline_by_class('timeline');
    for (const log of timeline_logs.reverse()) {
        if (allowed_logs.includes(log.type_log)) {
            let style = document.createElement("style");
            div_timeline.appendChild(style);
            let timeline_event = document.createElement("div");
            timeline_event.classList.add("timeline__event", "animated", "fadeInUp", "delay-3s", "timeline__event--type1");
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
            if (log.type_log !== "W") {
                let t = "";
                if (log.content_log.type === "A") {
                    t = "The vehicle has been parked.";
                }
                if (log.content_log.type === "B") {
                    t = "The vehicle is not longer parked.";
                } else if (log.content_log.type === "C") {
                    t = "A journey has begun.";
                } else if (log.content_log.type === "D") {
                    t = "A journey ended up.";
                }


                let title_content = document.createTextNode("Information")
                timeline_title.appendChild(title_content);
                let style_content = document.createTextNode(":root {\n" +
                    "                                    --timeline-main-color: #7BC6E1;\n" +
                    "                                }");
                style.appendChild(style_content);
                let timeline_description_text_content = document.createTextNode(t)
                timeline_description_text.appendChild(timeline_description_text_content);
            } else {
                let t = "";
                let text_content = "";
                if (log.content_log.type === "V") {
                    t = "Vibration detected";
                    text_content = "A vibration has been detected at those coordinates :\n" +
                        "Longitude : " + log.content_log.longitude + "\n" +
                        "Latitude : " + log.content_log.latitude + "\n" +
                        "Someone or something may have it your vehicle.";
                } else if (log.content_log.type === "G") {
                    t = "GPS Signal detected";
                    text_content = "Your device begun to move from those coordinates :\n" +
                        "Longitude : " + log.content_log.longitude + "\n" +
                        "Latitude : " + log.content_log.latitude + "\n" +
                        "Maybe someone is trying to steal your vehicle.";
                } else if (log.content_log.type === "F") {
                    t = "Vehicle fall detected";
                    text_content = "Your device has fallen at those coordinates :\n" +
                        "Longitude : " + log.content_log.longitude + "\n" +
                        "Latitude : " + log.content_log.latitude + "\n";
                }
                let title_content = document.createTextNode("Alert - " + t)
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
}


function reset_timeline_by_class(classe) {
    let timeline = document.getElementsByClassName(classe)[0];
    while (timeline.firstChild) {
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


    // #################################################################################################
    // #################################################################################################
    // #################################################################################################

    var api=null;
    let parkData = null;


    function activeLink() {
        api = "http://127.0.0.1:5000/test/device/"+ getIdDevice()
        return api
    }


    function getPark(){
      return String("parked");
    }
    function getTextOfSelectedNumberDevice() {
        return document.getElementById("device-number")[document.getElementById("device-number").options.selectedIndex].text;
    }

    function clearPark(){
      getPark().innerHTML = "";
    }

    function getIdDevice(){
      return document.getElementById("device-number").value;
    }

    function get(url) {
        return new Promise((resolve, reject) => {
            const req = new XMLHttpRequest();
            req.open('GET', url);
            req.onload = () => req.status === 200 ? resolve(req.response) : reject(Error(req.statusText));
            req.onerror = (e) => reject(Error(`Network Error: ${e}`));
            req.send();
        });
    }

    function draw(is_parked) {
      console.log("Draw");
      console.log(getIdDevice())
          let park = "." + getPark();
          let parked = is_parked.parked;
          let text = "<div class='row'><div class='col-6 goche'>Selected device : " + getTextOfSelectedNumberDevice() + "</div>";
          text += "<div class='col-6 drouate'>Status : ";
          if (parked) {
            console.log("Pause")
            text += " Parked <i class='fa fa-pause'></i>";
          }
          else {
            console.log("Play")
            text += " Moving <i class='fa fa-play'></i>"
          }
          document.querySelector(park).innerHTML = text + "</div></div>";
    }


    let oldData = null;

    $(document).ready(function () {
        setInterval(function () {  // loop every 5 seconds
            activeLink()
            if (api!=null){
                get(api).then((data) => {
                    //Si data a changé :
                    try {
                            //on actualise parkData
                            parkData = JSON.parse(data);
                        } catch (e) {
                            console.error("Parsing error:", e);
                        }



                    if (oldData==null || (parkData.parked > oldData || parkData.parked < oldData)) { // si on doit redraw car nouveau changement
                      
                      
                      clearPark();
                        
                        if (parkData != null) {
                          oldData = parkData.parked
                          console.log(oldData)
                            draw(parkData)
                        }

                    } else {
                      oldData = parkData.parked
                    }
                }
            )
          }
        }, 5000);
    });

    function getDate(){
      var today = new Date();
      var month = today.getMonth()+1;
      var seconds = today.getSeconds();
      if (month<10){
          month = '0'+month;
      }
      if (seconds<10){
          seconds = '0'+seconds;
      }
      var date = today.getFullYear()+'-'+month+'-'+today.getDate();
      var time = today.getHours() + ":" + today.getMinutes() + ":" + seconds;
      return date+' '+time;
    }






}