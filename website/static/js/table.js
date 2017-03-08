$(document).ready(function()
{
  // swal("Here's a message!")
  $('.upload-btn input').on('change', function(){
  $(this).parent().find('span').html($(this).val());
});
$('tbody tr').click(function () {
    $('tr').removeClass('selected');
    $(this).addClass('selected');
    selectedRow = $(this);
    document.getElementById("edit_button").disabled = false;
    document.getElementById("delete_button").disabled=false;

});
$("#edit_button").click(function () {
    var td = $(selectedRow).children('td');
        window.location.href = "../../../../itdevice/editdevice/"+td[1].innerText;
});

$("#date_filter_btn").click(function () {
    var start_date = $( "#start_date" ).val();
    var end_date = $( "#end_date" ).val();
    if (start_date && end_date){
        location.href='/itdevice/date/'+start_date+'/'+end_date
    }
    else{
        swal("Please enter start & end date!")
    }
});

$("#delete_button").click(function () {
    var td = $(selectedRow).children('td');
        window.location.href = "../../../../itdevice/deletedevice/"+td[1].innerText;
});
});
$(document).on('click', 'th', function() {
        var table = $(this).parents('table').eq(0);
        var rows = table.find('tr:gt(0)').toArray().sort(comparer($(this).index()));
        this.asc = !this.asc;
        if (!this.asc) {
            rows = rows.reverse();
        }
        table.children('tbody').empty().html(rows);
        $('tbody tr').click(function () {
    $('tr').removeClass('selected');
    $(this).addClass('selected');
    selectedRow = $(this);
    document.getElementById("edit_button").disabled = false;
    document.getElementById("delete_button").disabled=false;

});
    });

    function comparer(index) {
        return function(a, b) {
            var valA = getCellValue(a, index),
                valB = getCellValue(b, index);
            return $.isNumeric(valA) && $.isNumeric(valB) ?
                valA - valB : valA.localeCompare(valB);
        };
    }
    function getCellValue(row, index) {
        return $(row).children('td').eq(index).text();
    }

