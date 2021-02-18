const today = new Date().toJSON().slice(0, 10);

const get_today_rides_count = async () => {
    const response = await fetch('/api/bikeeper/get_rides_from_user_at_time_with_bikeeper/' + username_home + "/" + selected_device + "/" + today);
    rides = await response.json();
    return rides.length;

}

const get_today_logs = async () => {
    const response_logs = await fetch('/api/bikeeper/get_logs_at_date/' + selected_device + "/" + today);
    logs = await response_logs.json();
    let informations = 0;
    let alerts = 0;
    console.log(logs);
    for (const log of logs){
        if (log.type_log === "+") {
            informations++;
    }
        if (log.type_log === "W") {
            alerts++;
        }
    }
    return [alerts, informations];
}

get_today_rides_count().then(r => document.getElementById('rides').innerText+= " (" + r + ")" );
get_today_logs().then(function(r){
    document.getElementById('notifications').innerText+= " (" + r[1] + ")";
    document.getElementById('alerts').innerText+= " (" + r[0] + ")";
});


