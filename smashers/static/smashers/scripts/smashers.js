define("smashers", ["sweetalert"], function(swal) {
    // /api/v1/smashers

    var activeUser;

    function getMessageGenerator() {
        var count = 0;
        var messages = [
            "We sent <%= name %> an email for you ;)",
            "Nice! Maybe you and <%= name %> will get married?",
            "Senior week is only so long. Carpe diem!",
            "I bet <%= name %> is as excited as you are.",
            "Somebody get me a towel.",
            "I'll be in my bunk.",
            "Think how far you've come since freshman year. Show <%= name %> your skillz!"
        ]

        return function(name) {
            count %= messages.length;
            return _.template(messages[count++])({name: name});
        }
    }

    var messageGenerator = getMessageGenerator();

    var Smasher = TastypieModel.extend({
        decisionUrl: '/api/v1/decision/',
        url: function() {
            return "/api/v1/smashers/" + this.id + "/"
        },
        defaults: {
            headshot: "static/smashers/avatar.png",
            has_headshot: false,
            num_matches: 0
        },
        parse: function(response) {
            if (response.major){
                response.major = response.major.split("(")[0]
            }
            if (!response.headshot) {
                return _.omit(response, "headshot");
            }
            return response;
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

                var firstname = that.get("name").split(" ")[0]

                if (response.match === true) {
                    swal({
                       title: "Matched!",   
                        text: messageGenerator(firstname),
                        type: "success" ,
                        timer: 2300 
                    });
                    // Sorry :(
                    var matches = parseInt($("#num-matches").text());
                    $("#num-matches").text(++matches)

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
        getNextSwipeSet: function(callback) {
            var that = this
            this.fetch({
                remove: false
            }).success(function(response) {
                if (callback) {
                    callback(that);
                }
            }).error(function() {
                console.log(arguments);
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
                (callback || $.noop)(new Smashers(response, {parse: true}));
            })
        },
        // Expects a plain object, returns smasher
        setActiveUser: function(user) {
            return activeUser = new Smasher(user, {parse: true});
        },
        // returns smasher model
        getActiveUser: function() {
            return activeUser;
        }
    }

});