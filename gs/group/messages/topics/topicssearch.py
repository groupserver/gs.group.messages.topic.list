# coding=utf-8
from math import log10
from zope.cachedescriptors.property import Lazy
from zope.component import createObject
from Products.GSSearch.queries import MessageQuery
from Products.XWFCore.cache import LRUCache
from Products.XWFMailingListManager.stopwords import en as STOP_WORDS
from queries import TopicsQuery

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
    def da(self):
        assert self.context
        retval = self.context.zsqlalchemy
        assert retval
        return retval
    
    @Lazy
    def messageQuery(self):
        retval  = MessageQuery(self.context, self.da)
        return retval

    @Lazy
    def topicsQuery(self):
        retval  = TopicsQuery(self.da)
        return retval

    def topics(self):
        '''The main method, returns a generator for the list of topics'''
        topics = self.rawTopicInfo
        for topic in topics:
            topic['files'] = self.files_for_topic(topic)
            topic['keywords'] = self.keywords_for_topic(topic)
            topic['last_author'] = self.last_author_for_topic(topic)
            yield topic
        
    @Lazy
    def rawTopicInfo(self):
        if ((self.offset == 0) and (not self.searchTokens.searchText)):
            retval = self.sticky_plus_recent()
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
                    self.siteInfo.id, self.groupInfo.id, limit)
        retval = s + r
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
        
    def keywords_for_topic(self, topic):
        retval = self.topicKeywords.get(topic['last_post_id'])
        if not retval:
            retval = self.generate_keywords_for_topic(topic)
            self.topicKeywords.add(topic['last_post_id'], retval)
        return retval

    @Lazy
    def topicsWordCounts(self):
        tIds = [t['topic_id'] for t in self.rawTopicInfo]
        retval = self.messageQuery.topics_word_count(tIds)
        return retval
    
    @Lazy
    def totalTopicCount(self):
        return self.messageQuery.count_topics()
        
    @Lazy
    def wordCounts(self):
        return self.messageQuery.word_counts()
        
    def generate_keywords_for_topic(self, topic):
        tId = topic['topic_id']
        topicWords = [tw for tw in self.topicsWordCounts 
                        if tw['topic_id'] == tId]
        twc = float(sum([w['count'] for w in topicWords]))
        wc = self.wordCounts
        retval = [{ 'word':  w['word'],
                    'tfidf': (w['count']/twc)*\
                              log10(self.totalTopicCount/\
                                    float(wc.get('word', 1)))}
                for w in topicWords
                if ((len(w['word']) > 3) and 
                     (w['word'] not in STOP_WORDS))]
        retval.sort(tfidf_sort)
        return retval

    def last_author_for_topic(self, topic):
        userId = topic['last_post_user_id']
        authorInfo = self.authorCache.get(userId)
        if not authorInfo:
            ui = createObject('groupserver.UserFromId', 
                                    self.context, userId)
            authorInfo = {
                'id':       ui.id,
                'exists':   not ui.anonymous,
                'url':      ui.url,
                'name':     ui.name,
                'onlyURL':  '#' # TODO: Fix
            }
            self.authorCache.add(userId, authorInfo)
        assert authorInfo
        assert authorInfo['id'] == userId
        return authorInfo

def tfidf_sort(a, b):
    if a['tfidf'] < b['tfidf']:
        retval = 1
    elif a['tfidf'] == b['tfidf']:
        retval = 0
    else:
        retval = -1
    return retval

