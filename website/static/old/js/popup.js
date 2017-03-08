$(function() {

  // contact form animations
  $('#add_button').click(function() {
    $('#add').fadeToggle();
  })
  $(document).mouseup(function (e) {
    var container = $("#add");

    if (!container.is(e.target) // if the target of the click isn't the container...
        && container.has(e.target).length === 0) // ... nor a descendant of the container
    {
        container.fadeOut();
    }
  });

    $('#edit_button').click(function() {
    $('#add').fadeToggle();
  })
  $(document).mouseup(function (e) {
    var container = $("#add");

    if (!container.is(e.target) // if the target of the click isn't the container...
        && container.has(e.target).length === 0) // ... nor a descendant of the container
    {
        container.fadeOut();
    }
  });

});
