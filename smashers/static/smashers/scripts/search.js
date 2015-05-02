define("search", [], function() {

    $searchbar = $("#smash-autocomplete");

    (function (_) {
        'use strict';

        _.compile = function (templ) {
            var compiled = this.template(templ);
            compiled.render = function (ctx) {
                return this(ctx);
            }
            return compiled;
        }
    })(window._);

    function loadSmashers(smashers) {
        var engine = new Bloodhound({
            local: smashers,
            datumTokenizer: function(d) {
                return Bloodhound.tokenizers.whitespace(d.val);
            },
            queryTokenizer: Bloodhound.tokenizers.whitespace,
            limit: 10
        });
        engine.initialize()

        $searchbar.typeahead(
            {
                hint: true,
                minLength: 1,
                highlight: true
            }, 
            {
                displayKey: "val",
                templates: {
                    empty: "<div class='tt-empty-results'>No results found.</div>",
                    suggestion: _.compile($("#suggestion-template").html())
                }
            }
        ).on("typeahead:selected", function(e, suggestion) {
            console.log(suggestions)
            $searchbar.typeahead("val", "")
        });

    }

    return loadSmashers;
})
