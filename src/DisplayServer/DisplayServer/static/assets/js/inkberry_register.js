function inkberry_submit_registration_parent(){
    var did = getAllUrlParams().did;
    var hardware_type_str = $("#inkberry_hardware_type").val();
    var allocation = $("#inkberry_setup_user_input_allocation_parent").val();
    var parent_display_id = $("#inkberry_setup_user_parent_display_id_display_button").html();
    
    if(!allocation){
        alert("Please fill allocation field in");
        return;
    }
    
    if(!parent_display_id || parent_display_id.includes("_") || parent_display_id.includes(" ")){
        alert("Please select a valid parent");
        return;
    }
    
    
   
    $.getJSON("/api/register_parent/" + did + "/" + hardware_type_str + "/" + allocation + "/" + parent_display_id, function( data ) {
        if(data.error){
            alert("REGISTRATION FAILED - PLEASE TRY AGAIN");
            alert(data.error);
        }else{
            window.location.href = "/static/editor.html";  
        }
    });
}

function inkberry_submit_registration(){
    var did = getAllUrlParams().did;
    var hardware_type_str = $("#inkberry_hardware_type").val();
    var allocation = $("#inkberry_setup_user_input_allocation_new").val();
    var orientation = $("#inkberry_setup_user_orientation_display_button").html();
    
    if(!allocation){
        alert("Please fill allocation field in");
        return;
    }
    
    if(!orientation || orientation.includes("_") || orientation.includes(" ")){
        alert("Please select a valid orientation");
        return;
    }
    
   
    $.getJSON("/api/register_new/" + did + "/" + hardware_type_str + "/" + allocation + "/" + orientation, function( data ) {
        if(data.error){
            alert("REGISTRATION FAILED - PLEASE TRY AGAIN");
            alert(data.error);
        }else{
            window.location.href = "/static/editor.html";  
        }
    });
    
}
function inkberry_init(){
    
    var did = getAllUrlParams().did;
    if(!did){
        alert("DEVICE ID (QUERY PARAMETER did) NOT SPECIFIED. PLEASE USE THE QR CODE SHOWN ON THE DEVICE");
        window.location.href = "/";
        return;
    }
    
    var hardware_type = getAllUrlParams().hardware_type;
    if(!hardware_type){
        alert("HARDWARE TYPE (QUERY PARAMETER hardware_type) NOT SPECIFIED. PLEASE USE THE QR CODE SHOWN ON THE DEVICE");
        window.location.href = "/";
        return;
    }
    
    $("#inkberry_screen_id").val(did);
    
    $.getJSON("/api/get_hardware_type_name/" + hardware_type, function( data ) {
        if(data.error){
            alert("HARDWARE TYPE (QUERY PARAMETER hardware_type) IS INVALID. PLEASE MAKE SURE THAT THE RIGHT AND LATEST FIRMWARE IS USED");
            window.location.href = "/";
            return;
        }else{
            $("#inkberry_hardware_type").val(data.hardware_type_name);           
        }
    });
    
    $.getJSON("/api/list_possible_parent_devices/" + did + "/" + hardware_type, function( data ) {
      $.each( data['possible_parents'], function( key, val ) {
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
    
    
    
    
    $.getJSON("/api/list_display_orientations", function( data ) {
        $.each( data['orientations'], function( key, val ) {
                var item = $('<a>', {
                class: 'dropdown-item',
                text: val['name']
            }).data("data-orientation", val['value']);
            $('#inkberry_setup_user_orientation_display').append(item);
          });
    });
    
    
    $('#inkberry_setup_dropdown_possible_orientation_menu').on('click', '.dropdown-item', function(event) {
        event.preventDefault();
        var clicked_id = $(this).data('data-orientation');
        $('#inkberry_setup_user_orientation_display_button').html(clicked_id);
       
      });
}