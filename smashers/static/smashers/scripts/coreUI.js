define("coreUI", ["smashers", "cardInterface", "sweetalert", "animatedModal"], function(smashers, cardInterface, swal) {

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

    var UserProfileView = Backbone.View.extend({
        template: _.template($("#user-profile").html()),
        render: function() {
            this.$el.html(this.template(this.model.toJSON()))
            return this;
        },
        events: {
            "change #file-select": function(e) {
                var that = this;
                var reader = new FileReader();
                this.$(".js-upload").text("Click to finalize your picture!").show().removeClass("animated bounce").addClass("animated bounce")
                reader.onload = function(){
                  var output = document.getElementById('output');
                  output.src = reader.result;
                };
                reader.readAsDataURL(e.target.files[0]);
            },
            "click .js-upload": function(e) {
                var $this = $(e.currentTarget);
                var files = document.getElementById("file-select").files;
                var file = files[0];
                var that = this;
                if (!file) {
                    $this.show().text("Select a file first!")
                    return;
                }
                var formData = new FormData();
                $this.text("Uploading...")
                // Check the file type.
                if (!file.type.match('image.*')) {
                    return
                }

                formData.append('headshot', file);
                var xhr = new XMLHttpRequest();
                xhr.open("PUT", "/api/v1/user/" + smashers.getActiveUser().id + "/", true)
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                xhr.onload = function () {
                    if (xhr.status === 200) {
                        // File(s) uploaded.
                        var response = JSON.parse(xhr.responseText);
                        that.model.set("headshot", response.headshot);
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
            },
            "click .js-deactivate-account": function() {
                swal({
                   title: "Are you sure?",  
                   text: "You will not be able to recover it!",
                   type: "warning",
                   showCancelButton: true,
                   confirmButtonColor: "#DD6B55",
                   confirmButtonText: "Yes, delete it",
                   cancelButtonText: "No, cancel plz",
                   closeOnConfirm: false,
                   closeOnCancel: false 
               }, function(isConfirm){   
                    if (isConfirm) {     
                        $.ajax({
                            url:"/api/v1/user/" + smashers.getActiveUser().id + "/",
                            type: "DELETE"
                        }).success(function() {
                            swal("Deleted!", "Your account has been deleted.", "success");   
                        }).error(function(){
                            swal("Oh no!", "Something went wrong deleting your account :(", "error");   
                        })
                    } 
                    else {    
                        swal("Cancelled", "Your account is safe :)", "error");   
                    } 
                });
            },
            "click .js-logout": function() {
                $.get("/api/v1/user/logout/").success(function(response) {
                    swal({
                        type: "success",
                        title: "Successfully logged out.",
                        text: "Get out there and go smash!"
                    });
                    setTimeout(function() {
                        window.location.href = "/"
                    }, 1000)
                })
            }
        }
    })


    var $searchbar = $("#smash-autocomplete");
    var $matchButton = $("#show-matches");
    var $addPicture = $("#js-add-picture");
    var $showProfile = $(".js-show-profile")
    var $searchBarTrigger = $(".js-show-searchbar");
    var $matchList = $("#match-list");
    var $uploadButton = $("#upload");
    var searchBarOpen = false;
    var cardList = null;

    function init() {
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
        }).animatedModal({
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
        $searchBarTrigger.click(function() { 
            if (searchBarOpen === false) {
                $searchbar.add(".twitter-typeahead").fadeIn("fast");
                $searchBarTrigger.removeClass("icon-search3").addClass("active-searchbar icon-cross");
                searchBarOpen = true;
            }
            else {
                $searchbar.add(".twitter-typeahead").fadeOut("fast");
                $searchBarTrigger.removeClass("active-searchbar icon-cross").addClass("icon-search3");
                searchBarOpen = false;
            }
        });

        $addPicture.animatedModal({
            modalTarget: "updateProfileModal"
        });


        $showProfile.animatedModal({
            modalTarget: "updateProfileModal",
            beforeOpen: function() {
                var profileView = new UserProfileView({model: smashers.getActiveUser()}).render().delegateEvents();
                $("#updateProfileModal .modal-content").html(profileView.el);
            }
        })

    }


    return {
        init: init,
        setNumMatches: function(num_matches) {
            $("#num-matches").text(num_matches)
        }
    }
})