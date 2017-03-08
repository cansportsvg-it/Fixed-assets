$(document).ready(function()
{
$('tbody tr').click(function () {
    $('tr').removeClass('selected');
    $(this).addClass('selected');
    selectedRow = $(this);
    document.getElementById("edit_button").disabled = false;
    document.getElementById("delete_button").disabled = false;

});

$("#edit_button").click(function () {
    var td = $(selectedRow).children('td');
        window.location.href = "../../../../itdevice/editdevice/"+td[1].innerText;
});

$("#delete_button").click(function () {
    var td = $(selectedRow).children('td');
        window.location.href = "../../../../itdevice/deletedevice/"+td[1].innerText;
});

/*

$("#edit_material").click(function () {
    var e = document.getElementById("material");
    var id = e.options[e.selectedIndex].value;
        window.location.href = "../../../../itdevice/editmaterial/"+id;
});

$("#delete_material").click(function () {
    var e = document.getElementById("material");
    var id = e.options[e.selectedIndex].value;
        window.location.href = "../../../../itdevice/deletematerial/"+id;
});*/
});