

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

    if (document.getElementById("battery-img") == null) {
        const img_child = document.createElement('img');
        img_child.setAttribute("id", "battery-img");
        img_child.setAttribute("alt", "battery");
        img_child.setAttribute("src", img_name);
        document.getElementsByClassName("bikeeper-data")[0].appendChild(img_child);
    } else {
        document.getElementById("battery-img").setAttribute("src", img_name);
    }
    if (battery_info.charge === "t") {
        document.getElementById("is-charging").innerText = "The battery is charging"
    } else if (battery_info.charge === "f") {
        document.getElementById("is-charging").innerText = "The battery isn't charging"
    }
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


function reset_form_by_id(name) { // reset a form
    let form = document.getElementById(name);
    while (form.firstChild) {
        form.removeChild(form.lastChild);
    }
}

document.getElementById('ride-date').value = new Date().toJSON().slice(0, 10); // setting todays date by default
loadDateBikeepers();


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

    var api = null;
    let parkData = null;


    function activeLink() {
        api = "http://127.0.0.1:8080/api/device/" + getIdDevice()
        return api
    }


    function getPark() {
        return String("parked");
    }

    function getTextOfSelectedNumberDevice() {
        return document.getElementById("device-number")[document.getElementById("device-number").options.selectedIndex].text;
    }

    function clearPark() {
        getPark().innerHTML = "";
    }

    function getIdDevice() {
        return document.getElementById("device-number").value;
    }

    function draw(is_parked) {
        let park = "." + getPark();
        let parked = is_parked.parked;
        let text = "<div class='row'><div class='col-6 goche'>Selected device : " + getTextOfSelectedNumberDevice() + "</div>";
        text += "<div class='col-6 drouate'>Status : ";
        if (parked) {
            console.log("Pause")
            text += " Parked <i class='fa fa-pause'></i>";
        } else {
            console.log("Play")
            text += " Moving <i class='fa fa-play'></i>"
        }
        try {
            document.querySelector(park).innerHTML = text + "</div></div>";
        } catch {
            
        }
        
    }


    let oldData = null;

    $(document).ready(function () {
        setInterval(function () {  // loop every 5 seconds
            activeLink()
            if (api != null) {
                get(api).then((data) => {
                        //Si data a changé :
                        try {
                            //on actualise parkData
                            parkData = JSON.parse(data);
                        } catch (e) {
                            console.error("Parsing error:", e);
                        }

                        if (oldData == null || (parkData.parked > oldData || parkData.parked < oldData)) { // si on doit redraw car nouveau changement

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



}