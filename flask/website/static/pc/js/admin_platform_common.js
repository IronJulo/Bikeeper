const maximumPoints = 10;

function addData(chart, label, data) {
    chart.data.labels.push(label);
    chart.data.datasets.forEach((dataset) => {
        var d = data[0];
        dataset.data.push(d);
        data.shift();
    });


    var canRemoveData = false;
    chart.data.datasets.forEach((dataset) => {
        if (dataset.data.length > maximumPoints) {

            if (!canRemoveData) {
                canRemoveData = true;
                chart.data.labels.shift();
            }

            dataset.data.shift();

        }

    });

    chart.update();
}

