var api=null;
let parkData = null;


function activeLink() {
    api = "http://127.0.0.1:5000/test/device/"+ getIdDevice()
    return api
}


function getPark(){
  return String("parked-"+getIdDevice());
}

function clearPark(){
  getPark().innerHTML = "";
}

function getIdDevice(){
  var parked = document.getElementsByClassName("park")[0].classList[0];
  numero = parked.split('-')[1];
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

function draw(is_parked) {
  console.log("Draw");
      let park = "." + getPark();
      let parked = is_parked.parked;
      if (parked) {
        console.log("Pause")
        document.querySelector(park).innerHTML = " Parked <i class='fa fa-pause'></i>";
      }
      else {
        console.log("Play")
        document.querySelector(park).innerHTML = " Moving <i class='fa fa-play'></i>"
      }
}


let oldData = null;

$(document).ready(function () {
  activeLink();
    setInterval(function () {  // loop every 5 seconds
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