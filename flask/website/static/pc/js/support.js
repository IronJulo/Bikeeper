var api=null;
let jsonData = null;

function activeLink(tab) {
    try{
        li_active = getActive();
        a_active = getLinkActive();

        li_active.classList.replace("active","inactive");
        a_active.classList.replace("active","inactive");
    }
    catch {
      console.log("cannot get active link");
    }
    tab.classList.replace("inactive","active");
    api = "/test/message/"+ getIdTicket() +"/all"
}

function getActive(){
  return document.querySelector("ul.nav > li.active");
}

function getLinkActive(){
  return document.querySelector("ul.nav li.active div.ticket-title a:first-of-type");
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
  return lien.split('tab')[1];
}


function draw(message) {
  console.log("draw : "+message);
      var div = getActiveUL();
      const admin_message = message["is_admin_message"];
      user = message['username_user'];
      user_picture = message["user_picture"]
      estAdmin = isAdmin();

      if (admin_message===1 && estAdmin==="True" || admin_message===0 && estAdmin=="False"){
        div.innerHTML += "<li class=\"sent\"><div>"
        + "<span>"+ user +"</span>"
        + "<p>" + message["content"] + "</p>"
        + "</div>"
        + "<div style=\"background-image: url('" + getImageUser() + "')\"></div>"
        + "</li>"
      }
      else if (admin_message===0 && estAdmin==="True" || admin_message===1 && estAdmin==="False"){
        div.innerHTML +="<li class=\"replies\">"
        + "<div style=\"background-image: url('" + user_picture + "')\"></div>"
        + "<div>"
        + "<span>"+ user +"</span>"
        + "<p>" + message["content"] +"</p>"
        + "</div></li>"
      }
      else {
        console.log("error draw");
      }
}

let oldData = null;

$(document).ready(function () {
  try {
    api = "/test/message/"+ getIdTicket() +"/all"
    get(api).then((data) => {
      clearDiv();
      try {
          jsonData = JSON.parse(data);
      } catch (e) {
          console.error("Parsing error:", e);
      }
      if (jsonData != null) {
          for (let message in jsonData) {
            draw(jsonData[message]);
          }
          let activeDiv = getActiveUL();
          activeDiv.parentNode.classList.add("active","show");
          oldData = data;
      }
    })
  } catch (TypeError) {
    console.log("No active link");
  }
});

$(document).ready(function () {
    var loadingMessage = setInterval(function () {
      if (api!=null){
        get(api).then((data) => {
                //Si data a chang?? :
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

function breakLoading(){
  clearInterval(loadingMessage)
}

function getDate(){
  let today = new Date();
  let month = today.getMonth()+1;
  let seconds = today.getSeconds();
  if (month<10){
      month = '0'+month;
  }
  if (seconds<10){
      seconds = '0'+seconds;
  }
  let date = today.getFullYear()+'-'+month+'-'+today.getDate();
  let time = today.getHours() + ":" + today.getMinutes() + ":" + seconds;
  return date+' '+time;
}

$(function() {
  $('#send-msg').on('click', function() {
    let content_message = document.getElementById("msg").value;
    let is_admin_msg = 0;

    if (is_admin==="True"){
        is_admin_msg = 1;
    }

    console.log("message envoy??")

    let datetime_msg = getDate();
    let id_ticket = getIdTicket();
    let username = getUsername();

    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/support/message/new", true); 
    xhttp.setRequestHeader("Content-Type", "application/json");
    xhttp.onreadystatechange = function() {
      if (this.readyState === 4 && this.status === 200) {
        console.log("le message est envoy??")
      }
    };
    var data = {
        content:content_message,
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


function checkRadioButton(elem) {
  elem.nextSibling.nextSibling.checked=true
}

function deleteTicket() {
    id_ticket = getIdTicket()
    $.ajax({
    url: "/support/ticket/close/" + id_ticket,
    type: 'DELETE',
    success: function(result) {
        window.location.replace(window.location.href)
    }, error: function (data) {
        console.log('Error:', data);
    }

});
}