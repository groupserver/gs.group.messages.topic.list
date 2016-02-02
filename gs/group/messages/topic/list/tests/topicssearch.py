# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2016 OnlineGroups.net and Contributors.
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
from __future__ import absolute_import, unicode_literals, print_function
from mock import MagicMock, patch, PropertyMock
from unittest import TestCase
from gs.group.messages.topic.list.topicssearch import (TopicsSearch, )


class TestTopicsSearch(TestCase):
    @patch.object(TopicsSearch, 'groupInfo', new_callable=PropertyMock)
    def test_marshall_file(self, m_gI):
        TopicsSearch.groupInfo.relativeURL = '/groups/example_group'
        f = {'file_name': 'example', 'post_id': 'eg123', 'mime_type': 'application/x-gs-test', }
        ts = TopicsSearch(MagicMock(), '', 6, 0)
        r = ts.marshall_file(f)

        self.assertIn('name', r)
        self.assertIn('url', r)
        self.assertEqual('/groups/example_group/messages/topic/eg123/#post-eg123', r['url'])
        self.assertIn('icon', r)

    @patch.object(TopicsSearch, 'sticky_plus_recent')
    @patch.object(TopicsSearch, 'just_recent')
    @patch.object(TopicsSearch, 'normal_search')
    def test_raw_topic_info(self, m_n_s, m_j_r, m_s_p_r):
        'Test that we show the recent and sticky when not searching for anything'
        m_s_p_r.return_value = ['item', ]
        searchTokens = MagicMock()
        searchTokens.searchText = ''
        ts = TopicsSearch(MagicMock(), searchTokens, 6, 0)
        r = ts.rawTopicInfo

        m_s_p_r.assert_called_once_with()
        self.assertEqual(r, m_s_p_r())
        self.assertEqual(0, m_n_s.call_count)
        self.assertEqual(0, m_j_r.call_count)

    @patch.object(TopicsSearch, 'sticky_plus_recent')
    @patch.object(TopicsSearch, 'just_recent')
    @patch.object(TopicsSearch, 'normal_search')
    def test_raw_topic_info_searching(self, m_n_s, m_j_r, m_s_p_r):
        'Test that we show the items when searching'
        m_n_s.return_value = ['item', ]
        searchTokens = MagicMock()
        searchTokens.searchText = 'foo'
        ts = TopicsSearch(MagicMock(), searchTokens, 6, 1)
        r = ts.rawTopicInfo

        self.assertEqual(0, m_s_p_r.call_count)
        m_n_s.assert_called_once_with()
        self.assertEqual(r, m_n_s())
        self.assertEqual(0, m_j_r.call_count)

    @patch.object(TopicsSearch, 'sticky_plus_recent')
    @patch.object(TopicsSearch, 'just_recent')
    @patch.object(TopicsSearch, 'normal_search')
    def test_raw_topic_info_paging(self, m_n_s, m_j_r, m_s_p_r):
        'Test that we page through the items'
        m_j_r.return_value = ['item', ]
        searchTokens = MagicMock()
        searchTokens.searchText = ''
        ts = TopicsSearch(MagicMock(), searchTokens, 6, 1)
        r = ts.rawTopicInfo

        self.assertEqual(0, m_s_p_r.call_count)
        self.assertEqual(0, m_n_s.call_count)
        m_j_r.assert_called_once_with()
        self.assertEqual(r, m_j_r())
