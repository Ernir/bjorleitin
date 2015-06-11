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
        makeAlcoholPerISKChart(data);
    });

    $.get("/api/statistics/store-numbers/", function (data) {
        makeStoreNumberChart(data);
    });
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
    var styleData = [];
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
            styleData.push({
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
                data: styleData,
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

function makeStoreNumberChart(rawData) {
    // Creates one Highcharts donut chart.
    // http://www.highcharts.com/demo/pie-donut

    var colors = Highcharts.getOptions().colors;
    var regions = [];
    for (var regionName in rawData) {
        if (rawData.hasOwnProperty(regionName)) {
            regions.push(regionName);
        }
    }
    var totalCount = 0;
    var data = [];
    for (var i = 0; i < regions.length; i++) {
        var region = regions[i];
        data[i] = {
            y: 0,
            color: colors[i],
            drilldown: {
                name: region,
                data: [],
                locations: [],
                color: colors[i]
            }
        };
        for (var storeName in rawData[region]) {
            if (rawData[region].hasOwnProperty(storeName)) {
                var currentCount = rawData[region][storeName];
                data[i].y += currentCount;
                data[i].drilldown.locations.push(storeName);
                data[i].drilldown.data.push(currentCount);
                totalCount += rawData[region];
            }
        }
    }

    var regionData = [];
    var versionsData = [];
    var j;
    var k;
    var dataLen = data.length;
    var detailedCategoryDataLen;
    var brightness;

    // Build the data arrays.
    // ToDo: Combine this loop with the one above.
    for (j = 0; j < dataLen; j += 1) {

        // add region data
        regionData.push({
            name: regions[j],
            y: data[j].y,
            color: data[j].color
        });

        // add store data
        detailedCategoryDataLen = data[j].drilldown.data.length;
        for (k = 0; k < detailedCategoryDataLen; k += 1) {
            brightness = 0.2 - (k / detailedCategoryDataLen) / 5;
            versionsData.push({
                name: data[j].drilldown.locations[k],
                y: data[j].drilldown.data[k],
                color: Highcharts.Color(data[j].color).brighten(brightness).get()
            });
        }
    }

    $("#store-number-chart").highcharts({
        chart: {
            type: 'pie'
        },
        title: {
            text: 'Fjöldi bjórvörutegunda í hverri vínbúð'
        },
        plotOptions: {
            pie: {
                shadow: false,
                center: ['50%', '50%']
            }
        },
        tooltip: {
            headerFormat: "",
            pointFormatter: function () {
                if (regions.indexOf(this.name) !== -1) {
                    return this.name
                } else {
                    return this.name + ": " + this.y + " vörutegundir";
                }
            }
        },
        series: [
            {
                name: 'Landshluti',
                data: regionData,
                size: '60%',
                dataLabels: {
                    formatter: function () {
                        return this.point.name;
                    },
                    color: 'white',
                    distance: -30
                },
                animation: false
            },
            {
                name: 'Staðsetning',
                data: versionsData,
                size: '80%',
                innerSize: '60%',
                dataLabels: {
                    formatter: function () {
                        return this.point.name + ": " + this.point.y;
                    }
                },
                animation: false
            }
        ],
        credits: false
    });
}

function makeAlcoholPerISKChart(rawData) {
    var data = rawData.beers;
    for (var i = 0; i < data.length; i++) {
        data[i].ppMlAlc =  data[i].price/(data[i].volume * data[i].abv /100)
    }
    data.sort(function(a, b) {
        return a.ppMlAlc - b.ppMlAlc;
    });
    var beerNames = [];
    var ppMlAlc = [];
    for (var j = 0; j < data.length; j++) {
        beerNames[j] = data[j].name;
        ppMlAlc[j] = data[j].ppMlAlc;
    }
    $('#price-per-alcohol-ml').highcharts({
        chart: {
            type: 'bar'
        },
        title: {
            text: 'Krónur per millilítra alkóhóls í bjór'
        },
        subtitle: {
            text: "verð / (rúmmál * áfengisprósenta)"
        },
        xAxis: {
            categories: beerNames,
            title: {
                text: null
            }
        },
        yAxis: {
            min: 0,
            title: {
                text: 'kr/ml alkóhóls',
                align: 'high'
            },
            labels: {
                overflow: 'justify'
            }
        },
        tooltip: {
            headerFormat: "",
            pointFormatter: function () {
                return beerNames[this.x]
                    + ": "
                    + this.y.toFixed(2)
                    + " kr/ml alkóhóls";
            }
        },
        plotOptions: {
            bar: {
                dataLabels: {
                    enabled: true
                }
            }
        },
        legend: {
            enabled: false
        },
        credits: {
            enabled: false
        },
        series: [{
            name: 'kr/ml alkóhóls',
            data: ppMlAlc,
            animation: false,
            dataLabels: {
                format: "{point.y:.2f}"
            }
        }]
    });
}


$(initializeCharts());