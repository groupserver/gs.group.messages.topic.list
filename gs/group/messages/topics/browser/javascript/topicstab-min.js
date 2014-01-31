jQuery.noConflict();function init_topic_search(){var c=null,a=null,d=null,e="#gs-group-messages-topics-search";
a=jQuery("base").attr("href");if(a[a.length-1]!="/"){a=a+"/"}d=a+"gs-group-topics-ajax.html";
c=GSSearch(e,d,0,6,{},null);jQuery(e).on("resultsloaded",function(){jQuery("abbr[role=tooltip]").tooltip()
});jQuery("#gs-group-messages-base-tabs-buttons li:first-child a").click();c.load()
}jQuery(document).ready(function(){gsJsLoader.with_module("/++resource++gs-search-base-js-min-20131121.js",init_topic_search)
});jQuery(window).load(function(){var a=null,b=null;if(jQuery("#gs-group-messages-topics-postinginfo").length!=0){a=jQuery("#gs-group-messages-topics-postinginfo-privacy").html();
b={animation:true,html:true,placement:"bottom",trigger:"click",content:a};jQuery("#gs-group-messages-topics-postinginfo-privacy-summary").popover(b)
}});