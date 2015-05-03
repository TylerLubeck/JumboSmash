define("smashers", ["sweetalert"], function(swal) {
    // /api/v1/smashers
    var Smasher = TastypieModel.extend({
        decisionUrl: '/api/v1/decision/',
        url: function() {
            return "/api/v1/smashers/" + this.id + "/"
        },
        initialize: function() {

        },
        like: function() {
            this._decide(true);
        },
        dislike: function(){ 
            this._decide(false);
        },
        _decide: function(decision) {
            var that = this;
            $.ajax({
                type: 'POST',
                url: this.decisionUrl, 
                data: JSON.stringify({
                    user_id: this.id,
                    like: decision
                }), 
                contentType: 'application/json'
            }).success(function(response) {
                // that.swingCard.throwOut(0, -100);
                that.swingCard.destroy();
                that.trigger("destroy", that);

                if (response.match === true) {
                    swal({
                       title: "You and " + that.get("name") + " matched!",   
                        text: "We sent them an email for you ;)",   
                        type: "success" ,
                        timer: 2300 
                    })
                }
            }).
            error(function() {
                swal({   
                    title: "Error!",   
                    text: "Something went wrong! Beat it.",   
                    type: "error"
                });
            }).
            always(function() {})
        }
    })

    var Smashers = TastypieCollection.extend({
        model: Smasher,
        url: '/api/v1/smashers',
        getNextSwipeSet: function() {
            var that = this
            this.fetch({
                remove: false
            }).success(function() {
                console.log(that)
            }).error(function() {
                // console.log(arguments);
            }).always(function(){ 
                // console.log(arguments)
            });
        }
    });


    return {
        getSmashers: function(args, opts) {
            return new Smashers(args, opts);
        },
        getSmasher: function(args, opts) {
            return new Smasher(args, opts);
        },
        getMatches: function(callback) {
            $.getJSON("/api/v1/matches").success(function(response) {
                callback(new Smashers(response, {parse: true}));
            })
        }
    }

});