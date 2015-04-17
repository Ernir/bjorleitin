/*
 Code handling the search form AJAX.
 Mostly verbatim from here:
 https://realpython.com/blog/python/django-and-ajax-form-submissions/
 */

"use strict";

// This function gets cookie with a given name
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

/*
 The functions below will create a header with csrftoken
 */

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

// Main AJAX function
var xhr;
function getBeers() {
    showMessage("#results-working");
    if (xhr) { // If we were already requesting data, start over.
        xhr.abort();
    }
    xhr = $.ajax({
        url: "/api/leit/",
        type: "post",
        data: $("#main-form").serialize(),

        success: function (json) {
            displayResults(json);
        },

        error: function (xhr, errmsg, err) {
            if (errmsg !== "abort") { // Aborts don't count.
                showMessage("#results-error");
            }
        }
    });
}

function displayResults(jsonData) {

    var numResults = jsonData.length;

    // Handling the messages
    if (numResults === 0) {
        showMessage("#results-none");
    } else {
        if (numResults % 10 !== 1 || numResults === 11) {
            $("#results-found").text(numResults + " bjórar fundust.");
        } else { // Result on the form 1+10k, k=0, 2, 3, 4, ...
            $("#results-found").text(numResults + " bjór fannst");
        }
        showMessage("#results-found");
    }

    // Writing out the lists
    var $results = $("#results-list");
    $results.empty();
    for (var i = 0; i < jsonData.length; i++) {
        $results.append("<li><a href='http://www.vinbudin.is/DesktopDefault.aspx/tabid-54?productID=" + jsonData[i].atvr_id + "'>" + jsonData[i].name + "</a> " + jsonData[i].suffix + "</li>");
    }
}

function showMessage(id) {
    $(".alert").hide();
    $(id).show();
}

/*
 Listeners
 */
$("input[type=checkbox],input[type=number]").change(getBeers);

// Delayed calls for the text box.
// Source: http://stackoverflow.com/a/23569018/1675015
var requestTimer;
$("input[type=text],input[type=number]").keyup(requestLater);

function requestLater() {
    showMessage("#results-working");
    if (requestTimer) {
        window.clearTimeout(requestTimer);
    }
    if (xhr) {
        xhr.abort();
    }
    requestTimer = setTimeout(getBeers, 1000);
}

// Override for normal form behaviour
$('#main-form').on('submit', function (event) {
    event.preventDefault();
    getBeers();
});

/*
 Sliders
 */

function makeSliders() {
    // ToDo: Combine into one function call.
    $.get("/api/gildi/rummal/", function (data) {
        makeVolumeSlider(data);
    });
    $.get("/api/gildi/verd/", function (data) {
        makePriceSlider(data);
    });
    makeAbvSlider();
}

function makeVolumeSlider(volumes) {
    $("#volume-slider").slider({
        range: true,
        min: 0,
        max: volumes.length - 1,
        values: [0, volumes.length - 1],
        slide: function (event, ui) {
            $("#id_min_volume").val(volumes[ui.values[0]]);
            $("#id_max_volume").val(volumes[ui.values[1]]);
            requestLater();
        }
    });
}

function makePriceSlider(prices) {
    $("#price-slider").slider({
        range: true,
        min: 0,
        max: prices.length - 1,
        values: [0, prices.length - 1],
        slide: function (event, ui) {
            $("#id_min_price").val(prices[ui.values[0]]);
            $("#id_max_price").val(prices[ui.values[1]]);
            requestLater();
        }
    });
}

function makeAbvSlider() {
    var abvs = {
        min: parseFloat($("#id_min_abv").val()),
        max: parseFloat($("#id_max_abv").val())
    };
    $("#abv-slider").slider({
        range: true,
        min: abvs.min,
        max: abvs.max,
        step: 0.1,
        values: [abvs.min, abvs.max],
        slide: function (event, ui) {
            $("#id_min_abv").val(ui.values[0]);
            $("#id_max_abv").val(ui.values[1]);
            requestLater();
        }
    });
    // TODO finish
}

/*
 Initialization
 */

function initialize() {
    makeSliders();
    getBeers();
    $("table").tablesorter();
}
$(initialize());