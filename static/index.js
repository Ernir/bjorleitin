/*
 Functions and objects related to the core of the filtering functionality
 */

function updateAndFilter() {
    // Initializing a default object of values which will be compared to each successive product, to determine if that
    // particular product should be included in a final list.
    var filterVals = {
        names: [],
        breweries: [],
        minPrice: -Infinity,
        maxPrice: Infinity,
        minAbv: -Infinity,
        maxAbv: Infinity,
        minVol: -Infinity,
        maxVol: Infinity,
        styles: [],
        minUntappd: -Infinity,
        maxUntappd: Infinity,
        containers: ["flaska", "dós"],
        countries: [],
        stores: []
    };

    // Finding all beer names, breweries, styles, countries and stores selected by the user.
    filterVals.names = [];
    $("#beer-name-filter").find("option:selected").each(function (i) {
        filterVals.names.push($(this).val());
    });
    filterVals.breweries = [];
    $("#brewery-name-filter").find("option:selected").each(function (i) {
        filterVals.breweries.push($(this).val());
    });
    filterVals.styles = [];
    $("#style-filter").find("option:selected").each(function (i) {
        filterVals.styles.push($(this).val());
    });
    filterVals.countries = [];
    $("#country-name-filter").find("option:selected").each(function (i) {
        filterVals.countries.push($(this).val())
    });
    filterVals.stores = [];
    $("#store-name-filter").find("option:selected").each(function (i) {
        filterVals.stores.push($(this).val())
    });

    // Finding the extreme values of ABV, price, volume and Untappd Rating selected by the user.
    filterVals.minAbv = parseFloat($("#abv-min-filter").text().replace(",", "."));
    filterVals.maxAbv = parseFloat($("#abv-max-filter").text().replace(",", "."));
    filterVals.minPrice = parseInt($("#price-min-filter").text());
    filterVals.maxPrice = parseInt($("#price-max-filter").text());
    filterVals.minVol = parseInt($("#volume-min-filter").text());
    filterVals.maxVol = parseInt($("#volume-max-filter").text());
    filterVals.minUntappd = parseFloat($("#untappd-min-filter").text());
    filterVals.maxUntappd = parseFloat($("#untappd-max-filter").text());

    filterVals.containers = [];
    $(".container-filter:checked").each(function (i) {
        filterVals.containers.push($(this).val().toLowerCase());
    });

    var numResults = 0;
    $.each(allBeerData, function (i, beer) {
        var $row = $("#row-" + beer.productId);

        var display = nameFilter(beer.name)
            && breweryFilter(beer.brewery)
            && priceFilter(beer.minPrice, beer.maxPrice)
            && abvFilter(beer.abv)
            && volumeFilter(beer.minVolume, beer.maxVolume)
            && styleFilter(beer.style)
            && untappdFilter(beer.untappdRating)
            && containerFilter(beer.containers)
            && countryFilter(beer.country)
            && storeFilter(beer.stores);

        if (display) {
            numResults += 1;
            $row.show();
        } else {
            $row.hide();
        }
    });
    updateDisplays(numResults);
    applyStripes();

    function nameFilter(beerName) {
        if (filterVals.names.length === 0) {
            return true;
        }
        return filterVals.names.indexOf(beerName) !== -1;
    }

    function breweryFilter(breweryName) {
        if (filterVals.breweries.length === 0) {
            return true;
        }
        return filterVals.breweries.indexOf(breweryName) !== -1;
    }

    function priceFilter(beerMinimumPrice, beerMaximumPrice) {
        return beerMinimumPrice <= filterVals.maxPrice && filterVals.minPrice <= beerMaximumPrice;
    }

    function abvFilter(beerAbv) {
        return filterVals.minAbv <= beerAbv && beerAbv <= filterVals.maxAbv;
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

    function untappdFilter(beerRating) {
        if (beerRating != undefined) {
            return filterVals.minUntappd <= beerRating && beerRating <= filterVals.maxUntappd;
        }
        return filterVals.minUntappd === 0 && filterVals.maxUntappd == 5;
    }

    function containerFilter(containers) {
        // This would be a nice place for array.includes, but browser support is lacking.
        for (var i = 0; i < containers.length; i++) {
            if (filterVals.containers.indexOf(containers[i].toLowerCase()) !== -1) {
                return true;
            }
        }
        return false;
    }

    function countryFilter(countryName) {
        if (filterVals.countries.length === 0) {
            return true;
        }
        return filterVals.countries.indexOf(countryName) !== -1;
    }

    function storeFilter(stores) {
        if (filterVals.stores.length === 0) {
            return true;
        }
        for (var i = 0; i < stores.length; i++) {
            if (filterVals.stores.indexOf(stores[i]) !== -1) {
                return true;
            }
        }
        return false;
    }
}

/*
 Helpers for displaying the results
 */

function updateDisplays(numResults) {
    // Handling the messages
    if (numResults === 0) {
        showMessage("#results-none");
    } else {
        if (numResults % 10 !== 1 || numResults === 11) {
            $("#results-found").text(numResults + " bjórar fundust.");
        } else { // Result of the form 1+10k, k=0, 2, 3, 4, ...
            $("#results-found").text(numResults + " bjór fannst");
        }
        showMessage("#results-found");
    }
}

function showMessage(id) {
    $(".search-alert").hide();
    $(id).show();
}

/*
 Functions and objects to initialize the page
 */

var allBeerData = [];
var beerNames = [];
var breweryNames = [];
var styleNames = [];
var beerAbvs = [];
var beerPrices = [];
var beerVolumes = [];
var countryNames = [];
var storeNames = [];

function makeBeerTable() {
    /*
     One initial AJAX call to create the list of beers.
     */
    showMessage("#results-working");
    $.get("/main-table/", function (data) {
        var $tableContainer = $("#table-container");
        $tableContainer.html(data);
        var $tables = $("table");
        $tables.tablesorter();
        $tables.bind("sortEnd", applyStripes);
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
    $.get("/main-table/json/", function (data) {
        allBeerData = data.beers;
        $.each(allBeerData, function (i, beer) {
            beerNames.push(beer.name);
            if (breweryNames.indexOf(beer.brewery) === -1) {
                breweryNames.push(beer.brewery);
            }
            if (styleNames.indexOf(beer.style) === -1) {
                styleNames.push(beer.style);
            }
            if (beerAbvs.indexOf(beer.abv)) {
                beerAbvs.push(beer.abv)
            }
            if (beerPrices.indexOf(beer.minPrice) === -1) {
                beerPrices.push(beer.minPrice);
            }
            if (beerPrices.indexOf(beer.maxPrice) === -1) {
                beerPrices.push(beer.maxPrice);
            }
            if (beerVolumes.indexOf(beer.maxVolume) === -1) {
                beerVolumes.push(beer.maxVolume);
            }
            if (beerVolumes.indexOf(beer.minVolume) === -1) {
                beerVolumes.push(beer.minVolume);
            }
            if (countryNames.indexOf(beer.country) === -1) {
                countryNames.push(beer.country);
            }
            for (var i = 0; i < beer.stores.length; i++) { // ToDo: find a more efficient way to get all store names
                if (storeNames.indexOf(beer.stores[i]) === -1) {
                    storeNames.push(beer.stores[i]);
                }
            }
        });
        beerPrices.sort(saneSort);
        beerAbvs.sort(saneSort);
        beerVolumes.sort(saneSort);
        storeNames.sort();
        breweryNames.sort();
        styleNames.sort();
        countryNames.sort();
        deferredInitializeSearchForm();
        updateDisplays(allBeerData.length)
    });

    function saneSort(a, b) {
        return a - b;
    }
}

function initialize() {
    $("select").select2({
            theme: "bootstrap",
            containerCssClass: ":all:"
        }
    ); // These values are later overridden in deferredInitializeSearchForm.
    makeBeerTable();
    getDataSet();
    applyListeners();
}

function deferredInitializeSearchForm() {

    var selectIds = ["#beer-name-filter", "#brewery-name-filter", "#style-filter", "#country-name-filter",
        "#store-name-filter"
    ];
    var placeholders = ["Nafn bjórs", "Nafn brugghúss", "Nafn stíls", "Nafn upprunalands", "Sölustaður eða vörulisti"];
    var datasources = [beerNames, breweryNames, styleNames, countryNames, storeNames];

    for (var i = 0; i < selectIds.length; i++) {
        $(selectIds[i]).select2({
            theme: "bootstrap",
            containerCssClass: ":all:",
            placeholder: placeholders[i],
            data: datasources[i]
        });
    }

    makePriceSlider(beerPrices);
    makeAbvSlider(beerAbvs);
    makeVolumeSlider(beerVolumes);
    makeUntappdSlider();
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
            updateAndFilter();
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
            updateAndFilter();
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
            updateAndFilter();
        }
    });
}

function makeUntappdSlider() {
    $("#untappd-slider").slider({
        range: true,
        min: 0, // Ratings are on a scale of 0 to 5 stars
        max: 5,
        step: 0.01,
        values: [0, 5],
        slide: function (event, ui) {
            $("#untappd-min-filter").text(ui.values[0]);
            $("#untappd-max-filter").text(ui.values[1]);
            updateAndFilter();
        }
    });
}

function applyListeners() {
    $("#beer-name-filter, #brewery-name-filter, #country-name-filter, #store-name-filter").keyup(function () {
        updateAndFilter();
    });
    $("select").change(function () {
        updateAndFilter();
    });
    $(".checkbox label input").on("click", function () {
        updateAndFilter();
    });

    $(".container-button").on("click", function () {
        $(this).toggleClass("active");
        updateAndFilter();
    })
}

$(initialize());
