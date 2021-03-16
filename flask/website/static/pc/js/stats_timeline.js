function reset_timeline_by_class(css_class) {
    let timeline = document.getElementsByClassName(css_class)[0];
    while (timeline.firstChild) {
        timeline.removeChild(timeline.lastChild);
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
                switch (log.content_log.type) {

                    case "A" :
                        t = "The vehicle has been parked.";
                        break;

                    case "B" :
                        t = "The vehicle is not longer parked.";
                        break;

                    case "C" :
                        t = "A journey has begun.";
                        break;
                    case "D" :
                        t = "A journey ended up.";
                        break;
                    default :
                        t = "Error";
                        console.log("Error")
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
                switch (log.content_log.type) {

                    case "V" :
                        t = "Vibration detected";
                        text_content = "A vibration has been detected at those coordinates :\n" +
                            "Longitude : " + log.content_log.longitude + "\n" +
                            "Latitude : " + log.content_log.latitude + "\n" +
                            "Someone or something may have it your vehicle.";
                        break;

                    case "G" :
                        t = "GPS Signal detected";
                        text_content = "Your device begun to move from those coordinates :\n" +
                            "Longitude : " + log.content_log.longitude + "\n" +
                            "Latitude : " + log.content_log.latitude + "\n" +
                            "Maybe someone is trying to steal your vehicle.";
                        break;

                    case "F" :
                        t = "Vehicle fall detected";
                        text_content = "Your device has fallen at those coordinates :\n" +
                            "Longitude : " + log.content_log.longitude + "\n" +
                            "Latitude : " + log.content_log.latitude + "\n";
                        break;

                    default :
                        t = "Error";
                        text_content = "Alerte Error";
                        console.log("Error");

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