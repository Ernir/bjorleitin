/*
 Override default form behaviour
 */

$('#main-form').on('submit', function (event) {
    event.preventDefault();
    getBeers();
});
