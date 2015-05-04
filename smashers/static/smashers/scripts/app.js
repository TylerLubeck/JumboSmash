require.config({
    paths: {
        "jquery"        : "bower_components/jquery/dist/jquery.min",
        "underscore"    : "bower_components/underscore/underscore-min",
        "backbone"      : "bower_components/backbone/backbone",
        "animatedModal" : "animatedModal/animatedModal.min",
        "sweetalert"    : "bower_components/sweetalert/lib/sweet-alert.min"
    }
});

define("app", ["jquery", "underscore", "backbone"], function($, _, Backbone) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function csrfSafeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        }
    });

    window.TastypieModel = Backbone.Model.extend({
        base_url: function() {
          var temp_url = Backbone.Model.prototype.url.call(this);
          return (temp_url.charAt(temp_url.length - 1) == '/' ? temp_url : temp_url+'/');
        },

        url: function() {
          return this.base_url();
        }
    });

    window.TastypieCollection = Backbone.Collection.extend({
        parse: function(response) {
            this.recent_meta = response.meta || {};
            return response.objects || response;
        }
    });

    var login = require(["login"]);
    require(["smashers"], function(smashers) {
       if (!_.isUndefined(window.user) && !window.user.error) {
            smashers.setActiveUser(window.user);
       }
    });
    var cards = require(["cardInterface"]);
    require(["search"], function(search) {
        search(window.people)
    });
    require(["coreUI"], function(ui) { 
        ui.init(); 
        if (window.user && !window.user.error) {
            ui.setNumMatches(window.user.num_matches);
        }
    })

})
