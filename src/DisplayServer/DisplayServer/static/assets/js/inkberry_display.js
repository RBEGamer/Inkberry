var current_svg_content = "";
var current_loaded_device_id = "";
var current_svg_clickable_areas = [];

function generate_image_link(_did, _type){
 return window.location.origin + "/api/render/" + current_loaded_device_id + "?type=" + _type;  
}

function open_render_preview_popup(_type = "html"){
    console.log("open_render_preview_popup " + _type);
    window.open(generate_image_link(current_loaded_device_id, _type), '_blank');
}

function editor_refresh_rendering(_id){
     $("#inkberry_device_renderered_image").attr("src","/api/render/" + _id + "?type=png&ts=" +String(Date.now()));
}


function load_editor_for_device(_id){
    console.log('load_editor_for_device: ' + _id, null); // Beispielaktion

    editor_refresh_rendering(_id);
    
    $('#inkberry_calepd_link_text_output').val(generate_image_link(_id, 'calepd').replace("https:", "http:"));
    
    $('#inkberry_inkberry_link_text_output').val(generate_image_link(_id, 'inkfw').replace("https:", "http:"));

}



function copy_calepd_link(_elem_id){
    var link_content = $('#' + _elem_id).val();
        copyTextToClipboard(link_content);
}

function inkberry_init(){
    
   

    
    var did = getAllUrlParams().did;
    if(did){
        current_loaded_device_id = did;
        load_editor_for_device(current_loaded_device_id);
    }else{
        alert("DID not specified - please open this page using the EDITOR page.");
        return window.location.origin + "/static/index.html";
        
    }
    
    
    // REGISTER OPEN PREVIEW POPUP BUITTONS EVENT
    $('#inkberry_open_preview_button_group').on('click', 'button', function(event) {
        var popup_type = this.textContent.toLowerCase();
        open_render_preview_popup(popup_type);
    });
    
   
    
    $('#inkberry_manage_inkberry_btn').on('click', 'button', function(event) {
      generate_manage_link();
    });
    
    
    
    
    
}