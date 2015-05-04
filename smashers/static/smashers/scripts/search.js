define("search", ["typeahead", "smashers", "cardInterface"], function(typeahead, smashers, cardInterface) {

    var $searchbar = $("#smash-autocomplete");

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

    function loadSmashers(people) {
        var engine = new Bloodhound({
            local: people,
            datumTokenizer: function(d) {
                return Bloodhound.tokenizers.whitespace(d.name);
            },
            queryTokenizer: Bloodhound.tokenizers.whitespace,
            limit: 10
        });
        engine.initialize(true)

        $searchbar.typeahead(
            {
                hint: false,
                minLength: 2,
                highlight: true
            }, 
            {
                source: engine.ttAdapter(),
                displayKey: "name",
                templates: {
                    empty: "<div class='tt-empty-results'>No results found.</div>",
                    suggestion: _.compile($("#suggestion-template").html())
                }
            }
        ).on("typeahead:selected", function(e, suggestion) {
            $searchbar.typeahead("val", "")
            $searchbar.blur()
            $searchbar.typeahead("blur");
            var s = smashers.getSmasher({id: suggestion.pk});
            s.fetch().success(function() {
                cardInterface.activeSet().add(s)
            })
        });

    }

    return loadSmashers;
})
