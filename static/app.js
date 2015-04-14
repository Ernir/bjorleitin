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
    xhr = $.ajax({
        url: "/api/leit/",
        type: "post",
        data: $("#main-form").serialize(),

        success: function (json) {
            updateResults(json);
        },

        error: function (xhr, errmsg, err) {
            showMessage("#results-error");
        }
    });
}

function updateResults(jsonData) {

    var numResults = jsonData.length;

    // Handling the messages
    if (numResults === 0) {
        showMessage("#results-none");
    } else {
        if (numResults % 10 !== 1) {
            $("#results-found").text(numResults + " bjórar fundust.");
        } else { // Result on the form 1+10k, k=0, 1, 2 ...
            $("#results-found").text(numResults + " bjór fannst");
        }
        showMessage("#results-found");
    }

    // Writing out the lists
    var $results = $("#results-list");
    $results.empty();
    for (var i = 0; i < jsonData.length; i++) {
        $results.append("<li><a href='http://www.vinbudin.is/DesktopDefault.aspx/tabid-54?productID=" + jsonData[i].atvr_id + "'>" + jsonData[i].unique_name + "</a></li>");
    }
}

function showMessage(id) {
    $(".alert").hide();
    $(id).show();
}

/*
 Listeners
 */
$("input[type=checkbox]").change(getBeers);

// Delayed calls for the text box.
// Source: http://stackoverflow.com/a/23569018/1675015
var requestTimer;
$("input[type=text]").keyup(function () {
    showMessage("#results-working");
    if (requestTimer) {
        window.clearTimeout(requestTimer);
    }
    if (xhr) {
        xhr.abort();
    }
    requestTimer = setTimeout(getBeers, 1000);
});

// Override for normal form behaviour
$('#main-form').on('submit', function (event) {
    event.preventDefault();
    getBeers();
});

/*
 Initialization
 */

function initialize() {
    getBeers();
    $("table").tablesorter();
}
$(initialize());