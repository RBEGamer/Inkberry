var did = null;


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


function inkberry_init(){
    
    did = getAllUrlParams().did;
    if(!did){
        alert("DEVICE ID (QUERY PARAMETER did) NOT SPECIFIED");
        window.location.href = "/";
    }
    
    $("#inkberry_enable_button").click(enable_screen);
    $("#inkberry_disable_button").click(disable_screen);
    
}