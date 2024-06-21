function resize_canvas(width, height){
    var canvas = document.getElementById('canvas');
    var ctx = canvas.getContext('2d');
    ctx.width = width;
    ctx.height = height;
}

function load_svg_to_canvas(url, callback) {

    var canvas = document.getElementById('canvas');
    var ctx = canvas.getContext('2d');


    var img = new Image();
    img.onload = function() {
        ctx.drawImage(img, 0, 0);
        callback();
    };
    img.src = url;
    }


function editor_refresh_rendering(_id){
     $("#inkberry_device_renderered_image").attr("src","/api/render/" + _id + "as_png=1&ts=" +String(Date.now()));
     resize_canvas(document.getElementById("inkberry_device_renderered_image").clientWidth, document.getElementById("inkberry_device_renderered_image").clientHeight);
     load_svg_to_canvas('/api/render/' + _id,)
}
function load_editor_for_device(_id){
    console.log('load_editor_for_device: ' + _id); // Beispielaktion

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
            for (var entry in data['parameter']) {

            }
        }
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
        load_editor_for_device(clicked_id);
      });
    });
    }

function inkberry_init(){
    load_available_devices();

    var did = getAllUrlParams().did;
    if(did){
        load_editor_for_device(did);
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