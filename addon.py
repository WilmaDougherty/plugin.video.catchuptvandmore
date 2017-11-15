# -*- coding: utf-8 -*-
"""
    Catch-up TV & More
    Copyright (C) 2016  SylvainCecchetto

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

import imp
import YDStreamUtils
import YDStreamExtractor
from resources.lib import skeleton
from resources.lib import common
from resources.lib import vpn
from resources.lib import utils


# Useful path
LIB_PATH = common.sp.xbmc.translatePath(
    common.sp.os.path.join(
        common.ADDON.path,
        "resources",
        "lib"
    )
)

MEDIA_PATH = (
    common.sp.xbmc.translatePath(
        common.sp.os.path.join(
            common.ADDON.path,
            "resources",
            "media"
        )
    )
)

# Initialize GNU gettext emulation in addon
# This allows to use UI strings from addon’s English
# strings.po file instead of numeric codes
_ = common.ADDON.initialize_gettext()


@common.PLUGIN.action()
def root(params):
    """
    Build the addon main menu
    with all not hidden categories
    """

    print '# Enter in root(params)'

    # If we just launch the addon
    if 'menu_dict' not in params:
        params['menu_dict'] = skeleton.SKELETON
        params['path'] = []
    else:
        params['menu_dict'] = eval(params['menu_dict'])
        params['path'] = eval(params['path'])

    print '# params[menu_dict]: ' + repr(params['menu_dict'])

    # First we sort the current menu
    menu = []
    for item_id in params['menu_dict']:
        # If menu item isn't disable
        # if common.PLUGIN.get_setting(item_id):
        item_order = common.PLUGIN.get_setting(item_id + '.order')
        item_title = skeleton.LABELS[item_id]
        item_folder = skeleton.FOLDERS[item_id]
        item = (item_order, item_id, item_title, item_folder)
        menu.append(item)

    menu = sorted(menu, key=lambda x: x[0])

    listing = []
    last_item_id = ''
    for index, (item_order, item_id, item_title, item_folder) \
            in enumerate(menu):

        if params['path'] is None:
            params['path'] = [item_folder]
        params_path = params['path'].append(item_folder)
        params_menu_dict = params['menu_dict'][item_id]

        # DEBUG
        print '#\t item_id: ' + item_id
        print '#\t item_folder: ' + item_folder
        print '#\t item_title: ' + item_title
        print '#\t params_path: ' + repr(params_path)
        print '#\t params_menu_dict: ' + repr(params_menu_dict)

        last_item_id = item_id
        last_window_title = _(item_title)

        # Build context menu (Move up, move down, ...)
        context_menu = []

        item_down = (
            _('Move down'),
            'XBMC.RunPlugin(' + common.PLUGIN.get_url(
                action='move',
                direction='down',
                item_id_order=item_id + '.order',
                displayed_items=menu) + ')'
        )
        item_up = (
            _('Move up'),
            'XBMC.RunPlugin(' + common.PLUGIN.get_url(
                action='move',
                direction='up',
                item_id_order=item_id + '.order',
                displayed_items=menu) + ')'
        )

        if index == 0:
            context_menu.append(item_down)
        elif index == len(menu) - 1:
            context_menu.append(item_up)
        else:
            context_menu.append(item_up)
            context_menu.append(item_down)

        hide = (
            _('Hide'),
            'XBMC.RunPlugin(' + common.PLUGIN.get_url(
                action='hide',
                item_id=item_id) + ')'
        )
        context_menu.append(hide)

        context_menu.append(utils.vpn_context_menu_item())

        '''
        media_item_path = common.sp.xbmc.translatePath(
            common.sp.os.path.join(
                MEDIA_PATH,
                'categories',
                category_id[-2:]
            )
        )

        media_category_path = media_category_path.decode(
            "utf-8").encode(common.FILESYSTEM_CODING)

        icon = media_category_path + '.png'
        fanart = media_category_path + '_fanart.jpg'
        '''

        listing.append({
            # 'icon': icon,
            # 'fanart': fanart,
            'label': _(item_title),
            'url': common.PLUGIN.get_url(
                action='root',
                item_id=item_id,
                path=repr(params_path),
                menu_dict=repr(params_menu_dict),
                window_title=_(item_title)
            ),
            'context_menu': context_menu
        })

    # If only one category is present, directly open this category
    if len(listing) == 1:
        params['item_id'] = last_item_id
        params['window_title'] = last_window_title
        return root(params)

    return common.PLUGIN.create_listing(
        listing,
        sort_methods=(
            common.sp.xbmcplugin.SORT_METHOD_UNSORTED,),
        category=common.get_window_title()
    )


@common.PLUGIN.action()
def list_channels(params):
    """
    Build the channels list
    of the desired category
    """

    # First, we sort channels by order
    channels_dict = skeleton.CHANNELS[params.category_id]
    channels = []
    for channel_id, title in channels_dict.iteritems():
        # If channel isn't disable
        if common.PLUGIN.get_setting(channel_id):
            channel_order = common.PLUGIN.get_setting(channel_id + '.order')
            channel = (channel_order, channel_id, title)
            channels.append(channel)

    channels = sorted(channels, key=lambda x: x[0])

    # Secondly, we build channels list in Kodi
    listing = []
    for index, (order, channel_id, title) in enumerate(channels):
        # channel_id = channels.fr.6play.w9
        [
            channel_type,  # channels
            channel_category,  # fr
            channel_file,  # 6play
            channel_name  # w9
        ] = channel_id.split('.')

        # channel_module = channels.fr.6play
        channel_module = '.'.join((
            channel_type,
            channel_category,
            channel_file))

        media_channel_path = common.sp.xbmc.translatePath(
            common.sp.os.path.join(
                MEDIA_PATH,
                channel_type,
                channel_category,
                channel_name
            )
        )

        media_channel_path = media_channel_path.decode(
            "utf-8").encode(common.FILESYSTEM_CODING)

        # Build context menu (Move up, move down, ...)
        context_menu = []

        item_down = (
            _('Move down'),
            'XBMC.RunPlugin(' + common.PLUGIN.get_url(
                action='move',
                direction='down',
                item_id_order=channel_id + '.order',
                displayed_items=channels) + ')'
        )
        item_up = (
            _('Move up'),
            'XBMC.RunPlugin(' + common.PLUGIN.get_url(
                action='move',
                direction='up',
                item_id_order=channel_id + '.order',
                displayed_items=channels) + ')'
        )

        if index == 0:
            context_menu.append(item_down)
        elif index == len(channels) - 1:
            context_menu.append(item_up)
        else:
            context_menu.append(item_up)
            context_menu.append(item_down)

        hide = (
            _('Hide'),
            'XBMC.RunPlugin(' + common.PLUGIN.get_url(
                action='hide',
                item_id=channel_id) + ')'
        )
        context_menu.append(hide)

        context_menu.append(utils.vpn_context_menu_item())

        icon = media_channel_path + '.png'
        fanart = media_channel_path + '_fanart.jpg'

        listing.append({
            'icon': icon,
            'fanart': fanart,
            'label': title,
            'url': common.PLUGIN.get_url(
                action='channel_entry',
                next='root',
                channel_name=channel_name,
                channel_module=channel_module,
                channel_id=channel_id,
                channel_category=channel_category,
                window_title=title
            ),
            'context_menu': context_menu
        })

    return common.PLUGIN.create_listing(
        listing,
        sort_methods=(
            common.sp.xbmcplugin.SORT_METHOD_UNSORTED,),
        category=common.get_window_title()
    )


def get_channel_module(params):
    if 'channel_name' in params and \
            'channel_module' in params and \
            'channel_id' in params and \
            'channel_category' in params:
        channel_name = params.channel_name
        channel_module = params.channel_module
        channel_id = params.channel_id
        channel_category = params.channel_category
        storage = common.sp.MemStorage('last_channel')
        storage['last_channel_name'] = channel_name
        storage['last_channel_module'] = channel_module
        storage['last_channel_id'] = channel_id
        storage['last_channel_category'] = channel_category
    else:
        storage = common.sp.MemStorage('last_channel')
        channel_name = storage['last_channel_name']
        channel_module = storage['last_channel_module']
        channel_id = storage['last_channel_id']
        channel_category = storage['last_channel_category']

    params['channel_name'] = channel_name
    params['channel_id'] = channel_id
    params['channel_category'] = channel_category

    channel_path = common.sp.xbmc.translatePath(
        common.sp.os.path.join(
            LIB_PATH,
            *(channel_module.split("."))
        )
    )
    channel_filepath = channel_path + ".py"
    channel_filepath = channel_filepath.decode(
        "utf-8").encode(common.FILESYSTEM_CODING)

    return imp.load_source(
        channel_name,
        channel_filepath
    )


@common.PLUGIN.action()
def channel_entry(params):
    """
    Last plugin action function in addon.py.
    Now we are going into the channel python file.
    The channel file can return folder or not item ; playable or not item
    """
    channel = get_channel_module(params)

    # Let's go to the channel file ...
    return channel.channel_entry(params)


@common.PLUGIN.action()
def move(params):
    if params.direction == 'down':
        offset = + 1
    elif params.direction == 'up':
        offset = - 1

    for k in range(0, len(params.displayed_items)):
        item = eval(params.displayed_items[k])
        item_order = item[0]
        item_id = item[1]
        if item_id + '.order' == params.item_id_order:
            item_swaped = eval(params.displayed_items[k + offset])
            item_swaped_order = item_swaped[0]
            item_swaped_id = item_swaped[1]
            common.PLUGIN.set_setting(
                params.item_id_order,
                item_swaped_order)
            common.PLUGIN.set_setting(
                item_swaped_id + '.order',
                item_order)
            common.sp.xbmc.executebuiltin('XBMC.Container.Refresh()')
            return None


@common.PLUGIN.action()
def hide(params):
    if common.PLUGIN.get_setting('show_hidden_items_information'):
        common.sp.xbmcgui.Dialog().ok(
            _('Information'),
            _('To re-enable hidden items go to the plugin settings'))
        common.PLUGIN.set_setting('show_hidden_items_information', False)

    common.PLUGIN.set_setting(params.item_id, False)
    common.sp.xbmc.executebuiltin('XBMC.Container.Refresh()')
    return None


@common.PLUGIN.action()
def download_video(params):
    #  Ici on a seulement le lien de la page web où se trouve la video
    #  Il faut appeller la fonction get_video_url de la chaine concernée
    #  pour avoir l'URL finale de la vidéo
    channel = get_channel_module(params)
    params.next = 'download_video'
    url_video = channel.get_video_url(params)

    #  Maintenant on peut télécharger la vidéo

    print 'URL_VIDEO to download ' + url_video

    vid = YDStreamExtractor.getVideoInfo(url_video, quality=3)
    path = common.PLUGIN.get_setting('dlFolder')
    path = path.decode(
        "utf-8").encode(common.FILESYSTEM_CODING)

    with YDStreamUtils.DownloadProgress() as prog:
        try:
            YDStreamExtractor.setOutputCallback(prog)
            result = YDStreamExtractor.downloadVideo(vid, path)
            if result:
                # success
                full_path_to_file = result.filepath
            elif result.status != 'canceled':
                # download failed
                error_message = result.message
        finally:
            YDStreamExtractor.setOutputCallback(None)

    return None


@common.PLUGIN.action()
def vpn_entry(params):
    vpn.root(params)
    return None


@common.PLUGIN.action()
def clear_cache():
    utils.clear_cache()
    return None


if __name__ == '__main__':
    common.PLUGIN.run()
