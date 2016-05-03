/*
 Functions and objects related to the core of the filtering functionality
 */

var filterVals = {
    name: "",
    brewery: "",
    minPrice: -Infinity,
    maxPrice: Infinity
};

function updateFilters() {
    filterVals.name = $("#beer-name-filter").val();
    filterVals.brewery = $("#brewery-name-filter").val();
    filterVals.minPrice = parseInt($("#price-min-filter").text());
    filterVals.maxPrice = parseInt($("#price-max-filter").text());
}

function performFiltering() {
    $.each(allBeerData, function (i, beer) {
        var $row = $("#row-" + beer.productId);

        var display = nameFilter(beer.name)
            && breweryFilter(beer.brewery)
            && priceFilter(beer.minPrice, beer.maxPrice);

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
    return beerMinimumPrice < filterVals.maxPrice && filterVals.minPrice < beerMaximumPrice;
}

/*
 Functions and objects to initialize the page
 */

var tableLoaded = false;
var allBeerData;
var beerNames = [];
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
        beerPrices.sort(function (a, b) {
            return a - b;
        });
        prepareSearchForm();
    })
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

function applyListeners() {
    $("#beer-name-filter, #brewery-name-filter").keyup(function () {
        updateFilters();
        performFiltering();
    });
}

$(initialize());
