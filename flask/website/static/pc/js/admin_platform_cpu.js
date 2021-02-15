var resCPU = 0


function getServerCpu() {
    $.ajax({
        url: "/api/stats/cpu/",
        success: function (result) {
            resCPU = result.response
        },
        error: function (err) {
            console.log("Error")
            console.log(err)
        }
    });
}


var canvasCPU = document.getElementById('cpu')
var ctxCPU = canvasCPU.getContext('2d');

var gradientStroke = ctxCPU.createLinearGradient(500, 0, 100, 0);
gradientStroke.addColorStop(0, '#f49080'); // bleu
gradientStroke.addColorStop(1, '#80b6f4'); // red




var CpuLineChart = new Chart(ctxCPU, {
    type: 'line',
    pointRadius: 0,
    fill: false,
    lineTension: 4,
    borderWidth: 2,
    data: {
        labels: [],
        datasets: [
            {
                data: [],
                label: 'CPU Usage in percent',
                borderColor: gradientStroke,
                pointBorderColor: gradientStroke,
                pointBackgroundColor: gradientStroke,
                pointHoverBackgroundColor: gradientStroke,
                pointHoverBorderColor: gradientStroke,
                backgroundColor: "#36a2eb88"

            }
        ],

    },
    options: {
        responsive: false,
        maintainAspectRatio: false,
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }]
        },
        animation: {
            duration: 0 // general animation time
        },
        hover: {
            animationDuration: 0 // duration of animations when hovering an item
        },
        responsiveAnimationDuration: 0, // animation duration after a resize
        elements: {
            line: {
                tension: 0 // disables bezier curves
            }
        }
    }
});



