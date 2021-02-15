var ctx = document.getElementById('cpu').getContext('2d');
var gradientStroke = ctx.createLinearGradient(0, 0,300,300);
gradientStroke.addColorStop(0, "#2CE7E1");
gradientStroke.addColorStop(1, "#1CBDF8");
var myChart = new Chart(ctx, {
    type: 'line',
    title: 'Speed',
    data: {
        labels: ['10.00', '10.30', '11.00', '11.30', '12.00', '12.30','13.00'],
        datasets: [{
            fill: false,
            label: 'speed',
            data: [12, 19, 3, 5, 2, 3,28,52],
            borderColor: gradientStroke,
            pointBackgroundColor: "white",
            borderWidth: 2,
            pointBorderWidth:3,
            lineTension: 0,
        }]
    },
    options: {
        legend: { display: false },
        scales: {
            yAxes: [{
                scaleLabel: {
                    display: true,
                    labelString: 'Load',
                    fontSize: 20,
                    fontStyle: "bold",
                    fontColor: "black",
                    
                },
                position: 'top',
                ticks: {
                    beginAtZero: true
                },
            }],
            xAxes: [{ 
                scaleLabel: {
                    display: true,
                    labelString: 'Time',
                    fontSize: 20,
                    fontStyle: "bold",
                    fontColor: "black",
                },
                
                position: "right"
            }],
        },
        elements: {
            point: {
                radius: 6
            }
        }
    }
});

var ctx = document.getElementById('ram').getContext('2d');
var gradientStroke = ctx.createLinearGradient(0, 0,300,300);
gradientStroke.addColorStop(0, "#2CE7E1");
gradientStroke.addColorStop(1, "#1CBDF8");
var myChart = new Chart(ctx, {
    type: 'line',
    title: 'Speed',
    data: {
        labels: ['10.00', '10.30', '11.00', '11.30', '12.00', '12.30','13.00'],
        datasets: [{
            fill: false,
            label: 'speed',
            data: [12, 19, 3, 5, 2, 3,28,52],
            borderColor: gradientStroke,
            pointBackgroundColor: "white",
            borderWidth: 2,
            pointBorderWidth:3,
            lineTension: 0,
        }]
    },
    options: {
        legend: { display: false },
        scales: {
            yAxes: [{
                scaleLabel: {
                    display: true,
                    labelString: 'Load',
                    fontSize: 20,
                    fontStyle: "bold",
                    fontColor: "black",
                    
                },
                position: 'top',
                ticks: {
                    beginAtZero: true
                },
            }],
            xAxes: [{ 
                scaleLabel: {
                    display: true,
                    labelString: 'Time',
                    fontSize: 20,
                    fontStyle: "bold",
                    fontColor: "black",
                },
                
                position: "right"
            }],
        },
        elements: {
            point: {
                radius: 6
            }
        }
    }
});