// GroupServer module for providing the Topics tab in a group.
jQuery.noConflict();
GSGroupTopicTab = function () {
    // Private variables
    var prevButton = null;
    var nextButton = null;
    var latestTopics = null;
    var loadingMessage = null;
    
    // Private methods
    
    var init_prev_button = function() {
        prevButton = jQuery('#gs-group-messages-topics-toolbar-prev');
        prevButton.button({
            text: true,
            icons: { primary: 'ui-icon-carat-1-w', },
            disabled: true,
        });
    };// init_prev_button
    
    var init_next_button = function() {
        nextButton = jQuery('#gs-group-messages-topics-toolbar-next');
        nextButton.button({
            text: true,
            icons: { primary: 'ui-icon-carat-1-e', },
            disabled: true,
        });
    };// init_next_button
    
    var load_topics = function() {
        latestTopics.load('gs-group-topics-ajax.html');
        loadingMessage.fadeOut('slow', 'swing', show_topics);
    };// load_topics
    
    var show_topics = function () {
        latestTopics.fadeIn('slow', 'swing')
    }
    
    // Public methods and properties.
    return {
        init: function (groupId) {
            init_prev_button();
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
