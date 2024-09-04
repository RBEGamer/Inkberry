function open_device_in_editor(event) {
    
    event.preventDefault();
    const clicked_id = $(this).data('data-device_id');  
    console.log(clicked_id);
  
    window.open(window.location.origin + "/static/editor.html?did=" + clicked_id);
}


function load_available_devices(){
    $.getJSON("/api/list_devices", function( data ) {
        $('#inkberry_open_editor_button_group').empty();
      $.each( data['devices'], function( key, val ) {
            var item = $('<a>', {
            class: 'btn btn-primary',
            text: val['name'],
            style: 'margin: 10px;display: block;width: 100%;text-align: center;height: auto;',
            id: 'inkberry_open_editor_button_' + val['id']
            
        }).data("data-device_id", val['id']).click(open_device_in_editor);
          
        $('#inkberry_open_editor_button_group').append(item);
      });
    });
}



function inkberry_init(){
    load_available_devices();
}