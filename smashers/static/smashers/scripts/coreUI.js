define("coreUI", [], function() {

    var $searchbar = $("#smash-autocomplete");
    var $matchButton = $(".js-show-matches");
    var $searchBarTrigger = $(".js-show-searchbar");
    var searchBarOpen = false;

    return function() {
        $matchButton.click(function() {
            console.log("showing matches")
        });
        $searchBarTrigger.click(function() { 
            if (searchBarOpen === false) {
                $searchbar.animate({
                    width: 300
                }, 200);
                $matchButton.fadeOut("fast");
                $searchBarTrigger.removeClass("icon-search3").addClass("active-searchbar icon-cross");
                searchBarOpen = true;
            }
            else {
                $searchbar.animate({
                    width: 0
                }, 200);
                $matchButton.fadeIn("fast");
                $searchBarTrigger.removeClass("active-searchbar icon-cross").addClass("icon-search3");
                searchBarOpen = false;
            }
        })

    }
})