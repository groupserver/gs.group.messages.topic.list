================================
``gs.group.messages.topic.list``
================================
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The list of topics in a GroupServer group
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Author: `Michael JasonSmith`_
:Contact: Michael JasonSmith <mpj17@onlinegroups.net>
:Date: 2015-02-24
:Organization: `GroupServer.org`_
:Copyright: This document is licensed under a
  `Creative Commons Attribution-Share Alike 4.0 International License`_
  by `OnlineGroups.net`_.


Introduction
============

Posts [#posts]_ made to a GroupServer group are organised into
*topics* [#topics]_. This product is responsible for displaying
the different topic lists:

* The topics tab_, and 
* The topics page_.


Tab
===

Most groups display a list of topics on the *group page*
[#group]_ (with Announcement groups being the exception). The tab
is a viewlet_, that uses AJAX_ is used to load the list of
topics, which is controlled by JavaScript_

Viewlet
-------

The viewlet ``gs-group-messages-topics-tab`` all the code for the
tab, except for the list of topics itself, which is supplied by
the AJAX_. The tab depends on the viewlet manager
``gs.group.messages.base.interfaces.IGroupHomepageMessages``,
which is used by the *Posts* tab as well.

Because the *New topic* button is displayed by the Topics viewlet
this product depends on ``gs.group.member.canpost``.

The viewlet ends with links to the *Topics* page_ and the ATOM
feed for the topics.

AJAX
----

The contents of the Topics tab is loaded from the page
``gs-group-topics-ajax.html`` within the group context, using
AJAX. (The page is not viewed directly by people, so it does not
have a human-friendly name.) The same page provides an interface
to the search system [#search]_.

The Topics list provided by the AJAX is designed to provide many
cues to information retrieval (or *information scent*). For each
topic the following metadata is provided:

* A *Sticky* marker is shown if the topic has been marked sticky
  by an administrator. Sticky topics are always listed first.

* The name of the topic (the *Subject*).

* The number of posts.

* The number of files. Hovering over the number of files shows
  icons for the files posted to the topic.

* Who wrote the most recent post, and when it was posted.

* Keywords extracted from the topic. Clicking on a keyword
  performs a search for other topics that contain that keyword.

The CSS for the topics list makes heavy use of *muted* text, to
provide a hierarchy of information.

JavaScript
----------

The JavaScript resource
``/++resource++gs-group-messages-topics-tab-20130111.js``
provides the code for running the viewlet_ and AJAX_. The topics
are loaded as the DOM is ready (using the
``jQuery(document).ready`` event), unlike most of the JavaScript
for GroupServer that is bound to the page loading event
(``jQuery(window).load``, so they appear to load faster.

Page
====

The Topics page is obscure: it is a method of viewing the topics
without using AJAX. It mostly exists for Search engines, or the
very few users without JavaScript that want to read a public
group.

Resources
=========

- Code repository:
  https://github.com/groupserver/gs.group.messages.topic.list
- Translations:
  https://www.transifex.com/projects/p/gs-group-messages-topic-list/
- Questions and comments to
  http://groupserver.org/groups/development
- Report bugs at https://redmine.iopen.net/projects/groupserver

.. _GroupServer: http://groupserver.org/
.. _GroupServer.org: http://groupserver.org/
.. _OnlineGroups.Net: https://onlinegroups.net
.. _Michael JasonSmith: http://groupserver.org/p/mpj17
..  _Creative Commons Attribution-Share Alike 4.0 International License:
    http://creativecommons.org/licenses/by-sa/4.0/

..  [#posts] Posts are displayed by the ``gs.group.messages.post`` 
    product <https://github.com/groupserver/gs.group.messages.post>

..  [#topics] Topics are displayed by the ``gs.group.messages.topic.base`` 
    product <https://github.com/groupserver/gs.group.messages.topic.base>

..  [#group] The group page is provided by the ``gs.group.home`` 
    product <https://github.com/groupserver/gs.group.home>

..  [#search] See ``gs.search.base`` for more information on the Search
              system <https://github.com/groupserver/gs.search.base>
