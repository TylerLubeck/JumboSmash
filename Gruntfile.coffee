module.exports = (grunt) =>

    grunt.initConfig
        compass:
            dist:
                options:
                    sassDir: 'smashers/static/smashers/sass'
                    cssDir: 'smashers/static/smashers/stylesheets'
                    environment: 'production'
            dev:
                options:
                    watch: true
                    sassDir: 'smashers/static/smashers/sass'
                    cssDir: 'smashers/static/smashers/stylesheets'
        watch:
          # node: 
          #   files: ['app.js']
          #   tasks: ["nodemon:dev"]
          sass:
            files: ["smashers/static/smashers/sass/*.scss"]
            tasks: ["compass:dev"]
          # css:
          #   files: ["*.css"]
          # coffee:
          #   files: ['app/static/modules/src/*.coffee']
          #   tasks: ['coffee:dist']
          # livereload:
          #   files: ["app/static/stylesheets/*.css"]
          #   options:
          #     livereload: true

    grunt.loadNpmTasks 'grunt-contrib-watch'
    grunt.loadNpmTasks 'grunt-contrib-compass'
    # grunt.loadNpmTasks 'grunt-contrib-coffee'

    # grunt.registerTask 'server', (target) ->
    #   nodemon = grunt.util.spawn
    #       cmd: 'grunt'
    #         grunt: true
    #         args: 'nodemon'

    grunt.registerTask "default", ['watch']

