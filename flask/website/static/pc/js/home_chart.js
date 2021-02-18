const ctx = document.getElementById('activityChart').getContext('2d');
const week = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
function last7Days() {
    let resdate = [];
    let resstr = [];
    for (let i = 0; i < 7; i++) {
        let d = new Date();
        d.setDate(d.getDate() - i);
        if (d.getDay() - 1 === -1) {
            resstr.push(week[6])
        } else {
            resstr.push(week[d.getDay() - 1])
        }
        resdate.push(d.toJSON().slice(0, 10))
    }
    return ([resdate, resstr]);
}

const pastweek = last7Days();

function get_rides_count_at_date(day) {
    let rides = [];
    $.ajax({
        async : false,
        url: '/api/bikeeper/get_rides_from_user_at_time_with_bikeeper/' + username_home + "/" + selected_device + "/" + day,
        success: function (result) {
            rides = result;
        },
        error: function (err) {
        }
    });
    return rides.length;
}

const activityChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: pastweek[1].reverse(),
        datasets: [{
            label: 'Number of journey',
            data: [],
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
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


let rides_count = []
for (const day of pastweek[0]) {
    rides_count.push(get_rides_count_at_date(day));
}
activityChart.data.datasets[0].data = rides_count.reverse();
activityChart.update();
