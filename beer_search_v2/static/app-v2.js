function makeBeerTable() {
    /*
     One initial AJAX call to create the list of beers.
     */
    $.get("/v2/main-table/", function (data) {
        var $tableContainer = $("#table-container");
        $tableContainer.html(data);
        $("table").tablesorter();
        $tableContainer.fadeIn("slow", function () {
            // ToDo continue dependent initialization
        });
    });
}

function initialize() {
    makeBeerTable()
}

$(initialize());
