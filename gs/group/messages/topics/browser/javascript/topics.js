// GroupServer module for providing the Topics tab in a group.
jQuery.noConflict();
GSGroupTopicTab = function () {
    // Private variables
    // Widgets
    var prevButton = null;
    var moreButton = null;
    var nextButton = null;
    var latestTopics = null;
    var loadingMessage = null;
    // Search Info
    var ajaxPage = 'gs-group-topics-ajax.html';
    var offset = null;
    var limit = null;
    var MAX_ITEMS = 48;
    
    // Private methods
    
    // Next button
    var init_next_button = function() {
        nextButton = jQuery('#gs-group-messages-topics-toolbar-next');
        nextButton.button({
            text: true,
            icons: { primary: 'ui-icon-carat-1-e', },
            disabled: false,
        });
        nextButton.click(handle_next);
    };// init_next_button
    var handle_next = function(eventObject) {
        offset = offset + limit;
        latestTopics.fadeOut('slow', 'swing', do_topics_load);
    };//handle_next
    
    // More button
    var init_more_button = function() {
        moreButton = jQuery('#gs-group-messages-topics-toolbar-more');
        moreButton.button({
            text: true,
            icons: { primary: 'ui-icon-carat-1-s', },
            disabled: false,
        });
        moreButton.click(handle_more);
    };// init_more_button
    var handle_more = function(eventObject) {
        limit = limit * 2;
        if (limit >= MAX_ITEMS) {
            limit = MAX_ITEMS;
            moreButton.button('options', 'disabled', true);
        }
        latestTopics.fadeOut('slow', 'swing', do_topics_load);
    };//handle_more
    
    // Previous Button
    var init_prev_button = function() {
        prevButton = jQuery('#gs-group-messages-topics-toolbar-prev');
        prevButton.button({
            text: true,
            icons: { primary: 'ui-icon-carat-1-w', },
            disabled: true,
        });
        prevButton.click(handle_prev);
    };// init_prev_button
    var handle_prev = function(eventObject) {
        offset = offset - limit;
        if (offset < 0) {
            offset = 0
        }
        latestTopics.fadeOut('slow', 'swing', do_topics_load);
    };//handle_prev
    
    // Code to load the topics in a pleasing way.
    var do_topics_load = function () {
        // Function used by the buttons.
        loadingMessage.fadeIn('slow', 'swing', load_topics);
    };//do_topics_load
    var load_topics = function() {
        // Actually load the topics, making am AJAX request
        var data = {
            'i': offset,
            'l': limit,
        };
        latestTopics.load(ajaxPage, data, load_complete);
    };// load_topics
    var load_complete = function(responseText, textStatus, request) {
        // Hide the Loading message 
        loadingMessage.fadeOut('slow', 'swing', show_topics);
    };// load_complete
    var show_topics = function () {
        // Show the topics list
        latestTopics.fadeIn('slow', 'swing');
        prevButton.button('option', 'disabled', offset <= 0);
    };//show_topics

    // Public methods and properties.
    return {
        init: function (groupId) {
            limit = 12;
            offset = 0;
        
            init_prev_button();
            init_more_button()
            init_next_button();
            latestTopics = jQuery('#gs-group-messages-topics-latest');
            loadingMessage = jQuery('#gs-group-messages-topics-loading');
            load_topics();
        },//init
    };
}(); // GSVerifyEmailAddress
jQuery(document).ready( function () {
    GSGroupTopicTab.init()
});
