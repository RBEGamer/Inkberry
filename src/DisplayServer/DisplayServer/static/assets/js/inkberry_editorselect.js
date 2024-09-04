function load_available_devices(){
    $('#inkberry_open_editor_button_group').empty();

    $.getJSON("/api/list_devices", function( data ) {
      $.each( data['devices'], function( key, val ) {
            var item = $('<a>', {
            class: 'btn btn-primary',
            text: val['name'],
            style: 'margin: 10px;display: block;width: 100%;text-align: center;height: auto;'
            
        }).data("data-device_id", val['id']);
        $('#inkberry_open_editor_button_group').append(item);
      });

      $('#inkberry_open_editor_button_group').on('click', '.dropdown-item', function(event) {
        event.preventDefault();
        var clicked_id = $(this).data('data-device_id');
       
         window.location.origin + "/static/editor.html/?did=" + clicked_id;
        
      });
    });
    }



function inkberry_init(){
    
   
    load_available_devices();
    
   

    // REGISTER OPEN PREVIEW POPUP BUITTONS EVENT
    $('#inkberry_open_editor_button_group').on('click', 'button', function(event) {
        var popup_type = this.textContent.toLowerCase();
        open_render_preview_popup(popup_type);
    });
    
   
    
    
    
    
    
}