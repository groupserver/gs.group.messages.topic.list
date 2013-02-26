# coding=utf-8
from zope.cachedescriptors.property import Lazy
from zope.component import getMultiAdapter
from gs.group.member.canpost.interfaces import IGSPostingUser
from gs.group.home.simpletab import UserInfoTab


class TopicsTab(UserInfoTab):
    def __init__(self, group, request, view, manager):
        UserInfoTab.__init__(self, group, request, view, manager)

    @Lazy
    def canPost(self):
        retval = getMultiAdapter((self.groupInfo.groupObj, self.loggedInUser),
                                    IGSPostingUser)
        return retval
