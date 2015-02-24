Changelog
=========

5.0.0 (2015-02-24)
------------------

* Renaming the product `gs.group.messages.topic.list`_ from
  ``gs.group.messages.topics``

.. _gs.group.messages.topic.list:
   https://github.com/groupserver/gs.group.messages.topic.list

4.4.0 (2014-11-12)
------------------

* Using the new ``IMessagesPrivacy`` adaptor from
  `gs.group.messages.privacy`_

.. _gs.group.messages.privacy: https://github.com/groupserver/gs.group.messages.privacy

4.3.3 (2014-10-10)
------------------

* Switching to GitHub as the primary code repository
* Naming the reStructuredText files as such

4.3.2 (2014-06-24)
------------------

* Refactor of the *Posts* tab to make it WAI-ARIA compliant

4.3.1 (2014-03-13)
------------------

* Switching to ``"use strict";`` in the JavaScript
* Unicode and general code cleanup

4.3.0 (2014-01-31)
------------------

* Adding a privacy disclosure to the posting-information content
  provider

4.2.0 (2013-11-26)
------------------

* Using the new loading-character
* Adding a *failed* state to the page-template
* Following the new core JavaScript search code

4.1.2 (2013-06-13)
------------------

* Fixing the link to the *New topic* page
* Following jQuery to its new home (``gs.content.js.jquery.base``)

4.1.1 (2013-05-10)
------------------

* Fixing the ID of the topic-tab script

4.1.0 (2013-04-08)
------------------

* Updating the *Topics* page to bring it in line with the new UI
* Better formatting of the keywords and file-icons

4.0.0 (2013-02-26)
------------------

* Switch to Twitter Bootstrap (``gs.content.js.bootstrap``) from
  JQuery.UI
* Using the new JavaScript loader (``gs.content.js.loader``) to
  load the search JS
* Using Unicode characters for the file icons
* Moving the posting-information to its own viewlet

3.1.0 (2013-01-22)
------------------

* A fix for Microsoft Internet Explorer 7
* Fixing the ``canPost`` property
* Moving the *Topics* tab to the new *messages* viewlet manager

3.0.0 (2012-09-26)
------------------

* Using full-text retrieval (FTR) to perform the search
* Moved the queries here from ``Products.XWFMailingListManager``
* Use the new ``keyword`` column in the ``topic`` table

2.1.3 (2012-08-08)
------------------

* Deal with missing (deleted) user-profiles

2.1.2 (2012-05-27)
------------------

* Fix topics

2.1.1 (2012-05-22)
------------------

* Update to SQLAlchemy

2.1.0 (2012-06-06)
------------------

* Rely on ``gs.group.messages.base`` to supply the core
  JavaScript

2.0.0 (2012-05-17)
------------------

* Initial version (code originally from
  ``gs.group.messages.topic``)

..  LocalWords:  GitHub reStructuredText
