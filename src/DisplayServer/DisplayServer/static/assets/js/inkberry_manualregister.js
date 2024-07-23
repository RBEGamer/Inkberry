function redirect_to_real_setup(){
    
    var hardware_type_id = $("#inkberry_setup_user_parent_display_id_display_button").html();
    
    var inkberry_screen_id = $("#inkberry_screen_id").val();
    
    if(!inkberry_screen_id || !hardware_type_id || hardware_type_id.includes("_") || hardware_type_id.includes(" ") || inkberry_screen_id.includes(" ")){
        alert("Please fill id and type field in. Please note: Without any spaces dashes or underscores");
        return;
    }
    
    window.location.href = "/static/register.html?did=" + inkberry_screen_id + "&hardware_type=" + hardware_type_id;    
}

function inkberry_init(){

    var did = getAllUrlParams().did;
    if(did != undefined && did){
        $("#inkberry_screen_id").val(did);
    }
    
        
    $.getJSON("/api/list_hardware_types", function( data ) {
      $.each( data['hardware_type'], function( key, val ) {
            var item = $('<a>', {
            class: 'dropdown-item',
            text: val['name']
        }).data("data-possible_parent_device_id", val['id']);
        $('#inkberry_setup_dropdown_possible_parent_devices').append(item);
      });
    });
    
    $('#inkberry_setup_dropdown_possible_parent_devices_menu').on('click', '.dropdown-item', function(event) {
        event.preventDefault();
        var clicked_id = $(this).data('data-possible_parent_device_id');
        $('#inkberry_setup_user_parent_display_id_display_button').html(clicked_id);
       
      });
    
    
}