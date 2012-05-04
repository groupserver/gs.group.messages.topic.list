# coding=utf-8
from zope.cachedescriptors.property import Lazy
from zope.component import createObject
from gs.group.base.page import GroupPage
from Products.GSSearch.queries import MessageQuery

class TopicsAjax(GroupPage):
    @Lazy
    def messageQuery(self):
        da = self.context.zsqlalchemy
        retval  = MessageQuery(self.context, da)
        return retval

    @Lazy
    def searchTokens(self):
        retval = createObject('groupserver.SearchTextTokens', "")
        return retval
        
    @Lazy
    def topics(self):
        retval = self.messageQuery.topic_search_keyword(
              self.searchTokens, self.siteInfo.id,
              [self.groupInfo.id], limit=10, offset=0)
        return retval

