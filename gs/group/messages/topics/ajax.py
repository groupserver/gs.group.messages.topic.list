# coding=utf-8
from math import log10
from zope.cachedescriptors.property import Lazy
from zope.component import createObject
from gs.group.base.page import GroupPage
from Products.GSSearch.queries import MessageQuery
from Products.XWFCore.cache import LRUCache
from Products.XWFMailingListManager.stopwords import en as STOP_WORDS

class TopicsAjax(GroupPage):
    topicKeywords = LRUCache("TopicKeywords")
    @Lazy
    def messageQuery(self):
        da = self.context.zsqlalchemy
        retval  = MessageQuery(self.context, da)
        return retval

    @Lazy
    def searchTokens(self):
        return createObject('groupserver.SearchTextTokens', "")
    
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
        return self.messageQuery.topic_search_keyword(
                self.searchTokens, self.siteInfo.id, 
                [self.groupInfo.id], limit=self.limit, 
                offset=self.offset)
        
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

    def topics(self):
        '''Generator, which returns the topics'''
        topics = self.rawTopicInfo
        for topic in topics:
            topic['files'] = self.files_for_topic(topic)
            topic['keywords'] = self.keywords_for_topic(topic)
            yield topic

def tfidf_sort(a, b):
    if a['tfidf'] < b['tfidf']:
        retval = 1
    elif a['tfidf'] == b['tfidf']:
        retval = 0
    else:
        retval = -1
    return retval

