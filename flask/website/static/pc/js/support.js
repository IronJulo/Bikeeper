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
      const expr = message["is_admin_message"]
      switch (expr) {
          case 0:
                div.innerHTML +="<li class=\"replies\">"
                + "<img src=\"http://emilcarlsson.se/assets/harveyspecter.png\" alt=\"\"/>"
                + "<p>" + message["content"] +"</p>"
                + "</li>"
              break;
          case 1:
                div.innerHTML += "<li class=\"sent\">"
                + "<p>" + message["content"] + "</p>"
                + "<img src=\"http://emilcarlsson.se/assets/mikeross.png\" alt=\"\"/>"
                + "</li>"
              break;
          default:
              console.log(`Sorry, we are out of ${expr}.`);
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
                        console.log("DATA :"+data);
                        console.log("JSONDATA : "+jsonData);
                    } catch (e) {
                        console.error("Parsing error:", e);
                    }

                    if (jsonData != null) {
                        for (let message in jsonData) {
                            console.log("JE PASSE DANS LE FOR")
                            console.log("MESSAGE : "+jsonData[message])
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