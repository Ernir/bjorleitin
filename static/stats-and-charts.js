/*
 Generates more or less hard-coded http://www.highcharts.com/ charts.
 */

function initializeCharts() {
    // AJAX calls. Each chart is created on the callback.
    $.get("/api/statistics/style-numbers/", function (data) {
        makeStyleNumberChart(data);
    });

    $.get("/api/beers/", function (data) {
        makeAbvPriceScatterChart(data);
    })
}

function makeStyleNumberChart(rawData) {
    // Creates one Highcharts donut chart.
    // http://www.highcharts.com/demo/pie-donut

    var colors = Highcharts.getOptions().colors;
    var categories = ["Lager", "Öl"];
    var totalCount = 0;
    var data = [
        {
            y: 0,
            color: colors[0],
            drilldown: {
                name: "Lager",
                categories: [],
                data: [],
                color: colors[0]
            }
        },
        {
            y: 0,
            color: colors[1],
            drilldown: {
                name: "Öl",
                categories: [],
                data: [],
                color: colors[1]
            }
        }
    ];
    for (var styleName in rawData) {
        if (rawData.hasOwnProperty(styleName)) {
            var dataIndex;
            if (styleName.indexOf("Lager") !== -1) {
                dataIndex = 0;
            } else {
                dataIndex = 1;
            }
            data[dataIndex].y += rawData[styleName];
            data[dataIndex].drilldown.categories.push(styleName);
            data[dataIndex].drilldown.data.push(rawData[styleName]);
            totalCount += rawData[styleName];
        }
    }
    var bigCategoryData = [];
    var versionsData = [];
    var j;
    var k;
    var dataLen = data.length;
    var detailedCategoryDataLen;
    var brightness;

    // Build the data arrays.
    // ToDo: Combine this loop with the one above.
    for (j = 0; j < dataLen; j += 1) {

        // add lager/ale data
        bigCategoryData.push({
            name: categories[j],
            y: data[j].y,
            color: data[j].color
        });

        // add more detailed category data
        detailedCategoryDataLen = data[j].drilldown.data.length;
        for (k = 0; k < detailedCategoryDataLen; k += 1) {
            brightness = 0.2 - (k / detailedCategoryDataLen) / 5;
            versionsData.push({
                name: data[j].drilldown.categories[k],
                y: data[j].drilldown.data[k],
                color: Highcharts.Color(data[j].color).brighten(brightness).get()
            });
        }
    }

    $("#lager-ale-chart").highcharts({
        chart: {
            type: 'pie'
        },
        title: {
            text: 'Skipting vörutegunda Vínbúðarinnar í stíla'
        },
        plotOptions: {
            pie: {
                shadow: false,
                center: ['50%', '50%']
            }
        },
        tooltip: {
            pointFormat: 'Bjórar alls: {point.y}'
        },
        series: [
            {
                name: 'Yfirflokkar',
                data: bigCategoryData,
                size: '60%',
                dataLabels: {
                    formatter: function () {
                        var percentage = this.point.y / totalCount * 100;
                        percentage = percentage.toFixed(1);
                        return this.point.name
                            + ": "
                            + this.point.y
                            + " ("
                            + percentage
                            + "%)";
                    },
                    color: 'white',
                    distance: -30
                },
                animation: false
            },
            {
                name: 'Stíll',
                data: versionsData,
                size: '80%',
                innerSize: '60%',
                dataLabels: {
                    formatter: function () {
                        // Strips the "Lager" prefix, if any, and capitalizes.
                        var strippedName = this.point.name.replace("Lager - ", "");
                        var upperCasedName = strippedName[0].toUpperCase() + strippedName.slice(1);
                        return upperCasedName + ": " + this.point.y;
                    }
                },
                animation: false
            }
        ],
        credits: false
    });
}

function makeAbvPriceScatterChart(rawData) {

    var data = [];
    for (var i = 0; i < rawData.beers.length; i++) {
        var currentBeer = rawData.beers[i];
        if (currentBeer.container !== "Gjafaaskja") {
            data.push({
                name: currentBeer.name,
                x: Math.round((currentBeer.price / currentBeer.volume) * 1000),
                y: currentBeer.abv
            });
        }
    }

    $("#abv-price-scatter").highcharts({
        chart: {
            type: 'scatter',
            zoomType: 'xy'
        },
        title: {
            text: "Lítraverð bjóra á móti áfengisprósentu"
        },
        xAxis: {
            title: {
                enabled: true,
                text: "kr./L"
            },
            startOnTick: true,
            endOnTick: true,
            showLastLabel: true
        },
        yAxis: {
            title: {
                text: "Áfengisprósenta"
            }
        },
        plotOptions: {
            scatter: {
                marker: {
                    radius: 5,
                    states: {
                        hover: {
                            enabled: true,
                            lineColor: 'rgb(100,100,100)'
                        }
                    }
                },
                states: {
                    hover: {
                        marker: {
                            enabled: false
                        }
                    }
                },
                tooltip: {
                    headerFormat: "",
                    pointFormat: '{point.name}: {point.x} kr/L, {point.y}%'
                }
            }
        },
        series: [
            {
                name: 'Bjórar',
                color: 'rgba(223, 83, 83, .5)',
                data: data,
                animation: false
            }
        ],
        credits: false,
        animation: false
    });
}


$(initializeCharts());