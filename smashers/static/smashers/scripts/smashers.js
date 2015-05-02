define("smashers", ["sweetalert"], function(swal) {
    // /api/v1/smashers
    var Smasher = TastypieModel.extend({
        url: '/api/v1/decision/',
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
                url: this.url, 
                data: JSON.stringify({
                    user_id: this.id,
                    like: decision
                }), 
                contentType: 'application/json'
            }).success(function() {
                // that.swingCard.throwOut(0, -100);
                that.swingCard.destroy();
                that.trigger("destroy", that);
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
    }

});