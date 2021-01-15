var api=null;
let jsonData = null;


function activeLink(tab) {
    try{
        active = getActive();
        active.classList.replace("active","inactive");
    }
    catch {

    }
    tab.classList.replace("inactive","active");
    api = "http://127.0.0.1:5000/test/message/"+ getIdTicket() +"/all"
}

function getActive(){
  return document.querySelector("ul.nav > li.active");
}

function getLinkActive(){
  return document.querySelector("ul.nav li.active a");
}

function getActiveUL(){
  return document.querySelector(String("#ul-"+getIdTicket()));
}

function clearDiv(){
  getActiveUL().innerHTML = "";
}

function getIdTicket(){
  actif = getLinkActive();
  lien = actif.href;
  numero = lien.split('tab')[1];
  return numero;
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

function draw(message) {
    // {content: "Bonjour de la par d'un admin", datetime_message: "11/28/2017, 23:55:59", id_ticket: 1, is_admin_message: 0}
      var div = getActiveUL();
      const admin_message = message["is_admin_message"];
      user = message['username_user'];
      estAdmin = isAdmin();

      if (admin_message==1 && estAdmin=="True" || admin_message==0 && estAdmin=="False"){
        div.innerHTML += "<li class=\"sent\">"
        + "<p>" + message["content"] + "</p>"
        + "<img src=\""+ getImageUser() +"\" alt=\"\"/>"
        + "<span>"+ getUsername() +"</span>"
        + "</li>"
      }
      else if (admin_message==0 && estAdmin=="True" || admin_message==1 && estAdmin=="False"){
        div.innerHTML +="<li class=\"replies\">"
        + "<img src=\"http://emilcarlsson.se/assets/harveyspecter.png\" alt=\"\"/>"
        + "<p>" + message["content"] +"</p>"
        + "<span>"+ getUsername() +"</span>"
        + "</li>"
      }
      else {
        console.log("error draw");
      }
}


let oldData = null;

$(document).ready(function () {
    setInterval(function () {  // loop every 5 seconds
      if (api!=null){
        get(api).then((data) => {
                //Si data a changé :
                if (data !== oldData) { // si on doit redraw car nouveau changement
                  clearDiv();
                    try {
                        //on actualise jsonData
                        jsonData = JSON.parse(data);
                    } catch (e) {
                        console.error("Parsing error:", e);
                    }

                    if (jsonData != null) {
                        for (let message in jsonData) {
                            //console.log("Drawing message")
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

$(function() {
  $('#send-msg').on('click', function() {
    var contenu_message = document.getElementById("msg").value;
    var is_admin_msg = 0;

    if (isAdmin()=="True"){
        is_admin_msg = 1;
    }

    var datetime_msg = getDate();
    var id_ticket = getIdTicket();
    var username = getUsername();

    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/support/message/new", true); 
    xhttp.setRequestHeader("Content-Type", "application/json");
    xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        console.log("le message est envoyé")
      }
    };
    var data = {
        content:contenu_message,
        is_admin:is_admin_msg,
        date:datetime_msg,
        id_ticket:id_ticket,
        username:username,
    };
    
    xhttp.send(JSON.stringify(data));
  });
});

var input = document.getElementById("msg");

input.addEventListener("keyup", function(event) {
  // Number 13 is the "Enter" key on the keyboard
  if (event.keyCode === 13) {
    event.preventDefault();
    document.getElementById("send-msg").click();
    input.value="";
  }
});