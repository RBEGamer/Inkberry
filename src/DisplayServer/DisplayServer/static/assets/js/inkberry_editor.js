var current_svg_content = "";
var current_loaded_device_id = "";
var current_svg_clickable_areas = [];

function generate_manage_link(){
    return window.location.origin + "/static/reactivate.html" + current_loaded_device_id + "?did=" + _type;
}

function generate_display_link(){
    window.open(window.location.origin + "/static/display.html" + current_loaded_device_id + "?did=" + current_loaded_device_id, '_blank');
}

function generate_image_link(_did, _type){
 return window.location.origin + "/api/render/" + current_loaded_device_id + "?type=" + _type;  
}




function resize_canvas(_width = null, _height = null){
    if(!_width){
     _width = $("#inkberry_device_editor_canvas_container").width();
    }

    if(!_height){
        _height = $("#inkberry_device_editor_canvas_container").height();
    }

    //SET DIV SIZE
    $("#inkberry_device_editor_canvas_container").width(_width);
    $("#inkberry_device_editor_canvas_container").height(_height);
    // SET CANVAS SIZE
    var canvas = document.getElementById('inkberry_device_editor_canvas');
    canvas.width = _width;
    canvas.height = _height;

}

function handle_canvas_click(event) {
    var x = event.offsetX;
    var y = event.offsetY;
    var clickedObject = get_svg_clicked_object(x, y);
    if (!clickedObject) {
        return;
    }

    console.log('canvas_clicked_object: ' + clickedObject);

    // FETCH PARAMETER INTO PARAMS TABLE
   load_parameters(current_loaded_device_id, clickedObject);
}

function get_svg_clicked_object(x, y) {

    for (var i = 0; i < current_svg_clickable_areas.length; i++) {
        var obj = current_svg_clickable_areas[i];

        if (x >= obj.x && x <= obj.x + obj.width && y >= obj.y && y <= obj.y + obj.height) {
            if(obj.id){
                return obj.id;
            }
        }
    }
    return null;
}

function loadSVGSync(url) {
    try {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", url, false); // false für synchrone Anfrage
    xhr.send(null);

    if (xhr.status === 200) {
        return xhr.responseText;
    } else {
        throw new Error('Network response was not ok ' + xhr.statusText);
    }
    } catch (error) {
    console.error('Fetch operation failed: ', error);
    return "";
}
}

function calculateArea(obj) {
    switch (obj.tag) {
        case 'svg':
        case 'rect':
        case 'image':
        case 'use':
            return obj.width * obj.height;
        case 'circle':
            return Math.PI * Math.pow(obj.r, 2);
        case 'ellipse':
            return Math.PI * obj.rx * obj.ry;
        default:
            return 0;
    }
}

// Funktion zum Extrahieren der SVG-Objekte mit relevanten Attributen
function extractSVGObjects(_xml_doc) {
    // Selektiere alle relevanten SVG-Elemente
    const elements = _xml_doc.querySelectorAll('svg');

    const objects = [];

    // Iteriere über die Elemente und extrahiere die Attribute
    elements.forEach(function(element) {
        const obj = { tag: element.tagName };
        if (element.hasAttribute('x')) obj.x = parseFloat(element.getAttribute('x'));
        if (element.hasAttribute('y')) obj.y = parseFloat(element.getAttribute('y'));
        if (element.hasAttribute('width')) obj.width = parseFloat(element.getAttribute('width'));
        if (element.hasAttribute('height')) obj.height = parseFloat(element.getAttribute('height'));
        if (element.hasAttribute('id')) obj.id = element.getAttribute('id');


        obj.area = calculateArea(obj);
        if(obj.id){
            objects.push(obj);
        }
    });
    // Sortiere die Objekte nach Fläche
    objects.sort((a, b) => b.area - a.area);
    return objects;
}


function load_svg_to_canvas(_id, callback) {

    // GET CANVAS SIZE
    const dw = Math.floor($("#inkberry_device_editor_canvas_container").width() * 0.8);
    const dh = Math.floor($("#inkberry_device_editor_canvas_container").height());

    // FETCH SVG
    const url = '/api/render/' + _id + "?type=svg&target_width="+ dw +"&ts=" + String(Date.now());


    const svgString = loadSVGSync(url);

    if(!svgString){
        alert("cant get Device Document from " + url);
        window.location.assign("/");
        //window.location.reload();
        return;
    }
    const parser = new DOMParser();
    const xmlDoc = parser.parseFromString(svgString, "image/svg+xml");

    // SET NEW CANVAS HEIGHT
    const svgElement = xmlDoc.getElementsByTagName("svg")[0];
    // Extract the width, height, and viewBox attributes and resize the canvas
    const width = svgElement.getAttribute("width");
    const height = svgElement.getAttribute("height");
    const viewBox = svgElement.getAttribute("viewBox");
    resize_canvas(width, height);

    //SETUP CANVAS
    var canvas = document.getElementById('inkberry_device_editor_canvas');
    var ctx = canvas.getContext('2d');
    //REGISTER ONCLICK EVENT SO THE USER CAN SELECT OBJECTS
    canvas.addEventListener('click', handle_canvas_click);

    //RENDER SVG AS IMAGE ON CANVAS
    var img = new Image();
    img.onload = function() {
        ctx.drawImage(img, 0, 0);
        if(callback){
            callback();
        }
    };
    img.src = url;

    const objs = extractSVGObjects(xmlDoc);
    if(objs){
        current_svg_clickable_areas = objs;
    }
}


function editor_refresh_rendering(_id){
     resize_canvas(document.getElementById("inkberry_device_editor_canvas_container").clientWidth, document.getElementById("inkberry_device_editor_canvas_container").clientHeight);
     load_svg_to_canvas(_id);
}


function load_editor_for_device(_id){
    console.log('load_editor_for_device: ' + _id, null); // Beispielaktion

    editor_refresh_rendering(_id);
  
  
    //LOAD PARAMETER TABLE
    $.getJSON("/api/information/" + _id, function( data ) {
        if(!data['error']){
            console.log(data);
            //LOAD INFO TABLE
            $('#inkberry_device_information_type').html(data['hardware']);
            $('#inkberry_device_information_name').html(data['name']);

            // LOAD PARAMETER
            $('#inkberry_parameter_table_row_block').empty();
        }
    });
}

function on_parameter_changed(d){
    console.log(d);

    $.getJSON("/api/update_parameter/" + d.currentTarget.dataset['device_id'] + "/" + d.currentTarget.dataset['tile_id'] + "/"+  d.currentTarget.dataset['parameter'] +"/" + d.currentTarget.value + "/" + d.currentTarget.dataset['is_system_parameter'], function( data ) {
        editor_refresh_rendering(current_loaded_device_id);
    });
}

function load_parameters(_id, _parameter_id){
    $('#inkberry_parameter_table_row_block').empty();
    $('#inkberry_user_selected_parameter_id_text').html(_parameter_id);
    
    $.getJSON("/api/get_parameter_list/" + _id + "/" + _parameter_id, function( data ) {

      if(!data['parameters']){return;}

      $.each( data['parameters'], function( key, val ) {
        const $row = $('<tr></tr>');
        const $col1 = $('<td></td>').text(key);
        const $input = $('<input/>').attr({ type: 'text', name: key, value: val , 'data-device_id': _id, 'data-tile_id': _parameter_id, 'data-parameter': key, 'data-is_system_parameter': '0'});
        $input.change(on_parameter_changed);

        const $col2 = $('<td></td>').append($input);
        $row.append($col1, $col2);

        $('#inkberry_parameter_table_row_block').append($row);
      });

      $('#inkberry_parameter_table_row_block').append($('<tr>TILE</tr>').append($('<td>TILE</td>'), $('<td>SETTINGS</td>')));

      $.each( data['system_parameters'], function( key, val ) {
        const $row = $('<tr></tr>');
        const $col1 = $('<td></td>').text(key);
        const $input = $('<input/>').attr({ type: 'text', name: key, value: val , 'data-device_id': _id, 'data-tile_id': _parameter_id, 'data-parameter': key, 'data-is_system_parameter': '1'});
        $input.change(on_parameter_changed);

        const $col2 = $('<td></td>').append($input);
        $row.append($col1, $col2);

        $('#inkberry_parameter_table_row_block').append($row);
      });
    });
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
        current_loaded_device_id = clicked_id;
        $('#inkberry_available_devices_dropdown_menu_button').html(clicked_id);
         load_editor_for_device(current_loaded_device_id);
        
      });
    });
    }




function copy_calepd_link(_elem_id){
    var link_content = $('#' + _elem_id).val();
        copyTextToClipboard(link_content);
}

function inkberry_init(){
    resize_canvas();
    $(window).on( "resize", function() {
        load_svg_to_canvas(current_loaded_device_id);
    });

    load_available_devices();
    
    var did = getAllUrlParams().did;
    if(did){
        current_loaded_device_id = did;
        load_editor_for_device(current_loaded_device_id);
    }
    

    
    $('#inkberry_manage_inkberry_btn').on('click', 'button', function(event) {
      generate_manage_link();
    });
    
    $('#inkberry_display_inkberry_btn').on('click', 'button', function(event) {
      generate_display_link();
    });
    
    
    
    
    
}