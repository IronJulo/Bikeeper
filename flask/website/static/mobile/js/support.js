var api = null;
let jsonData = null;

function activeLink() {
    api = "http://127.0.0.1/test/message/" + getIdTicket() + "/all"
    return api
}

function getChat() {
    return document.querySelector(String("#chat-" + getIdTicket()));
}

function clearChat() {
    getChat().innerHTML = "";
}

function getIdTicket() {
    let lien = window.location.pathname;
    return lien.split('/')[2];
}


function draw(message) {
    var div = getChat();
    const admin_message = message["is_admin_message"];
    user = message['username_user'];
    user_picture = message["user_picture"]
    estAdmin = isAdmin();


    if (admin_message === 1 && estAdmin === "True" || admin_message === 0 && estAdmin === "False") {
        div.innerHTML += "<div class='row msg'>"
            + "<div class='col-2'></div>"
            + "<div class='col-8 admin'>" + message["content"] + " </div>"
            + "<div class='col-2'><img src='" + getImageUser() + "' class='pp'></div>"
            + "</div>";

    } else if (admin_message === 0 && estAdmin === "True" || admin_message === 1 && estAdmin === "False") {
        div.innerHTML += "<div class='row msg'>"
            + "<div class='col-2'><img src='" + user_picture + "' class='pp'></div>"
            + "<div class='col-8 user'>" + message['content'] + "</div>"
            + "</div>";

    } else {
        console.log("error draw");
    }
}


let oldData = null;

$(document).ready(function () {
    activeLink();
    setInterval(function () {  // loop every 5 seconds
        if (api != null) {
            get(api).then((data) => {
                    //Si data a changé :
                    if (data !== oldData) { // si on doit redraw car nouveau changement
                        clearChat();
                        try {
                            //on actualise jsonData
                            jsonData = JSON.parse(data);
                        } catch (e) {
                            console.error("Parsing error:", e);
                        }
                        if (jsonData != null) {
                            for (let message in jsonData) {
                                // console.log("Drawing message")
                                draw(jsonData[message])
                            }
                            oldData = data
                        }

                    } else {

                    }
                }
            )
        }
    }, 1000);
});

function getDate() {
    let today = new Date();
    let month = today.getMonth() + 1;
    let seconds = today.getSeconds();
    if (month < 10) {
        month = '0' + month;
    }
    if (seconds < 10) {
        seconds = '0' + seconds;
    }
    let date = today.getFullYear() + '-' + month + '-' + today.getDate();
    let time = today.getHours() + ":" + today.getMinutes() + ":" + seconds;
    return date + ' ' + time;
}

$(function () {
    $('#send-msg').on('click', function () {
        let content_message = document.getElementById("msg").value;
        if (content_message.localeCompare("") !== 0) {
            let is_admin_msg = 0;

            if (is_admin === "True") {
                is_admin_msg = 1;
            }

            console.log("message envoyé")

            let datetime_msg = getDate();
            let id_ticket = getIdTicket();
            let username = getUsername();

            let xhttp = new XMLHttpRequest();
            xhttp.open("POST", "/support/message/new", true);
            xhttp.setRequestHeader("Content-Type", "application/json");
            xhttp.onreadystatechange = function () {
                if (this.readyState === 4 && this.status === 200) {
                    console.log("le message est envoyé")
                }
            };
            let data = {
                content: content_message,
                is_admin: is_admin_msg,
                date: datetime_msg,
                id_ticket: id_ticket,
                username: username,
            };

            xhttp.send(JSON.stringify(data));
        }

    });
});

var input = document.getElementById("msg");

input.addEventListener("keyup", function (event) {
    // Number 13 is the "Enter" key on the keyboard
    if (event.keyCode === 13) {
        event.preventDefault();
        document.getElementById("send-msg").click();
        input.value = "";
    }
});