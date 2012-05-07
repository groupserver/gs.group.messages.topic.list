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
    def offset(self):
        retval = int(self.request.get('i', 0))
        assert retval >= 0
        return retval
    
    @Lazy
    def limit(self):
        retval = int(self.request.get('l', 12)) % 48
        assert retval >= 0
        return retval
    
    @Lazy
    def rawTopicInfo(self):
        retval = self.messageQuery.topic_search_keyword(
              self.searchTokens, self.siteInfo.id,
              [self.groupInfo.id], limit=self.limit, offset=self.offset)
        return retval
        
    @Lazy
    def topicFiles(self):
        tIds = [t['topic_id'] for t in self.rawTopicInfo]
        retval = self.messageQuery.files_metadata_topic(tIds)
        return retval

    def files_for_topic(self, topic):
        retval = [{
                'name': f['file_name'],
                'url': '/r/topic/%s#post-%s' % (f['post_id'], f['post_id']),
                'icon': f['mime_type'].replace('/','-').replace('.','-'),
            } for f in self.topicFiles 
                if f['topic_id'] == topic['topic_id']]
        return retval
        
    def topics(self):
        '''Generator, which returns the topics'''
        topics = self.rawTopicInfo
        for topic in topics:
            topic['files'] = self.files_for_topic(topic)
            yield topic

