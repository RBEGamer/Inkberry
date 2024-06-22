var current_svg_content = "";
var current_loaded_device_id = "";
var current_svg_clickable_areas = [];

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
    const dw = $("#inkberry_device_editor_canvas_container").width();
    const dh = $("#inkberry_device_editor_canvas_container").height();

    // FETCH SVG
    const url = '/api/render/' + _id + "?as_png=0&target_width="+ dw +"&ts=" + String(Date.now());


    const svgString = loadSVGSync(url);

    if(!svgString){
        alert("cant get Device Document from " + url);
        window.location.reload();
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
    //debugger;
}


function editor_refresh_rendering(_id){
     $("#inkberry_device_renderered_image").attr("src","/api/render/" + _id + "?as_png=1&ts=" +String(Date.now()));
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

    $.getJSON("/api/update_parameter/" + d.currentTarget.dataset['device_id'] + "/" + d.currentTarget.dataset['parameter'] + "/" + d.currentTarget.value, function( data ) {
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
        const $input = $('<input/>').attr({ type: 'text', name: key, value: val , 'data-device_id': _id, 'data-parameter': _parameter_id});
        $input.change(on_parameter_changed);

        const $col2 = $('<td></td>').append($input);
        $row.append($col1, $col2);

        $('#inkberry_parameter_table_row_block').append($row);
                //.data("data-device_id", val['id']);
      });

        /*
      $('#inkberry_available_devices_dropdown_menu').on('click', '.dropdown-item', function(event) {
        event.preventDefault();
        var clicked_id = $(this).data('data-device_id');
        current_loaded_device_id = clicked_id;
        load_editor_for_device(current_loaded_device_id);
      });
      */

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
        load_editor_for_device(current_loaded_device_id);
      });
    });
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
}



function getAllUrlParams(url) {
  // get query string from url (optional) or window
  var queryString = url ? url.split('?')[1] : window.location.search.slice(1);
  // we'll store the parameters here
  var obj = {};
  // if query string exists
  if (queryString) {
    // stuff after # is not part of query string, so get rid of it
    queryString = queryString.split('#')[0];
    // split our query string into its component parts
    var arr = queryString.split('&');
    for (var i = 0; i < arr.length; i++) {
      // separate the keys and the values
      var a = arr[i].split('=');
      // set parameter name and value (use 'true' if empty)
      var paramName = a[0];
      var paramValue = typeof (a[1]) === 'undefined' ? true : a[1];
      // (optional) keep case consistent
      paramName = paramName.toLowerCase();
      if (typeof paramValue === 'string') paramValue = paramValue.toLowerCase();
      // if the paramName ends with square brackets, e.g. colors[] or colors[2]
      if (paramName.match(/\[(\d+)?\]$/)) {
        // create key if it doesn't exist
        var key = paramName.replace(/\[(\d+)?\]/, '');
        if (!obj[key]) obj[key] = [];
        // if it's an indexed array e.g. colors[2]
        if (paramName.match(/\[\d+\]$/)) {
          // get the index value and add the entry at the appropriate position
          var index = /\[(\d+)\]/.exec(paramName)[1];
          obj[key][index] = paramValue;
        } else {
          // otherwise add the value to the end of the array
          obj[key].push(paramValue);
        }
      } else {
        // we're dealing with a string
        if (!obj[paramName]) {
          // if it doesn't exist, create property
          obj[paramName] = paramValue;
        } else if (obj[paramName] && typeof obj[paramName] === 'string'){
          // if property does exist and it's a string, convert it to an array
          obj[paramName] = [obj[paramName]];
          obj[paramName].push(paramValue);
        } else {
          // otherwise add the property
          obj[paramName].push(paramValue);
        }
      }
    }
  }
  return obj;
}