
$.ajax({
    url: 'http://127.0.0.1:8000/medications',
    dataType: 'json',
    type: 'get', // This is the default though, you don't actually need to always mention it
    success: function(data) {
    	var json = $.parseJSON(data);
        console.log(json.html);
    },
    failure: function(data) {
    	var json = $.parseJSON(data);
        console.log(json.error);
    }

}); 