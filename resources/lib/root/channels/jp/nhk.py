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

import ast
import base64
import json
import time
import re
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup as bs
from resources.lib import utils
from resources.lib import common

# Initialize GNU gettext emulation in addon
# This allows to use UI strings from addon’s English
# strings.po file instead of numeric codes
_ = common.ADDON.initialize_gettext()

context_menu = []
context_menu.append(utils.vpn_context_menu_item())

URL_ROOT = 'http://www3.nhk.or.jp/'

URL_ROOT_2 = 'http://www.nhk.or.jp'

URL_WEATHER_NHK_NEWS = 'https://www3.nhk.or.jp/news/weather/weather_movie.json'

URL_NEWS_NHK_NEWS = 'http://www3.nhk.or.jp/news/json16/newmovie_%s.json'
# Page

URL_STREAM_NEWS = 'https://www3.nhk.or.jp/news/html/%s/movie/%s.json'
# Date, IdVideo

URL_NHK_LIFESTYLE = 'http://www.nhk.or.jp/lifestyle/'

URL_API_KEY_LIFE_STYLE = 'http://movie-s.nhk.or.jp/player.php?v=%s&wmode=transparen&r=true'
# VideoId

URL_STREAM_NHK_LIFE_STYLE = 'http://movie-s.nhk.or.jp/ws/ws_program/api/%s/apiv/5/mode/json?v=%s'
# Api_Key, VideoId


def module_entry(params):
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
    return None


CORRECT_MONTH = {
    'Jan': '01',
    'Feb': '02',
    'Mar': '03',
    'Apr': '04',
    'May': '05',
    'Jun': '06',
    'Jul': '07',
    'Aug': '08',
    'Sep': '09',
    'Oct': '10',
    'Nov': '11',
    'Dec': '12'
}


@common.PLUGIN.mem_cached(common.CACHE_TIME)
def root(params):
    modes = []

    if params.submodule_name == 'nhknews':

        # Add News
        modes.append({
            'label': 'ニュース',
            'url': common.PLUGIN.get_url(
                action='module_entry',
                next='list_videos_news',
                page='1',
                category='NHK ニュース',
                window_title='NHK ニュース'
            ),
            'context_menu': context_menu
        })

        # Add Weather
        modes.append({
            'label': '気象',
            'url': common.PLUGIN.get_url(
                action='module_entry',
                next='list_videos_weather',
                category='NHK ニュース - 気象',
                window_title='NHK ニュース - 気象'
            ),
            'context_menu': context_menu
        })

    elif params.submodule_name == 'nhklifestyle':

        # Build Menu
        list_categories_html = utils.get_webcontent(URL_NHK_LIFESTYLE)
        list_categories_soup = bs(list_categories_html, 'html.parser')
        list_categories = list_categories_soup.find_all(
            'a', class_="header__menu__head")

        for category in list_categories:
            if '#' not in category.get('href'):
                category_title = category.get_text().encode('utf-8')
                category_url = URL_NHK_LIFESTYLE + category.get('href')

                modes.append({
                    'label': category_title,
                    'url': common.PLUGIN.get_url(
                        action='module_entry',
                        next='list_videos_lifestyle',
                        title=category_title,
                        category_url=category_url,
                        window_title=category_title
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
    if 'previous_listing' in params:
        videos = ast.literal_eval(params['previous_listing'])

    if params.next == 'list_videos_weather':

        file_path = utils.download_catalog(
            URL_WEATHER_NHK_NEWS,
            '%s_weather.json' % (params.submodule_name)
        )
        file_weather = open(file_path).read()
        json_parser = json.loads(file_weather)

        title = json_parser["va"]["adobe"]["vodContentsID"]["VInfo1"]
        img = URL_ROOT + json_parser["mediaResource"]["posterframe"]
        duration = 0
        video_url = json_parser["mediaResource"]["url"]

        info = {
            'video': {
                'title': title,
                # 'plot': plot,
                # 'episode': episode_number,
                # 'season': season_number,
                # 'rating': note,
                # 'aired': aired,
                # 'date': date,
                'duration': duration,
                # 'year': year,
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
                action='module_entry',
                next='play_weather_r',
                video_url=video_url
            ),
            'is_playable': True,
            'info': info,
            'context_menu': context_menu
        })

    elif params.next == 'list_videos_news':

        # Build URL :
        url = ''
        if int(params.page) < 10:
            url = URL_NEWS_NHK_NEWS % ('00' + params.page)
        elif int(params.page) >= 10 and int(params.page) < 100:
            url = URL_NEWS_NHK_NEWS % ('0' + params.page)
        else:
            url = URL_NEWS_NHK_NEWS % params.page
        file_path = utils.download_catalog(
            url,
            '%s_news_%s.json' % (params.submodule_name, params.page)
        )
        file_news = open(file_path).read()
        json_parser = json.loads(file_news)

        for video in json_parser["channel"]["item"]:
            title = video["title"]
            img = URL_ROOT + 'news/' + video["imgPath"]
            duration = int(video["videoDuration"])
            video_id = video["videoPath"].replace('.mp4', '')
            pub_date_list = video["pubDate"].split(' ')

            if len(pub_date_list[1]) == 1:
                day = '0' + pub_date_list[0]
            else:
                day = pub_date_list[1]
            try:
                mounth = CORRECT_MONTH[pub_date_list[2]]
            except Exception:
                mounth = '00'
            year = pub_date_list[3]

            date = '.'.join((day, mounth, year))
            aired = '-'.join((year, mounth, day))

            video_date = ''.join((year, mounth, day))

            info = {
                'video': {
                    'title': title,
                    # 'plot': plot,
                    # 'episode': episode_number,
                    # 'season': season_number,
                    # 'rating': note,
                    'aired': aired,
                    'date': date,
                    'duration': duration,
                    'year': year,
                    'mediatype': 'tvshow'
                }
            }

            download_video = (
                _('Download'),
                'XBMC.RunPlugin(' + common.PLUGIN.get_url(
                    action='download_video',
                    video_id=video_id,
                    video_date=video_date) + ')'
            )
            context_menu = []
            context_menu.append(download_video)
            context_menu.append(utils.vpn_context_menu_item())

            videos.append({
                'label': title,
                'thumb': img,
                'fanart': img,
                'url': common.PLUGIN.get_url(
                    action='module_entry',
                    next='play_news_r',
                    video_id=video_id,
                    video_date=video_date
                ),
                'is_playable': True,
                'info': info,
                'context_menu': context_menu
            })

        # More videos...
        videos.append({
            'label': '# ' + common.ADDON.get_localized_string(30100),
            'url': common.PLUGIN.get_url(
                action='module_entry',
                next='list_videos_news',
                page=str(int(params.page) + 1),
                update_listing=True,
                previous_listing=str(videos)
            ),
            'context_menu': context_menu
        })

    elif params.next == 'list_videos_lifestyle':

        replay_episodes_html = utils.get_webcontent(params.category_url)
        replay_episodes_soup = bs(replay_episodes_html, 'html.parser')
        episodes_html = replay_episodes_soup.find('article')
        episodes_html = episodes_html.find_all(
            'script')[0].get_text().encode('utf-8')
        replay_episodes_json = episodes_html.replace(']', '')
        replay_episodes_json = replay_episodes_json.replace(
            'var NHKLIFE_LISTDATA = [', '')
        replay_episodes_json = replay_episodes_json.strip()
        replay_episodes_json = replay_episodes_json.replace('{', '{"')
        replay_episodes_json = replay_episodes_json.replace(': ', '": ')
        replay_episodes_json = replay_episodes_json.replace(',', ',"')
        replay_episodes_json = replay_episodes_json.replace(',"{', ',{')
        json_parser = json.loads('[' + replay_episodes_json + ']')

        for video in json_parser:
            if 'video' in video["href"]:
                title = video["title"]
                plot = video["desc"]
                img = URL_ROOT_2 + video["image_src"]
                duration = 60 * int(video["videoInfo"]["duration"].split(':')[0]) + \
                    int(video["videoInfo"]["duration"].split(':')[1])
                video_url = URL_NHK_LIFESTYLE + \
                    video["href"].replace('../', '')

                # published_date: "2017年10月10日"
                # year = video["published_date"].encode('utf-8').split('年')[0]
                # mounth = video["published_date"].encode('utf-8').split('年')[1].split['月'][0]
                # day = video["published_date"].encode('utf-8').split('月')[1].split['日'][0]

                # date = '.'.join((day, mounth, year))
                # aired = '-'.join((year, mounth, day))

                info = {
                    'video': {
                        'title': title,
                        'plot': plot,
                        # 'episode': episode_number,
                        # 'season': season_number,
                        # 'rating': note,
                        # 'aired': aired,
                        # 'date': date,
                        'duration': duration,
                        # 'year': year,
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
                        action='module_entry',
                        next='play_lifestyle_r',
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
        update_listing='update_listing' in params,
        category=common.get_window_title()
    )


@common.PLUGIN.mem_cached(common.CACHE_TIME)
def list_live(params):
    return None


@common.PLUGIN.mem_cached(common.CACHE_TIME)
def get_video_url(params):

    if params.next == 'play_weather_r':
        return params.video_url
    elif params.next == 'play_news_r':
        url = ''
        file_path = utils.download_catalog(
            URL_STREAM_NEWS % (params.video_date, params.video_id),
            '%s_%s.json' % (params.submodule_name, params.video_id)
        )
        video_vod = open(file_path).read()
        json_parser = json.loads(video_vod)
        return json_parser["mediaResource"]["url"]
    elif params.next == 'play_lifestyle_r':
        video_id_html = utils.get_webcontent(params.video_url)
        video_id = re.compile('player.php\?v=(.*?)&').findall(video_id_html)[0]
        api_key_html = utils.get_webcontent(URL_API_KEY_LIFE_STYLE % video_id)
        api_key = re.compile(
            'data-de-api-key="(.*?)"').findall(api_key_html)[0]
        url_stream = URL_STREAM_NHK_LIFE_STYLE % (api_key, video_id)
        url_stream_json = utils.get_webcontent(url_stream)
        json_parser_stream = json.loads(url_stream_json)
        return json_parser_stream["response"]["WsProgramResponse"]["program"]["asset"]["ipadM3u8Url"]
