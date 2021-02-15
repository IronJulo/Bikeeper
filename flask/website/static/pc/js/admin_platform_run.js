window.onload = function () {

    setInterval(function () {

        var dataCpu = [];
        var dataRam = [];
        getServerRam();
        getServerCpu();

        CpuLineChart.data.datasets.forEach((dataset) => {
            dataCpu.push(resCPU);
        });

        RamLineChart.data.datasets.forEach((dataset) => {
            dataRam.push(resRAM);
        });

        let time = new Date
        addData(RamLineChart, time.getHours() + ":" + time.getMinutes() + ":" + time.getSeconds(), dataRam);
        addData(CpuLineChart, time.getHours() + ":" + time.getMinutes() + ":" + time.getSeconds(), dataCpu);

    }, 800);

}