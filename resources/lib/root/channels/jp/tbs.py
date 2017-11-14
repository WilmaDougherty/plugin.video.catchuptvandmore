# -*- coding: utf-8 -*-
"""
    Catch-up TV & More
    Copyright (C) 2017  SylvainCecchetto

    This file is part of Catch-up TV & More.

    Catch-up TV & More is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    Catch-up TV & More is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with Catch-up TV & More; if not, write to the Free Software Foundation,
    Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""

from bs4 import BeautifulSoup as bs
from resources.lib import utils
from resources.lib import common

# Initialize GNU gettext emulation in addon
# This allows to use UI strings from addon’s English
# strings.po file instead of numeric codes
_ = common.ADDON.initialize_gettext()

context_menu = []
context_menu.append(utils.vpn_context_menu_item())

URL_ROOT = 'http://news.tbs.co.jp'

URL_CONTENT = URL_ROOT + '/digest/%s.html'
# content

URL_STREAM = 'http://flvstream.tbs.co.jp/flvfiles/_definst_/newsi/digest/%s_1m.mp4/playlist.m3u8'
# content

NEWS_CONTENT = ['nb', '23', 'nst', 'jnn']

def channel_entry(params):
    """Entry function of the module"""
    if 'root' in params.next:
        return root(params)
    elif 'list_shows' in params.next:
        return list_shows(params)
    elif 'list_videos' in params.next:
        return list_videos(params)
    elif 'live' in params.next:
        return list_live(params)
    elif 'play' in params.next:
        return get_video_url(params)


@common.PLUGIN.mem_cached(common.CACHE_TIME)
def root(params):
    modes = []

    # Add News
    modes.append({
        'label': 'ニュース',
        'url': common.PLUGIN.get_url(
            action='channel_entry',
            next='list_videos_news',
            page='1',
            category='TBS ニュース',
            window_title='TBS ニュース'
        ),
        'context_menu': context_menu
    })

    # Add Weather
    modes.append({
        'label': '気象',
        'url': common.PLUGIN.get_url(
            action='channel_entry',
            next='list_videos_weather',
            category='TBS ニュース - 気象',
            window_title='TBS ニュース - 気象'
        ),
        'context_menu': context_menu
    })

    return common.PLUGIN.create_listing(
        modes,
        sort_methods=(
            common.sp.xbmcplugin.SORT_METHOD_UNSORTED,
            common.sp.xbmcplugin.SORT_METHOD_LABEL
        ),
        category=common.get_window_title()
    )


@common.PLUGIN.mem_cached(common.CACHE_TIME)
def list_shows(params):
    return None


@common.PLUGIN.mem_cached(common.CACHE_TIME)
def list_videos(params):
    videos = []

    if params.next == 'list_videos_weather':

        weather_html = utils.get_webcontent(URL_CONTENT % 'weather')
        weather_soup = bs(weather_html, 'html.parser')
        title = weather_soup.find('article', class_='md-mainArticle').find_all('img', class_='lazy')[0].get('alt').encode('utf-8')
        img = weather_soup.find('article', class_='md-mainArticle').find_all('img', class_='lazy')[0].get('data-original')
        duration = 0
        video_url = URL_STREAM % 'weather'

        info = {
            'video': {
                'title': title,
                #'plot': plot,
                #'episode': episode_number,
                #'season': season_number,
                #'rating': note,
                #'aired': aired,
                #'date': date,
                'duration': duration,
                #'year': year,
                'mediatype': 'tvshow'
            }
        }

        download_video = (
            _('Download'),
            'XBMC.RunPlugin(' + common.PLUGIN.get_url(
                action='download_video',
                video_url=video_url) + ')'
        )
        context_menu = []
        context_menu.append(download_video)
        context_menu.append(utils.vpn_context_menu_item())

        videos.append({
            'label': title,
            'thumb': img,
            'fanart': img,
            'url': common.PLUGIN.get_url(
                action='channel_entry',
                next='play_r',
                video_url=video_url
            ),
            'is_playable': True,
            'info': info,
            'context_menu': context_menu
        })

    elif params.next == 'list_videos_news':

        for content in NEWS_CONTENT:

            news_html = utils.get_webcontent(URL_CONTENT % content)
            news_soup = bs(news_html, 'html.parser')
            title = news_soup.find('article', class_='md-mainArticle').find_all('img', class_='lazy')[0].get('alt').encode('utf-8')
            img = URL_ROOT + news_soup.find('article', class_='md-mainArticle').find_all('img', class_='lazy')[0].get('data-original')
            duration = 0
            video_url = URL_STREAM % content

            info = {
                'video': {
                    'title': title,
                    #'plot': plot,
                    #'episode': episode_number,
                    #'season': season_number,
                    #'rating': note,
                    #'aired': aired,
                    #'date': date,
                    'duration': duration,
                    #'year': year,
                    'mediatype': 'tvshow'
                }
            }

            download_video = (
                _('Download'),
                'XBMC.RunPlugin(' + common.PLUGIN.get_url(
                    action='download_video',
                    video_url=video_url) + ')'
            )
            context_menu = []
            context_menu.append(download_video)
            context_menu.append(utils.vpn_context_menu_item())

            videos.append({
                'label': title,
                'thumb': img,
                'fanart': img,
                'url': common.PLUGIN.get_url(
                    action='channel_entry',
                    next='play_r',
                    video_url=video_url
                ),
                'is_playable': True,
                'info': info,
                'context_menu': context_menu
            })

    return common.PLUGIN.create_listing(
        videos,
        sort_methods=(
            common.sp.xbmcplugin.SORT_METHOD_DATE,
            common.sp.xbmcplugin.SORT_METHOD_DURATION,
            common.sp.xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE,
            common.sp.xbmcplugin.SORT_METHOD_GENRE,
            common.sp.xbmcplugin.SORT_METHOD_PLAYCOUNT,
            common.sp.xbmcplugin.SORT_METHOD_UNSORTED
        ),
        content='tvshows',
        category=common.get_window_title()
    )


@common.PLUGIN.mem_cached(common.CACHE_TIME)
def list_live(params):
    return None


@common.PLUGIN.mem_cached(common.CACHE_TIME)
def get_video_url(params):

    if params.next == 'play_r':
        return params.video_url

