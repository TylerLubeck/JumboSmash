({
    mainConfigFile : "./smashers/static/smashers/scripts/app.js",
    baseUrl: "./smashers/static/smashers/scripts",
    waitSeconds: 15,
    // urlArgs : "bust="+ new Date().getTime(), 
    paths: {
        "jquery"        : "bower_components/jquery/dist/jquery.min",
        "underscore"    : "bower_components/underscore/underscore-min",
        "backbone"      : "bower_components/backbone/backbone",
        "animatedModal" : "animatedModal/animatedModal.min",
        "sweetalert"    : "bower_components/sweetalert/lib/sweet-alert.min"
    },
    name: "app",
    findNestedDependencies: true,
    out: "./smashers/static/smashers/scripts/app-built.js"

})
