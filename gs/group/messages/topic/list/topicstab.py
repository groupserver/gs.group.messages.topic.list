# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2013, 2014 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
############################################################################
from __future__ import absolute_import, unicode_literals
from zope.cachedescriptors.property import Lazy
from zope.component import getMultiAdapter
from gs.group.member.canpost.interfaces import IGSPostingUser
from gs.group.home.simpletab import UserInfoTab
from . import GSMessageFactory as _


class TopicsTab(UserInfoTab):
    def __init__(self, group, request, view, manager):
        super(TopicsTab, self).__init__(group, request, view, manager)
        self.title = _('topics-tab-title', 'Topics')

    @Lazy
    def canPost(self):
        retval = getMultiAdapter((self.groupInfo.groupObj,
                                  self.loggedInUser), IGSPostingUser)
        return retval
