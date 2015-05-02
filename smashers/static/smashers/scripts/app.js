require.config({
    paths: {
        "jquery"    : "bower_components/jquery/dist/jquery.min",
        "underscore": "bower_components/underscore/underscore-min",
        "backbone"  : "bower_components/backbone/backbone",
        "sweetalert": "bower_components/sweetalert/lib/sweet-alert.min"
    }
});

define("app", ["jquery", "underscore", "backbone"], function($, _, Backbone) {

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
    var activeUser;
    require(["smashers"], function(smashers) {
        activeUser = smashers.getSmasher();
        console.log(activeUser);
    });
    var cards = require(["cardInterface"]);

})