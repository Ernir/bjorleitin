/*
 Generates more or less hard-coded http://www.chartjs.org/ charts.
 */

function initializeCharts() {
    Chart.defaults.global.animation = false;

    // AJAX calls. Each chart is created on the callback.
    $.get("/api/statistics/lagers-ales/", function (data) {
        makeLagerAleChart(data);
    });
}

function makeLagerAleChart(rawData) {
    var ctx = $("#lager-ale-chart").get(0).getContext("2d");
    var baseColors = ["#F04124", "#5AD3D1"];
    var lightenedColors = ["#FF5B3E", "#74EDEB"];

    // Only two items, creating them manually.
    var chartData = [
        {
            value: rawData["lagers"],
            color: baseColors[0],
            highlight: lightenedColors[0],
            label: "Lagerbjórar"
        },
        {
            value: rawData["ales"],
            color: baseColors[1],
            highlight: lightenedColors[1],
            label: "Öl"
        }
    ];

    new Chart(ctx).Pie(chartData, {
        showScale: true,
        animateScale: true
    });
}



$(initializeCharts());