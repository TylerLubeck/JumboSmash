define("coreUI", ["smashers", "cardInterface", "upload", "sweetalert", "animatedModal"], function(smashers, cardInterface, upload, swal) {

    var $searchbar = $("#smash-autocomplete");
    var $matchButton = $(".js-show-matches");
    var $addPicture = $("#js-add-picture");
    var $showProfile = $(".js-show-profile")
    var $searchBarTrigger = $(".js-show-searchbar");
    var $matchList = $("#match-list");
    var $logoutButton = $("#logout");
    var searchBarOpen = false;
    var cardList = null;

    return function() {

        $logoutButton.click(function() {
            $.get("/api/v1/user/logout/").success(function(response) {
                swal({
                    type: "success",
                    title: "Successfully logged out.",
                    text: "Get out there and go smash!"
                });
                setTimeout(function() {
                    window.location.href = "/"
                }, 4000)
            })
        })

        $matchButton.click(function() {
            smashers.getMatches(function(matches) {
                if (cardList != null) {
                    cardList.stopListening();
                    cardList.$(".cards").empty()
                }

                cardList = cardInterface.getCardList({
                    collection: matches, 
                    el: "#match-list",
                    draggable: false
                }, {add: true});
            })
        });
        $searchBarTrigger.click(function() { 
            if (searchBarOpen === false) {
                $searchbar.animate({
                    width: 300
                }, 200);
                $searchBarTrigger.removeClass("icon-search3").addClass("active-searchbar icon-cross");
                searchBarOpen = true;
            }
            else {
                $searchbar.animate({
                    width: 0
                }, 200);
                $searchBarTrigger.removeClass("active-searchbar icon-cross").addClass("icon-search3");
                searchBarOpen = false;
            }
        });

        $("#show-matches").animatedModal({
            afterOpen: function() {
                $matchList.show().addClass("animated bounceInLeft")
                  
            },
            afterClose: function(){
                $matchList.hide().removeClass("animated bounceOutRight")
            },
            beforeClose: function() {
                $matchList.removeClass("bounceInLeft").addClass("animated bounceOutRight")
            }
        });

        $addPicture.animatedModal({
            modalTarget: "updateProfileModal"
        });

        $showProfile.animatedModal({
            modalTarget: "updateProfileModal"
        })
    }
})