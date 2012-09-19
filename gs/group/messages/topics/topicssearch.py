# coding=utf-8
from zope.cachedescriptors.property import Lazy
from zope.component import createObject
from Products.GSSearch.queries import MessageQuery
from Products.XWFCore.cache import LRUCache
from queries import TopicsQuery

from logging import getLogger
log = getLogger('gs.group.messages.topics.TopicsSearch')


class TopicsSearch(object):
    topicKeywords = LRUCache("TopicKeywords")
    authorCache = LRUCache("Author")

    def __init__(self, group, searchTokens, limit, offset):
        self.context = self.group = group
        self.searchTokens = searchTokens
        self.limit = limit
        self.offset = offset

    @Lazy
    def groupInfo(self):
        retval = createObject('groupserver.GroupInfo', self.context)
        return retval

    @Lazy
    def siteInfo(self):
        retval = createObject('groupserver.SiteInfo', self.context)
        return retval

    @Lazy
    def loggedInUser(self):
        retval = createObject('groupserver.LoggedInUser', self.context)
        return retval

    @Lazy
    def messageQuery(self):
        retval = MessageQuery(self.context)
        return retval

    @Lazy
    def topicsQuery(self):
        retval = TopicsQuery()
        return retval

    def topics(self):
        '''The main method, returns a generator for the list of topics'''
        topics = self.rawTopicInfo
        for topic in topics:
            topic['files'] = self.files_for_topic(topic)
            topic['last_author'] = self.last_author_for_topic(topic)
            yield topic

    @Lazy
    def rawTopicInfo(self):
        if ((not self.searchTokens.searchText) and (self.offset == 0)):
            retval = self.sticky_plus_recent()
        elif ((not self.searchTokens.searchText) and (self.offset != 0)):
            retval = self.just_recent()
        else:
            retval = self.normal_search()
        assert type(retval) == list
        return retval

    def normal_search(self):
        retval = self.messageQuery.topic_search_keyword(
                self.searchTokens, self.siteInfo.id,
                [self.groupInfo.id], limit=self.limit,
                offset=self.offset)
        return retval

    def sticky_plus_recent(self):
        s = self.topicsQuery.sticky_topics(self.siteInfo.id,
                                            self.groupInfo.id)
        limit = max([self.limit - len(s), 0])
        r = []
        if limit:
            r = self.topicsQuery.recent_non_sitcky_topics(
                    self.siteInfo.id, self.groupInfo.id, limit, 0)
        retval = s + r
        return retval

    def just_recent(self):
        retval = self.topicsQuery.recent_non_sitcky_topics(
                    self.siteInfo.id, self.groupInfo.id, self.limit,
                    self.offset)
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
                'icon': f['mime_type'].replace('/', '-').replace('.', '-'),
            } for f in self.topicFiles
                if f['topic_id'] == topic['topic_id']]
        return retval

    def last_author_for_topic(self, topic):
        # TODO: Implement cache
        userId = topic['last_post_user_id']
        #authorInfo = self.authorCache.get(userId)
        #if not authorInfo:
        #    print 'not from cache'
        ui = createObject('groupserver.UserFromId',
                          self.context, userId)
        authorInfo = {
            'id': ui.id,
            'exists': not ui.anonymous,
            'url': ui.url,
            'name': ui.name,
            'onlyURL': '#'  # FIXME: Figure out what onlyURL is for
        }
        #    self.authorCache.add(userId, authorInfo)

        assert authorInfo, "Author info was not created"
        if  authorInfo['id'] != userId:
            m = 'authorInfo ID (%s) did not equal userId (%s) for the topic '\
                '"%s". Was the user "%s" deleted?' % \
                (authorInfo['id'], userId, topic['topic_id'], userId)
            log.warning(m)
        return authorInfo
