define("coreUI", ["smashers", "cardInterface", "upload", "animatedModal"], function(smashers, cardInterface, upload) {

    var $searchbar = $("#smash-autocomplete");
    var $matchButton = $(".js-show-matches");
    var $addPicture = $("#js-add-picture");
    var $searchBarTrigger = $(".js-show-searchbar");
    var $matchList = $("#match-list");
    var searchBarOpen = false;

    return function() {
        $matchButton.click(function() {
            console.log("showing matches")
            smashers.getMatches(function(matches) {
                var cardList = cardInterface.getCardList({
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
        console.log($addPicture)
        $addPicture.animatedModal({
            modalTarget: "addPictureModal"
        })
    }
})