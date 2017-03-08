  $( function() {
    $( "#start_date" ).datepicker({
                // Consistent format with the HTML5 picker
                    dateFormat : 'yy-mm-dd'
                },
                // Localization
                $.datepicker.regional['us']);
    $( "#end_date" ).datepicker({
                // Consistent format with the HTML5 picker
                    dateFormat : 'yy-mm-dd'
                },
                // Localization
                $.datepicker.regional['us']);
     $( "#pur_date" ).datepicker({
                // Consistent format with the HTML5 picker
                    dateFormat : 'yy-mm-dd'
                },
                // Localization
                $.datepicker.regional['us']);
  } );