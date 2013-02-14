jQuery.noConflict();

var init_topic_search = function () {
    var topicsSearch = null;
    var b = null;
    var url = null;

    b = jQuery('base').attr('href');
    if (b[b.length -1] != '/') {
        b = b + '/';
    }
    url = b + 'gs-group-topics-ajax.html';
    topicsSearch = GSSearch('#gs-group-messages-topics-search', 
                            url, 0, 6, {}, null);
    topicsSearch.load();
    jQuery('#gs-group-messages-topics-search').on('resultsloaded', function () {
        jQuery('abbr[role=tooltip]').tooltip();
        jQuery('#gs-group-messages-base-tabs-buttons li:first-child a').click();
    });
}

// Connect to the DOM being ready, rather than the window loading, so the 
// topics can load while all the other assets are being downloaded
jQuery(document).ready(function () {
    gsJsLoader.with_module('/++resource++gs-search-base-js-20121217.js',
                           init_topic_search);
});
