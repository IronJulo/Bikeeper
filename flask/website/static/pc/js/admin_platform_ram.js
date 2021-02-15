var resRAM = 0


function getServerRam() {
    $.ajax({
        url: "/api/stats/ram",
        success: function (result) {
            resRAM = result.response;
        },
        error: function (err) {
        }
    });
}


var canvasRAM = document.getElementById('ram');
var ctxRAM = canvasRAM.getContext('2d');

var RamLineChart = new Chart(ctxRAM, {
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
                label: 'RAM Usage in percent',
                backgroundColor: "#36a2eb88",
                borderColor: "#36a2eb",
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
            duration: 0
        },
        hover: {
            animationDuration: 0
        },
        responsiveAnimationDuration: 0,
        elements: {
            line: {
                tension: 0
            }
        }
    }
});

