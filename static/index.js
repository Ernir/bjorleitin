/*
 Functions and objects related to the core of the filtering functionality
 */

var filterVals = {
    name: "",
    brewery: "",
    minPrice: -Infinity,
    maxPrice: Infinity,
    minAbv: -Infinity,
    maxAbv: Infinity,
    minVol: -Infinity,
    maxVol: Infinity,
    styles: []
};

function updateFilters() {
    filterVals.name = $("#beer-name-filter").val();
    filterVals.brewery = $("#brewery-name-filter").val();
    filterVals.minAbv = parseInt($("#abv-min-filter").text());
    filterVals.maxAbv = parseInt($("#abv-max-filter").text());
    filterVals.minPrice = parseInt($("#price-min-filter").text());
    filterVals.maxPrice = parseInt($("#price-max-filter").text());
    filterVals.minVol = parseInt($("#volume-min-filter").text());
    filterVals.maxVol = parseInt($("#volume-max-filter").text());
    filterVals.styles = [];
    $(".checkbox label input:checked").each(function (i) {
        filterVals.styles.push($(this).val())
    });
}

function performFiltering() {
    $.each(allBeerData, function (i, beer) {
        var $row = $("#row-" + beer.productId);

        var display = nameFilter(beer.name)
            && breweryFilter(beer.brewery)
            && priceFilter(beer.minPrice, beer.maxPrice)
            && abvFilter(beer.abv)
            && volumeFilter(beer.minVolume, beer.maxVolume)
            && styleFilter(beer.style);

        if (display) {
            $row.show();
        } else {
            $row.hide();
        }
    });
    applyStripes();
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
function volumeFilter(beerMinimumVolume, beerMaximumVolume) {
    return beerMinimumVolume <= filterVals.maxVol && filterVals.minVol <= beerMaximumVolume;
}
function styleFilter(beerStyle) {
    if (filterVals.styles.length === 0) {
        return true;
    }
    return filterVals.styles.indexOf(beerStyle) !== -1;
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
var beerVolumes = [];

function makeBeerTable() {
    /*
     One initial AJAX call to create the list of beers.
     */
    $.get("/v2/main-table/", function (data) {
        var $tableContainer = $("#table-container");
        $tableContainer.html(data);
        $("table").tablesorter();
        $tableContainer.fadeIn("slow", function () {
            applyStripes();
        });
    });
}
function applyStripes() {
    // Normal bootstrap table-striped malfunctions when rows are hidden. Here's a fix.
    // Source: http://stackoverflow.com/a/24637866/1675015
    $("tr:visible").each(function (index) {
        $(this).toggleClass("stripe", !!(index & 1));
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
            if (beerVolumes.indexOf(beer.maxVolume) === -1) {
                beerVolumes.push(beer.maxVolume);
            }
            if (beerVolumes.indexOf(beer.minVolume) === -1) {
                beerVolumes.push(beer.minVolume);
            }
        });
        beerPrices.sort(saneSort);
        beerAbvs.sort(saneSort);
        beerVolumes.sort(saneSort);
        prepareSearchForm();
    });

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
    makeVolumeSlider(beerVolumes);
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

function makeVolumeSlider(volumes) {
    $("#volume-slider").slider({
        range: true,
        min: 0,
        max: volumes.length - 1,
        values: [0, volumes.length - 1],
        slide: function (event, ui) {
            var minVolume = volumes[ui.values[0]];
            var maxVolume = volumes[ui.values[1]];
            $("#volume-min-filter").text(minVolume);
            $("#volume-max-filter").text(maxVolume);
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
    $(".checkbox label input").on("click", function () {
        updateFilters();
        performFiltering();
    });
}

$(initialize());
