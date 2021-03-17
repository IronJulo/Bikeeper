function reset_timeline_by_class(css_class) {
    let timeline = document.getElementsByClassName(css_class)[0];
    while (timeline.firstChild) {
        timeline.removeChild(timeline.lastChild);
    }
}

function createTimelineEvent(date){
    //main div
    let timeline_event = document.createElement("div");
    timeline_event.classList.add("timeline__event", "animated", "fadeInUp", "delay-3s", "timeline__event--type1");
    //first child of main div
    let timeline_event_icon = document.createElement("div");
    timeline_event_icon.classList.add("timeline__event__icon");
    timeline_event.appendChild(timeline_event_icon);
    //first child of timeline_event_icon
    let icon = document.createElement("i");
    icon.classList.add("fa", "fa-info-circle");
    timeline_event_icon.appendChild(icon);
    //second child of timeline_event_icon
    let timeline_date = document.createElement("div");
    timeline_date.textContent = date
    timeline_date.classList.add("timeline__event__date");
    timeline_event_icon.appendChild(timeline_date);
    //second child of main div
    let timeline_content = document.createElement("div");
    timeline_content.classList.add("timeline__event__content");
    timeline_event.appendChild(timeline_content);
    //first child of timeline_content
    let timeline_title = document.createElement("div");
    timeline_title.classList.add("timeline__event__title");
    timeline_content.appendChild(timeline_title);
    //second child of timeline_content
    let timeline_description = document.createElement("div");
    timeline_description.classList.add("timeline__event__description");
    timeline_content.appendChild(timeline_description);
    //paragraph of timeline_description
    let timeline_description_text = document.createElement("p");
    timeline_description.appendChild(timeline_description_text);
    
    document.querySelector(".timeline").appendChild(timeline_event);

    return {
        "main": timeline_event,
        "div_icon": timeline_event_icon,
        "icon": icon,
        "date": timeline_date,
        "content": timeline_content,
        "title": timeline_title,
        "description": timeline_description,
        "description_text": timeline_description_text
    }
}

const type_log_plus = {
    "A": "The vehicle has been parked.",
    "B": "The vehicle is not longer parked.",
    "C": "A journey has begun.",
    "D": "A journey ended up."
}

const createTimelineElements = async () => {
    let date = document.getElementById('ride-date').value;
    let bikeeper = document.getElementById('device-number').value;
    const response = await fetch('/api/bikeeper/get_logs_at_date/' + bikeeper + "/" + date);
    let timeline_logs = await response.json();
    const allowed_logs = ["W", "+"]
    reset_timeline_by_class('timeline');

    for (const log of timeline_logs.reverse()) {
        if (allowed_logs.includes(log.type_log)) {

            let timelineEvent = createTimelineEvent(log.datetime_log);
            
            let type_log_w = {
                "V": {
                    "title": "Vibration detected",
                    "textContent": "A vibration has been detected at those coordinates :\n" +
                                    "Longitude : " + log.content_log.longitude + "\n" +
                                    "Latitude : " + log.content_log.latitude + "\n" +
                                    "Someone or something may have it your vehicle."
                },
                "G": {
                    "title": "GPS Signal detected",
                    "textContent": "Your device began to move from those coordinates :\n" +
                                    "Longitude : " + log.content_log.longitude + "\n" +
                                    "Latitude : " + log.content_log.latitude + "\n" +
                                    "Maybe someone is trying to steal your vehicle."
                },
                "F": {
                    "title": "Vehicle fall detected",
                    "textContent": "Your device has fallen at those coordinates :\n" +
                                    "Longitude : " + log.content_log.longitude + "\n" +
                                    "Latitude : " + log.content_log.latitude + "\n"
                }
                
            }

            try {
                if (log.type_log === "+") {
                    timelineEvent.description.textContent = type_log_plus[log.content_log.type];
                    timelineEvent.title.textContent = "Information";
                } 
                else {
                    let type = type_log_w[log.content_log.type];
                    timelineEvent.title.textContent = "Alert - " + type["title"];
                    timelineEvent.title.style.color = "#DC1D21";
                    timelineEvent.icon.style.backgroundColor = "#DC1D21";
                    timelineEvent.description.textContent = type["textContent"];
                }
            } catch (error) {
                console.log("Error : "+error);
            }
        }
    }
}