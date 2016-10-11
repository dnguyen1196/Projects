
// Toggle movie query search
$("#menu-toggle").click(function(e) {
    e.preventDefault();
    $("#wrapper").toggleClass("toggled");
});

// MovieInfo model
var MovieInfo =  Backbone.Model.extend({
    default:{
        Title:'',
        Year: 0,
        Plot: '',
        Poster: ''
    },
});

var MoviePanel = Backbone.View.extend({
    el: '#movie_list',
    initialize: function(){
        this.render(this);
    },
    render: function(view){
        $.get("/static/movie_panel_template.html", function(data){
            var movie_panel = _.template(data);
            view.$el.append(movie_panel(view.model.toJSON()));
        });
    }
});

// Create a function that receives the user input choice 
// and create a binary string of 18 characters that represent 
// the user selection
function get_user_category_choice() {
    var query = ""
    $(".checkbox").each(function() {
        if ($(this).find("input").is(':checked')) {
            query += "1";
        } else {
            query += "0";
        }
    });
    return query;
}

// GET COOKIE 
// The few functions below interact with django security
// measures using CSRF
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


// Send the search query to the server (AJAX) and awaits
$("#movie_search_request").click(function(){
    $("#movie_list").empty();

    var query = get_user_category_choice();
    var url = "http://localhost:8080/search";
    var data = {
        "category": query 
    };

    $.ajax({
        "type": "POST",
        "dataType": "text",
        "url": url,
        "data": data,
        "beforeSend": function(xhr, settings) {
            $.ajaxSettings.beforeSend(xhr, settings);
        },
        "success": function(result) {
            handle_movie_return_data(result);
        },
        "error": function(error) {
            console.log(error.responseText);
        }
    });

});

function handle_movie_return_data(result) {
    if (result == "ERROR WITH POST DATA") {
        console.log("SOMETHING IS WRONG!!!");
        return 0;
    }
    movie_list = JSON.parse(result);
    for (var i = 0; i < movie_list.length; i++) {
        var film = movie_list[i]["fields"];
        get_movie_info_OMDB(film);
    }
}

// Perform ajax request to OMDB to find movie information
function get_movie_info_OMDB(film) {
    var url = "http://www.omdbapi.com/?t=" + film["name"];
    $.ajax({
        "type": "GET",
        "dataType": "JSON",
        "url": url,
        "success": function(result) {
            display_movie_info(result);
        },
        "error": function(error) {
            console.log(error.responseText);
        }
    });
}

// Display movie info on the screen
// Testing mode - simple list
function display_movie_info(film) {
    if (film["Title"] == undefined || film["Year"] == undefined || film["Plot"] == undefined) {
        return;
    }
    var MovieInst = new MovieInfo({Title: film["Title"], Year: film["Year"], Plot: film["Plot"], Poster: film["Poster"]});
    var MovieWindow =  new MoviePanel({model: MovieInst});
}