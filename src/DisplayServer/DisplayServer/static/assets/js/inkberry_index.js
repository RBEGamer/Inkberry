
function open_editor_redirect(){
    $.getJSON("/api/list_devices", function( data ) {
        const devices = data['devices'];
        
        if(!devices){
            window.location.href = "/editor.html";
        }
        const item = devices[Math.floor(Math.random()*devices.length)];
        
        window.location.href = "/static/editor.html?did=" + item['id'];
        //['id']
    });
}


function inkberry_init(){
    $("#open_editor_redirect").click( open_editor_redirect);
    
}