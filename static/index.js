/*
 Functions and objects related to the core of the filtering functionality
 */

var filterVals = {
    name: "",
    brewery: ""
};

function updateFilters() {
    filterVals.name = $("#beer-name-filter").val();
    filterVals.brewery = $("#brewery-name-filter").val();
}

function performFiltering() {
    $.each(allBeerData, function (i, beer) {
        var $row = $("#row-" + beer.productId);

        var display = nameFilter(beer.name) && breweryFilter(beer.brewery);

        if (display) {
            $row.show();
        } else {
            $row.hide();
        }
    });
}

function nameFilter(text) {
    return text.toLowerCase().indexOf(filterVals.name.toLowerCase()) !== -1
}
function breweryFilter(text) {
    return text.toLowerCase().indexOf(filterVals.brewery.toLowerCase()) !== -1
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
}

function applyListeners() {
    $("#beer-name-filter").keyup(function () {
        updateFilters();
        performFiltering();
    });
    $("#brewery-name-filter").keyup(function () {
        updateFilters();
        performFiltering();
    });
}

$(initialize());
