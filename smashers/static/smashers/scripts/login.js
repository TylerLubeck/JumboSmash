define("login", ["sweetalert", "cardInterface", "smashers", "coreUI", "animatedModal"], function(swal, cardInterface, smashers, ui) {

    var $loginWrap = $(".login-wrap");
    var $openRegistrationButton = $("#open-registration");

    $openRegistrationButton.animatedModal({
        modalTarget: "registrationModal"
    });

    $loginWrap.find(".login-inputs input").keydown(function(e) {
        var key = e.keyCode || e.which;
        if (key === 13) {
            tryLogin();
        }
    })
    var $loginButton = $("#login-submit");

    var tryLogin = function() {

        var $inputs = $(".login-inputs").find("[name]");
        var toSend = {}
        var flag = false;
        var name, val;
        $inputs.each(function() {
            var $this = $(this)
            name = $this.attr("name");
            val = $this.val()

            if (name !== "password") {
                val = val.toLowerCase().trim();
            }

            if((name == "password" || name == "username") && val === "") {
                flag = true;
                swal({
                    type: 'error',
                    timer: 4000,
                    title: "You forgot to fill in your " + name,
                    text: "You got this." 
                })
                return false;
            }

            toSend[name] = val;
        });
        if (flag === true) {
            return;
        }

        $.ajax({
            url:"/api/v1/user/login/", 
            data: JSON.stringify(toSend),
            contentType: "application/json",
            dataType: 'json',
            type: "POST"
        }).success(function(response) {
            if (response.success === true) {
                smashers.setActiveUser(response.user);
                console.log(response.user)
                ui.setNumMatches(response.user.num_matches)
                $(".logged-out-content").fadeOut("fast", function() {
                    $("#login-stylesheet").remove();
                    $(".logged-in-content").fadeIn("fast", function() {
                        cardInterface.activeSet().getNextSwipeSet();
                    });
                });
            }
        }).error(function(response) {
            swal({
                type: "error",
                title: "Make sure you register!",
                text: "It looks like your username or password was incorrect, or you forgot to register."
            })
        })
    }

    var failmessage = "Either we don't have your email in our database, or someone has already registered that address. Check the email address for a registration link. Search your spam folder.";

    var tryRegistration = function() {
        var $this = $(this);
        var $form = $this.closest(".form");
        var toSend = {}
        var flag = false;
        $form.children("input").each(function() {
            var $t = $(this);
            var val = $t.val();
            var name = $t.attr("name");
            if (name !== "password1" && name !== "password2") {
                val = val.toLowerCase().trim()
            }
            toSend[name] = val;

            if (name == "username" && val.indexOf(" ") !== -1) {
                flag = true;
                $form.prepend("<p style='color: red'>No spaces allowed in username</p>")
                return false;
            }

            if (val === "") {
                flag = true;
                swal({
                    type: "error",
                    title: "You can't leave any fields blank.",
                    timer: 2000
                })
            }
        });

        if (toSend.password1 !== toSend.password2) {
            swal({
                type: "error",
                title: "Passwords don't match",
                text: "You need to make your passwords match!",
                timer: 2000
            });
            flag = true;
        }

        if (flag === false) {
            $.post("/accounts/register/", toSend, function(response) {
                if (response == 0) {
                    swal({
                        type: "error",
                        title: "Something went wrong",
                        text: failmessage
                    })
                }
                else {
                    swal({
                        type: "success",
                        title: "Nice! Check your email!",
                        text: "Check your email for a validation link! Then you can get 'smashing' ;)"
                    })
                }
            }, 'json').error(function(response){
                swal({
                    type: "error",
                    title: "Something went wrong",
                    text: failmessage
                })
            })
        }

    }

    $loginButton.click(tryLogin);

    var $registerButton = $("#register");

    $registerButton.click(tryRegistration);
});