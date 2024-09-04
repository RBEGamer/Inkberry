function open_display_setup(){

    var did = getAllUrlParams().did;
    var hardware_type = getAllUrlParams().hardware_type;
    
    if(did != undefined && did && hardware_type != undefined && hardware_type){
        window.location.href = "/static/register.html?did=" + did + "&hardware_type=" + hardware_type;    
        return;
    }
    if(did != undefined && did){
        window.location.href = "/static/manualregister.html?did=" + did;      
    }else{
        window.location.href = "/static/manualregister.html";  
    }
}

function open_editor_redirect(){  
        var did = getAllUrlParams().did;
        if(did){
            window.location.href = "/static/editor.html?did=" + did;
        }else{
            window.location.href = "/static/editorselect.html";     
        }  
}


function inkberry_init(){
    $("#open_editor_redirect").click( open_editor_redirect);
    $("#open_setup_redirect").click( open_display_setup);   
}