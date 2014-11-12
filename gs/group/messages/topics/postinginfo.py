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
from Products.GSGroup.interfaces import IGSMailingListInfo
from gs.group.member.canpost.interfaces import IGSPostingUser
from gs.group.home.simpletab import UserInfoTab
from gs.group.messages.privacy.interfaces import IMessagesPrivacy


class PostingInfo(UserInfoTab):
    def __init__(self, group, request, view, manager):
        super(PostingInfo, self).__init__(group, request, view, manager)

    @Lazy
    def show(self):
        retval = self.canPost.canPost
        return retval

    @Lazy
    def canPost(self):
        retval = getMultiAdapter((self.groupInfo.groupObj,
                                  self.loggedInUser), IGSPostingUser)
        return retval

    @Lazy
    def email(self):
        l = IGSMailingListInfo(self.groupInfo.groupObj)
        retval = l.get_property('mailto')
        return retval

    @Lazy
    def privacy(self):
        retval = IMessagesPrivacy(self.context)
        print retval
        return retval
