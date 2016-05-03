/*
 Functions and objects related to the core of the filtering functionality
 */

var filterVals = {
    name: "",
    brewery: "",
    minPrice: -Infinity,
    maxPrice: Infinity,
    minAbv: -Infinity,
    maxAbv: Infinity
};

function updateFilters() {
    filterVals.name = $("#beer-name-filter").val();
    filterVals.brewery = $("#brewery-name-filter").val();
    filterVals.minAbv = parseInt($("#abv-min-filter").text());
    filterVals.maxAbv = parseInt($("#abv-max-filter").text());
    filterVals.minPrice = parseInt($("#price-min-filter").text());
    filterVals.maxPrice = parseInt($("#price-max-filter").text());
}

function performFiltering() {
    $.each(allBeerData, function (i, beer) {
        var $row = $("#row-" + beer.productId);

        var display = nameFilter(beer.name)
            && breweryFilter(beer.brewery)
            && priceFilter(beer.minPrice, beer.maxPrice)
            && abvFilter(beer.abv);

        if (display) {
            $row.show();
        } else {
            $row.hide();
        }
    });
}

function nameFilter(beerName) {
    return beerName.toLowerCase().indexOf(filterVals.name.toLowerCase()) !== -1
}
function breweryFilter(breweryName) {
    return breweryName.toLowerCase().indexOf(filterVals.brewery.toLowerCase()) !== -1
}
function priceFilter(beerMinimumPrice, beerMaximumPrice) {
    return beerMinimumPrice <= filterVals.maxPrice && filterVals.minPrice <= beerMaximumPrice;
}
function abvFilter(beerAbv) {
    return beerAbv <= filterVals.maxAbv && filterVals.minAbv <= beerAbv;
}
/*
 Functions and objects to initialize the page
 */

var tableLoaded = false;
var allBeerData;
var beerNames = [];
var beerAbvs = [];
var beerPrices = [];
var breweryNames = [];

function makeBeerTable() {
    /*
     One initial AJAX call to create the list of beers.
     */
    $.get("/v2/main-table/", function (data) {
        var $tableContainer = $("#table-container");
        $tableContainer.html(data);
        $("table").tablesorter();
        $tableContainer.fadeIn("slow", function () {
            tableLoaded = true;
        });
    });
}

function getDataSet() {
    /*
     Get the list of beers in JSON format
     */

    $.get("/v2/main-table/json/", function (data) {
        allBeerData = data.beers;
        $.each(allBeerData, function (i, beer) {
            beerNames.push(beer.name);
            if (beerAbvs.indexOf(beer.abv)) {
                beerAbvs.push(beer.abv)
            }
            if (beerPrices.indexOf(beer.minPrice) === -1) {
                beerPrices.push(beer.minPrice);
            }
            if (beerPrices.indexOf(beer.maxPrice) === -1) {
                beerPrices.push(beer.maxPrice);
            }
            if (breweryNames.indexOf(beer.brewery) === -1) {
                breweryNames.push(beer.brewery);
            }
        });
        beerPrices.sort(saneSort);
        beerAbvs.sort(saneSort);
        prepareSearchForm();
    })

    function saneSort(a, b) {
        return a - b;
    }
}

function initialize() {
    makeBeerTable();
    getDataSet();
    applyListeners();
}

function prepareSearchForm() {
    $("#beer-name-filter").typeahead({source: beerNames});
    $("#brewery-name-filter").typeahead({source: breweryNames});
    makePriceSlider(beerPrices);
    makeAbvSlider(beerAbvs);
}

function makePriceSlider(prices) {
    $("#price-slider").slider({
        range: true,
        min: 0,
        max: prices.length - 1,
        values: [0, prices.length - 1],
        slide: function (event, ui) {
            var minPrice = prices[ui.values[0]];
            var maxPrice = prices[ui.values[1]];
            $("#price-min-filter").text(minPrice);
            $("#price-max-filter").text(maxPrice);
            updateFilters();
            performFiltering();
        }
    });
}

function makeAbvSlider(abvs) {
    $("#abv-slider").slider({
        range: true,
        min: 0,
        max: abvs.length - 1,
        values: [0, abvs.length - 1],
        slide: function (event, ui) {
            var minAbv = abvs[ui.values[0]];
            var maxAbv = abvs[ui.values[1]];
            $("#abv-min-filter").text(minAbv);
            $("#abv-max-filter").text(maxAbv);
            updateFilters();
            performFiltering();
        }
    });
}

function applyListeners() {
    $("#beer-name-filter, #brewery-name-filter").keyup(function () {
        updateFilters();
        performFiltering();
    });
}

$(initialize());
