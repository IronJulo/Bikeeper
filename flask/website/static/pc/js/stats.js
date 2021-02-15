var ctx = document.getElementById('angle').getContext('2d');

var gradientStroke = ctx.createLinearGradient(0, 20, 0,screen.height/2.45);
gradientStroke.addColorStop(0, "#FF4500");
gradientStroke.addColorStop(0.30, "#FFFF00");
gradientStroke.addColorStop(0.5, "#00FF00");
gradientStroke.addColorStop(0.70, "#FFFF00");
gradientStroke.addColorStop(1, "#FF4500");
var myChart = new Chart(ctx, {
    type: 'line',
    title: 'Angle',
    data: {
        labels: ['Text', 'Text', 'Text', 'Text', 'Text', 'Text','Text','Text','Text','Text'],
        datasets: [{
            label: 'Hard',
            data: [12, 19, -45, 25, -15, 3,28,52,-25,48,-13,-3,15,34,52,28,-14,-33,0,42],
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

var ctx = document.getElementById('speed').getContext('2d');
var myChart = new Chart(ctx, {
    type: 'line',
    title: 'Speed',
    data: {
        labels: ['Text', 'Text', 'Text', 'Text', 'Text', 'Text','Text','Text','Text','Text','Text','Text','Text','Text','Text','Text','Text','Text','Text','Text',],
        datasets: [{
            fill: false,
            label: 'speed',
            data: [12, 19, 3, 5, 2, 3,28,52,-25,48,-13,-3,15,34,52,28,-14,-33,0,42],
            borderColor: ['rgba(135,206,235,1)'],
            pointBackgroundColor: ['rgba(135,206,235,1)','rgba(135,206,235,1)','rgba(135,206,235,1)','rgba(135,206,235,1)','rgba(135,206,235,1)','rgba(135,206,235,1)','rgba(135,206,235,1)','rgba(135,206,235,1)','rgba(135,206,235,1)','rgba(135,206,235,1)','rgba(135,206,235,1)','rgba(135,206,235,1)','rgba(135,206,235,1)','rgba(135,206,235,1)','rgba(135,206,235,1)','rgba(135,206,235,1)','rgba(135,206,235,1)','rgba(135,206,235,1)','rgba(135,206,235,1)','rgba(135,206,235,1)',],
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

var url = window.location.href
var arr = url.split("/");
var result = arr[0] + "//" + arr[2]
 var myIcon = L.icon({
            iconUrl: result + "/static/pc/assets/logo_bikeeper_without_text.png",
            iconSize: [40, 40],
            iconAnchor: [25, 50],
            popupAnchor: [-3, -76],
        });


// On initialise la latitude et la longitude de Paris (centre de la carte)
var lat = 47.902964;
var lon = 1.909251;

var mymap = L.map('position', { /* use the same name as your <div id=""> */
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