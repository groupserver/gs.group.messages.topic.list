Introduction
============

Posts [#posts]_ made to a GroupServer group are organised into *topics*
[#topics]_. This product here displays a list of topics on the *group 
page* [#group]_. 

The topics are displayed in a tab, entitled *Topics*. The contents of 
the tab is loaded from the page ``gs-group-topics-ajax.html`` within 
the group context, using AJAX. (The page is not viewed directly by 
people, so it does not have a human-friendly name.) The same page 
provides an interface to the search system. The same API is used for the
more generic search.

``i``:
    The *index,* or offset, into the list of results.

``l``:
    The number of results to return (the *length*).

``s``:
    The text to *search* for in the topics.

The group-identifier is skipped from the because the page can figure out
the group from the context.

..  Resources

..  [#posts] Posts are displayed by the ``gs.group.messages.post`` 
    product.
..  [#topics] Topics are displayed by the ``gs.group.messages.topic`` 
    product.
..  [#group] The group page is provided by the ``gs.group.home`` 
    product.

