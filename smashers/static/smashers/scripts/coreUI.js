define("coreUI", ["smashers", "cardInterface", "upload", "sweetalert", "animatedModal"], function(smashers, cardInterface, upload, swal) {

    var $searchbar = $("#smash-autocomplete");
    var $matchButton = $(".js-show-matches");
    var $addPicture = $("#js-add-picture");
    var $showProfile = $(".js-show-profile")
    var $searchBarTrigger = $(".js-show-searchbar");
    var $matchList = $("#match-list");
    var $logoutButton = $("#logout");
    var $uploadButton = $("#upload")
    var fileSelect = document.getElementById('file-select');
    var searchBarOpen = false;
    var cardList = null;

    return function() {

        $uploadButton.click(function(){
            var $this = $(this);
            $this.text("Uploading...")
            var files = fileSelect.files;
            console.log(files)
            var formData = new FormData();
            var file = files[0];
            if (!file) {
                return;
            }
            // Check the file type.
            if (!file.type.match('image.*')) {
                return
            }

            formData.append('headshot', file);
            var xhr = new XMLHttpRequest();
            xhr.open("PUT", "/api/v1/user/1514/", true)
            xhr.onload = function () {
                if (xhr.status === 200) {
                    // File(s) uploaded.
                    var response = JSON.parse(xhr.responseText);
                    swal({
                        type: 'success',
                        title: 'Picture uploaded!',
                        text: 'Nice work. Get ready for the matches to pour in.',
                        timer: 4000
                    })
                    $this.html('Upload');

                } 
                else {
                    alert('An error occurred!');
                }
            };
            xhr.send(formData);
            // Add the file to the request.
            // $.ajax({
            //     url: "/api/v1/user/1/",
            //     type: "PUT",
            //     data: FormData
            // }).success(function(response) {
            //     console.log(response)
            // })

        })

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