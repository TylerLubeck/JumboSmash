define("login", ["sweetalert", "cardInterface", "smashers", "animatedModal"], function(swal, cardInterface, smashers) {

    var $loginWrap = $(".login-wrap");
    var $openRegistrationButton = $("#open-registration");
    var $registerButton = $("#register");

    $registerButton.click(tryRegistration);

    $openRegistrationButton.animatedModal({
        modalTarget: "registrationModal"
    });

    $loginWrap.find("input").keydown(function(e) {
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
            val = $this.val();

            // if((name == "password" || name == "username") && val === "") {
            //     flag = true;
            //     swal({
            //         type: 'error',
            //         timer: 4000,
            //         title: "You forgot to fill in your " + name,
            //         text: "You got this." 
            //     })
            // }

            // if (name === "username") {
            //     if (val.indexOf("tufts.edu") === -1) {
            //         flag = true;
            //         swal({
            //             type: "error",
            //             timer: 5000,
            //             title: "Your username must be a tufts email.",
            //             text: "If you have not registered (it's really easy!), you should do that now."
            //         })
            //         return false;
            //     }
            // }

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
            console.log(response);
            if (response.success === true) {
                $(".logged-out-content").fadeOut("fast", function() {
                    $("#login-stylesheet").remove();
                    $(".logged-in-content").fadeIn("fast", function() {
                        cardInterface.activeSet().getNextSwipeSet();
                    });
                });
            }
        }).error(function(response) {
            console.log(response);
        })
    }

    var tryRegistration = function() {

    }

    $loginButton.click(tryLogin);
});