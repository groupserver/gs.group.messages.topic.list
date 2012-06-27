# coding=utf-8
import sqlalchemy as sa
from gs.database import getTable, getSession

class TopicsQuery(object):
    def __init__(self):
        self.topicTable = getTable('topic')
        self.postTable = getTable('post')
        
    def marshal_topic_info(self, x):
        assert x
        retval = {
            'topic_id':             x['topic_id'],
            'group_id':             x['group_id'], 
            'site_id':              x['site_id'], 
            'subject':              x['original_subject'], 
            'sticky':               x['sticky'],
            'num_posts':            x['num_posts'],
            'first_post_id':        x['first_post_id'], 
            'last_post_id':         x['last_post_id'], 
            'last_post_date':       x['last_post_date'], 
            'last_post_user_id':    x['user_id'],}
        assert type(retval) == dict
        assert retval
        return retval

    def sticky_topics(self, siteId, groupId):
        tt = self.topicTable
        pt = self.postTable

        cols = [tt.c.topic_id.distinct(), tt.c.last_post_id, 
                tt.c.first_post_id, tt.c.group_id, tt.c.site_id, 
                tt.c.original_subject, tt.c.last_post_date, 
                tt.c.num_posts, tt.c.sticky,
                sa.select([pt.c.user_id], 
                            tt.c.last_post_id == pt.c.post_id).label('user_id')]

        s = sa.select(cols, order_by=sa.desc(tt.c.last_post_date))
        s.append_whereclause(tt.c.site_id == siteId)
        s.append_whereclause(tt.c.group_id == groupId)
        s.append_whereclause(tt.c.sticky != None)        
        s.append_whereclause(tt.c.hidden == None)

        session = getSession()
        r = session.execute(s)

        retval = [self.marshal_topic_info(x)for x in r]
        assert type(retval) == list
        return retval

    def recent_non_sitcky_topics(self, siteId, groupId, limit, offset):
        tt = self.topicTable
        pt = self.postTable

        cols = [tt.c.topic_id.distinct(), tt.c.last_post_id, 
                tt.c.first_post_id, tt.c.group_id, tt.c.site_id, 
                tt.c.original_subject, tt.c.last_post_date, 
                tt.c.num_posts, tt.c.sticky,
                sa.select([pt.c.user_id], 
                          tt.c.last_post_id == pt.c.post_id,  
                          ).label('user_id')]
        s = sa.select(cols, order_by=sa.desc(tt.c.last_post_date),
                            limit=limit, offset=offset)
        s.append_whereclause(tt.c.site_id == siteId)
        s.append_whereclause(tt.c.group_id == groupId)
        s.append_whereclause(tt.c.sticky == None)
        s.append_whereclause(tt.c.hidden == None)

        session = getSession()
        r = session.execute(s)

        retval = [self.marshal_topic_info(x)for x in r]
        assert type(retval) == list
        return retval

