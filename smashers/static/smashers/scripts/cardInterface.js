define("cardInterface", ["smashers"], function(smashers) {


    var stack_config = {

        throwOutConfidence: function (offset, element) {
            return Math.min((Math.abs(offset) + 150) / element.offsetWidth, 1);
        },
        throwOutDistance: function() {
            return 1250
        },
        time: 1000
    };


    var CardItemView = Backbone.View.extend({
        template: _.template($("#single-card").html()),
        className: "smash-card",
        tagName: 'li',
        initialize: function() {
            var that = this;
            this.listenTo(this.model, {
                remove: function() {
                    var that = this;
                    this.$el.fadeOut("fast", function(){
                        that.remove();
                    })
                },
                "change:headshot": function(model, collection, opts) {
                },
                "pass": function(){ 
                    this.$el.slideUp("fast", function(){
                        that.model.passed = true;
                        that.model.trigger("destroy", that.model);
                    });
                }
            })
        },
        render: function() {
            this.$el.html(this.template(this.model.toJSON()))
            this.drawExistingFeedback();
            return this;
        },
        drawExistingFeedback: function() {
            var that = this;
            if (this.model.get("status") === 1) {
                setTimeout(function() {
                    that.updateLikeIcon(1);
                    that.updateDislikeIcon(0);
                    that.updateMatchIcon(0);
                }, 400);
            }
            else if (this.model.get("status") === 2) {
                setTimeout(function() {
                    that.updateDislikeIcon(1);
                    that.updateLikeIcon(0);
                    that.updateMatchIcon(0);
                }, 400);
            }
            else if (this.model.get("status") === 3) {
                setTimeout(function() {
                    that.updateMatchIcon(1);
                    that.updateDislikeIcon(0);
                    that.updateLikeIcon(0);
                }, 400);
            }
            else {
                this._updateFeedBackIcon(0);
            }
        },
        resetFeedbackIcons: function() {
            this.drawExistingFeedback();
        },
        _updateFeedBackIcon: function(opacity, icon) {
            var selector = ".feedback-icon";
            if (icon) {
                selector = ".icon-" + icon
            }
            this.$(selector).css("opacity", opacity);
        },
        updateDislikeIcon: function(opacity) {
            this._updateFeedBackIcon(opacity, "dislike")
            return this;
        },
        updateLikeIcon: function(opacity) {
            this._updateFeedBackIcon(opacity, "like")
            return this;
        },
        updateMatchIcon: function(opacity) {
            this._updateFeedBackIcon(opacity, "match")
            return this;  
        }
    });

    var CardCollectionView = Backbone.View.extend({
        el: "#card-interface",
        initialize: function(opts) {
            var that = this;
            this.stack = gajus.Swing.Stack(stack_config);
            _.extend(this, {draggable: true}, opts);

            if(this.collection.length > 0) {
                this.$(".placeholder").hide();
            }

            this.collection.each(function(smasher) {
                that.addCard(smasher);
            })

            this.listenTo(this.collection, {
                add: function(model, collection, opts) {
                    this.$(".placeholder").hide();
                    this.$(".loader").hide();
                    this.addCard(model);
                },
                remove: function() {
                    this.activeCard = this.collection.last();
                    // If there is nothing left in the collection....
                    if (!this.activeCard) {
                        this.collection.getNextSwipeSet(function() {
                            that.$(".loader").hide();
                        });
                        this.$(".loader").show();
                        this.$(".placeholder").show();
                    }
                }
            })

            _.bindAll(this, "addCard");

            this.bindStackListeners();
        },
        bindStackListeners: function() {
            var that = this;
            this.stack.on("throwout", function(e) {
                var id =  $(e.target).attr("model-id");
                var model = that.collection._byId[id];
                setTimeout(function() {
                    if (model) {
                        (e.throwDirection === gajus.Swing.Card.DIRECTION_LEFT ? model.dislike() : model.like());
                    }
                }, 300)    
            })
        },
        addCard: function(card) {
            var c = new CardItemView({model: card});
            this.$(".cards").append(c.render().el);
            c.$el.attr("model-id", card.cid);
            this.activeCard = card;
            if (this.draggable === true) {
                var swingCard = this.stack.createCard(c.el);
                swingCard.throwIn(-100, -100)

                swingCard.on("dragstart", function() {
                    c.$el.addClass("dragging")
                })
                swingCard.on("dragend", function() {
                    c.$el.removeClass("dragging")
                })

                swingCard.on("dragmove", function(e) {
                    if (e.throwDirection == gajus.Swing.Card.DIRECTION_LEFT) {
                        c.updateLikeIcon(0);
                        c.updateDislikeIcon(e.throwOutConfidence);
                    }
                    else {
                        c.updateLikeIcon(e.throwOutConfidence);
                        c.updateDislikeIcon(0);
                    }
                });
                swingCard.on("throwinend", function() {
                    c.resetFeedbackIcons();
                })
                card.swingCard = swingCard;
            }
        },
        events: {
            "click #like": function() {
                if (this.activeCard)
                    this.activeCard.swingCard.throwOut(20, 111)
            },
            "click #dislike": function() {
                if (this.activeCard)
                    this.activeCard.swingCard.throwOut(-20, 111)
            },
            "click .js-pass": function() {
                var activeCard = this.activeCard;
                if (activeCard) {
                    activeCard.trigger("pass");
                }
            }
        }

    });

    var activeSmashers = smashers.getSmashers();
    var activeSetView = new CardCollectionView({collection: activeSmashers});
    if (!window.user.error)
        activeSmashers.getNextSwipeSet();

    return {
        activeSet: function() {
            return activeSmashers;
        },
        getCardList: function(args, opts) {
            return new CardCollectionView(args, opts);
        }
    }
})