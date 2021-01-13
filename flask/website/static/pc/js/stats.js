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