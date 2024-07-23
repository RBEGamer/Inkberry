var did = null;

function set_delete(){
    $.getJSON("/api/set_delete_display/" + did, function( data ) {

    });
}

function enable_screen(){
    set_activation_state(did, "1");
}

function disable_screen(){
    set_activation_state(did, "0");
}

function set_activation_state(deivce_id, new_state){
    $.getJSON("/api/set_display_state/" + deivce_id + "/" + new_state, function( data ) {
        
        if(new_state){
            window.location.href = "/static/editor.html"; 
        }else{
             window.location.href = "/static/index.html";
        }
           
    });
}


function inkberry_init(){
    
    did = getAllUrlParams().did;
    if(!did){
        alert("DEVICE ID (QUERY PARAMETER did) NOT SPECIFIED");
        window.location.href = "/";
    }
    
    $("#inkberry_enable_button").click(enable_screen);
    $("#inkberry_disable_button").click(disable_screen);
     $("#inkberry_delete_button").click(set_delete);
    
}