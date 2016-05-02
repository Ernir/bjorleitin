/*
 Functions and objects related to the core of the filtering functionality
 */

var filterVals = {
    name: ""
};

function updateFilters() {
    filterVals.name = $("#beer-name-filter").val();
}

function performFiltering() {
    $.each(allBeerData, function (i, beer) {
        var $row = $("#row-" + beer.productId);

        var display = nameFilter(beer.name);

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

/*
 Functions and objects to initialize the page
 */

var tableLoaded = false;
var allBeerData;

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
    })
}

function initialize() {
    makeBeerTable();
    getDataSet();
    applyListeners();
}

function applyListeners() {
    $("#beer-name-filter").keyup(function () {
        updateFilters();
        performFiltering();
    });
}

$(initialize());
