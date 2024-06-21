function editor_refresh_rendering(_id){
    $("#my_image").attr("src","second.jpg");
}
function load_editor_for_device(_id){
     alert('Geklicktes Item: ' + _id); // Beispielaktion
} 
function load_available_devices(){
    $('#inkberry_available_devices_dropdown_menu').empty();

    $.getJSON("/api/list_devices", function( data ) {
      $.each( data['devices'], function( key, val ) {
            var item = $('<a>', {
            class: 'dropdown-item',
            text: val['name']
        }).data("data-device_id", val['id']);
        $('#inkberry_available_devices_dropdown_menu').append(item);
      });

      $('#inkberry_available_devices_dropdown_menu').on('click', '.dropdown-item', function(event) {
        event.preventDefault();
        var clicked_id = $(this).data('data-device_id');
        load_editor_for_device(clicked_id);
      });
    });
    }

function inkberry_init(){
    load_available_devices();
}
    