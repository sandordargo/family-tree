function show_date() {
    document.getElementById('demo').innerHTML = Date();
}

function add_row() {
    var table = document.getElementById("properties");
    var number_of_rows = table.rows.length
    var row = table.insertRow(number_of_rows);
    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    var cell3 = row.insertCell(2);
    if (table.rows[number_of_rows-1].cells[0].innerHTML.startsWith("<input name")) {
        prop_index = table.rows[number_of_rows-1].cells[0].innerHTML.indexOf("propertyname")
        last_prop_label = table.rows[number_of_rows-1].cells[0].innerHTML.match(/"propertyname[0-9]*"/)
        last_prop_number = last_prop_label.toString().substring(13, last_prop_label.toString().length-1)

        next_prop_number = parseInt(last_prop_number) + 1;
        cell1.innerHTML = "<input name='propertyname".concat(next_prop_number, "' value='propertynamevalue", next_prop_number, "'>");
        cell2.innerHTML = "<input name='propertyvalue".concat(next_prop_number, "' value='propertyvaluevalue", next_prop_number, "'>");
        cell3.innerHTML = "<button class='btn btn-danger' type='button' onclick='markRowForDeletion(this)'> Delete row </button>";
    }
    else {
        cell1.innerHTML = "<input name='propertyname".concat(1, "' value='propertynamevalue", 1, "'>");
        cell2.innerHTML = "<input name='propertyvalue".concat(1, "' value='propertyvaluevalue", 1, "'>");
        cell3.innerHTML = "<button class='btn btn-danger' type='button' onclick='markRowForDeletion(this)'> Delete row </button>";
    }
}

function markRowForDeletion(element) {
    var rowId = element.parentNode.parentNode.rowIndex;
    var table = document.getElementById("properties");
    table.deleteRow(rowId);
}

