# -*- coding: utf-8 -*-
from zope.cachedescriptors.property import Lazy
from zope.component import getMultiAdapter
from Products.GSGroup.interfaces import IGSMailingListInfo
from gs.group.member.canpost.interfaces import IGSPostingUser
from gs.group.home.simpletab import UserInfoTab


class PostingInfo(UserInfoTab):
    def __init__(self, group, request, view, manager):
        super(PostingInfo, self).__init__(group, request, view, manager)

    @Lazy
    def show(self):
        retval = self.canPost.canPost
        return retval

    @Lazy
    def canPost(self):
        retval = getMultiAdapter((self.groupInfo.groupObj, self.loggedInUser),
                                    IGSPostingUser)
        return retval

    @Lazy
    def email(self):
        l = IGSMailingListInfo(self.groupInfo.groupObj)
        retval = l.get_property('mailto')
        return retval