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
    Build the addon main menus
    with all not hidden categories
    """

    # params.module_path --> Path of the module to load
    # params.skeleton_path --> Path taken by the user in Kodi

    if 'skeleton_path' not in params:
        # We just launch the addon
        params.module_path = 'root'
        params.skeleton_path = 'root'

    current_dict = skeleton.SKELETON
    for key in params.skeleton_path.split('-'):
        current_dict = current_dict[key]

    # First we sort the current menu
    menu = []
    for item_id in current_dict:
        # If menu item isn't disable
        if common.PLUGIN.get_setting(item_id):
            # Get order value in settings file
            item_order = common.PLUGIN.get_setting(item_id + '.order')

            # Get english item title in LABELS dict in skeleton file
            # and check if this title has any translated version
            item_title = ''
            try:
                item_title = common.PLUGIN.get_localized_string(
                    skeleton.LABELS[item_id])
            except TypeError:
                item_title = skeleton.LABELS[item_id]

            # Build step by step the module pathfile
            item_folder = item_id
            if item_id in skeleton.FOLDERS:
                item_folder = skeleton.FOLDERS[item_id]

            # Check the next action to do
            item_next = ''
            if isinstance(current_dict, dict):
                item_next = 'root'
            elif 'live_tv' in params.skeleton_path:
                item_next = 'build_live_tv_menu'
            elif 'replay' in params.skeleton_path:
                item_next = 'replay_entry'
            elif 'website' in params.skeleton_path:
                item_next = 'build_website_menu'
            # This part can be extended if needed ...

            item = (item_order, item_id, item_title, item_folder, item_next)
            menu.append(item)

    menu = sorted(menu, key=lambda x: x[0])

    listing = []
    for index, (item_order, item_id, item_title, item_folder, item_next) \
            in enumerate(menu):

        # Build context menu (Move up, move down, vpn, ...)
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

        # Found icon and fanart images
        media_item_path = common.sp.xbmc.translatePath(
            common.sp.os.path.join(
                MEDIA_PATH,
                *((params.module_path + '-' + item_folder).split('-'))
            )
        )

        icon = media_item_path + '.png'
        fanart = media_item_path + '_fanart.jpg'

        icon = icon.decode(
            "utf-8").encode(common.FILESYSTEM_CODING)

        fanart = fanart.decode(
            "utf-8").encode(common.FILESYSTEM_CODING)

        print "#icon : " + icon
        print "#fanart : " + fanart

        # Append this item to listing
        listing.append({
            'icon': icon,
            'fanart': fanart,
            'label': item_title,
            'url': common.PLUGIN.get_url(
                action=item_next,
                item_id=item_id,
                module_path=params.module_path + '-' + item_folder,
                skeleton_path=params.skeleton_path + '-' + item_id,
                window_title=item_title
            ),
            'context_menu': context_menu
        })

    # If only one category is present, directly open this category
    if len(listing) == 1:
        params['item_id'] = menu[0][1]
        params['module_path'] = menu[0][1] + '-' + menu[0][1]
        params['skeleton_path'] = menu[0][1] + '-' + menu[0][1]
        params['window_title'] = menu[0][1]
        return eval(menu[0][1] + '(params)')

    return common.PLUGIN.create_listing(
        listing,
        sort_methods=(
            common.sp.xbmcplugin.SORT_METHOD_UNSORTED,),
        category=common.get_window_title()
    )


def get_module(params):
    module_path = []
    module_name = ''

    if 'module_path' in params:
        for path_part in params['module_path'].split('-'):
            if '.' in path_part:
                path_part = path_part.split('.')
                module_path.append(path_part[0])
                module_name = path_part[0]
                params['submodule_name'] = path_part[1]
            else:
                module_path.append(path_part)

        storage = common.sp.MemStorage('last_module')
        storage['module_path'] = module_path
        storage['module_name'] = module_name
        storage['submodule_name'] = params['submodule_name']
    else:
        storage = common.sp.MemStorage('last_module')
        module_path = storage['module_path']
        module_name = storage['module_name']
        params['submodule_name'] = storage['submodule_name']

    module_path = common.sp.xbmc.translatePath(
        common.sp.os.path.join(
            LIB_PATH,
            *(module_path)
        )
    )
    module_filepath = module_path + ".py"
    module_filepath = module_filepath.decode(
        "utf-8").encode(common.FILESYSTEM_CODING)

    return imp.load_source(
        module_name,
        module_filepath
    )


@common.PLUGIN.action()
def replay_entry(params):
    module = get_module(params)
    return module.replay_entry(params)


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
