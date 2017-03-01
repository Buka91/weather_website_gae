$(function(ready){
    $('#selected_value').change(function() {
        $('input#val')[0].value = $(this).find(":selected").text();
    });
});