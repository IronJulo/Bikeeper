let ctx = document.getElementById('angle').getContext('2d');

const gradientStroke = ctx.createLinearGradient(0, 20, 0, screen.height / 2.45);
gradientStroke.addColorStop(0, "#FF4500");
gradientStroke.addColorStop(0.30, "#FFFF00");
gradientStroke.addColorStop(0.5, "#00FF00");
gradientStroke.addColorStop(0.70, "#FFFF00");
gradientStroke.addColorStop(1, "#FF4500");

const Angle = new Chart(ctx, { // Angle chart
    type: 'line',
    title: 'Angle',
    data: {
        labels: [],
        datasets: [{
            label: 'Hard',
            data: [],
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

const Speed = new Chart(document.getElementById('speed').getContext('2d'), { // Speed chart
    type: 'line',
    title: 'Speed',
    data: {
        labels: [],
        datasets: [{
            fill: false,
            label: 'speed',
            data: [],
            borderColor: ['rgba(135,206,235,1)'],
            pointBackgroundColor: [],
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


function updateSpeedChart(data, labels) {
    let colors = new Array(data.length).fill('rgba(135,206,235,1)');
    Speed.data.datasets[0].data = data;
    Speed.data.datasets[0].pointBackgroundColor = colors;
    Speed.data.labels = labels;
    document.getElementById("max-speed").innerText = data.reduce((a, b) => {
        return Math.max(a, b)
    });
    document.getElementById("average-speed").innerText = (data.reduce((a, b) => a + b, 0) / data.length).toString();
    Speed.update();
}

function updateAngleChart(data, labels) {
    let colors = new Array(data.length).fill('rgba(135,206,235,1)');
    Angle.data.datasets[0].data = data;
    Angle.data.datasets[0].pointBackgroundColor = colors;
    Angle.data.labels = labels;
    document.getElementById("max-angle").innerText = data.reduce((a, b) => {
        return Math.max(a, b)
    });
    document.getElementById("average-angle").innerText = (data.reduce((a, b) => a + b, 0) / data.length).toString();
    Angle.update();

}