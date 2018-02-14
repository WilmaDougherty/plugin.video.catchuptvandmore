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


# https://countrycode.org for ISO coutry code


# FOLDERS dict corresponds to the folder to use to load python files
FOLDERS = {
    'websites': 'websites',
    'live_tv': 'channels',
    'replay': 'channels',
    'be': 'be',
    'fr': 'fr',
    'jp': 'jp',
    'ch': 'ch',
    'gb': 'gb',
    'wo': 'wo'
}


# LABELS dict is only used to retrieve string to display on Kodi
LABELS = {

    # root
    'live_tv': 'Live TV',
    'replay': 'Catch-up TV',
    'websites': 'Websites',

    # Countries
    'be': 'Belgium',
    'fr': 'France',
    'jp': 'Japan',
    'ch': 'Switzerland',
    'gb': 'United Kingdom',
    'wo': 'International',

    # Belgium channels / live TV
    'rtbf.auvio': 'RTBF Auvio (La Une, La deux, La Trois, ...)',
    'bvn.bvn': 'BVN',
    'brf.brf': 'BRF Mediathek',
    'rtl.rtltvi': 'RTL-TVI',
    'rtl.plugrtl': 'PLUG RTL',
    'rtl.clubrtl': 'CLUB RTL',

    # French channels / live TV
    'tf1.tf1': 'TF1',
    'pluzz.france2': 'France 2',
    'pluzz.france3': 'France 3',
    'groupecanal.cplus': 'Canal +',
    'pluzz.france5': 'France 5',
    '6play.m6': 'M6',
    'groupecanal.c8': 'C8',
    '6play.w9': 'W9',
    'tf1.tmc': 'TMC',
    'tf1.nt1': 'NT1',
    'nrj.nrj12': 'NRJ 12',
    'pluzz.france4': 'France 4',
    'bfmtv.bfmtv': 'BFM TV',
    'groupecanal.cnews': 'CNews',
    'groupecanal.cstar': 'CStar',
    'gulli.gulli': 'Gulli',
    'pluzz.franceo': 'France Ô',
    'tf1.hd1': 'HD1',
    'lequipe.lequipe': 'L\'Équipe',
    '6play.6ter': '6ter',
    'numero23.numero23': 'Numéro 23',
    'nrj.cherie25': 'Chérie 25',
    'pluzz.la_1ere': 'La 1ère (Outre-Mer)',
    'pluzz.franceinfo': 'France Info',
    'bfmtv.bfmbusiness': 'BFM Business',
    'bfmtv.rmc': 'RMC',
    'bfmtv.01net': '01Net TV',
    'tf1.tfou': 'Tfou (MYTF1)',
    'tf1.xtra': 'Xtra (MYTF1)',
    'tf1.lci': 'LCI',
    'lcp.lcp': 'LCP Assemblée Nationale',
    'bfmtv.rmcdecouverte': 'RMC Découverte HD24',
    '6play.stories': 'Stories (6play)',
    '6play.bruce': 'Bruce (6play)',
    '6play.crazy_kitchen': 'Crazy Kitchen (6play)',
    '6play.home': 'Home Time (6play)',
    '6play.styles': 'Sixième Style (6play)',
    '6play.comedy': 'Comic (6play)',
    'publicsenat.publicsenat': 'Public Sénat',
    'pluzz.france3regions': 'France 3 Régions',
    'pluzz.francetvsport': 'France TV Sport (francetv)',

    # Japan channels / live TV
    'nhk.nhknews': 'NHK ニュース',
    'nhk.nhklifestyle': 'NHKらいふ',
    'tbs.tbsnews': 'TBS ニュース',

    # Switzerland channels / live TV
    'srgssr.rts': 'RTS',
    'srgssr.rsi': 'RSI',
    'srgssr.srf': 'SRF',
    'srgssr.rtr': 'RTR',
    'srgssr.swissinfo': 'SWISSINFO',

    # United Kingdom channels / live TV
    'blaze.blaze': 'Blaze',
    'uktvplay.dave': 'Dave',
    'uktvplay.really': 'Really',
    'uktvplay.yesterday': 'Yesterday',
    'uktvplay.drama': 'Drama',

    # International channels / live TV
    'tv5monde.tv5mondeafrique': 'TV5Monde Afrique',
    'arte.arte': 'Arte',
    'euronews.euronews': 'Euronews',
    'france24.france24': 'France 24',
    'nhkworld.nhkworld': 'NHK World',
    'tv5monde.tv5monde': 'TV5Monde',
    'tv5monde.tivi5monde': 'Tivi 5Monde',

    # Websites
    'allocine': 'Allociné',
    'tetesaclaques': 'Au pays des Têtes à claques',
    'taratata': 'Taratata',
    'noob': 'Noob TV',
    'culturepub': 'Culturepub'


}


# SKELETON dictionary corresponds to the different level of menus of the addon
SKELETON = {
    ('root', 'root'): {

        ('live_tv', 'root'): {

            ('be', 'build_live_tv_menu'): {
                'rtbf.auvio',
                'bvn.bvn',
                'brf.brf',
                'rtl.rtltvi',
                'rtl.plugrtl',
                'rtl.clubrtl'
            },

            ('fr', 'build_live_tv_menu'): {
                'tf1.tf1',
                'pluzz.france2',
                'pluzz.france3',
                'groupecanal.cplus',
                'pluzz.france5',
                'groupecanal.c8',
                'tf1.tmc',
                'tf1.nt1',
                'nrj.nrj12',
                'pluzz.france4',
                'bfmtv.bfmtv',
                'groupecanal.cnews',
                'groupecanal.cstar',
                'gulli.gulli',
                'pluzz.franceo',
                'tf1.hd1',
                'lequipe.lequipe',
                'numero23.numero23',
                'nrj.cherie25',
                'pluzz.la_1ere',
                'pluzz.franceinfo',
                'bfmtv.bfmbusiness',
                'bfmtv.rmc',
                'tf1.lci',
                'lcp.lcp',
                'bfmtv.rmcdecouverte',
                'publicsenat.publicsenat',
                'pluzz.france3regions',
                'pluzz.francetvsport'
            },

            ('jp', 'build_live_tv_menu'): {
                'nhk.nhknews',
                'nhk.nhklifestyle',
                'tbs.tbsnews'
            },

            ('ch', 'build_live_tv_menu'): {
                'srgssr.rts',
                'srgssr.rsi',
                'srgssr.srf',
                'srgssr.rtr',
                'srgssr.swissinfo'
            },

            ('gb', 'build_live_tv_menu'): {
                'blaze.blaze',
                'uktvplay.dave',
                'uktvplay.really',
                'uktvplay.yesterday',
                'uktvplay.drama'
            },

            ('wo', 'build_live_tv_menu'): {
                'tv5monde.tv5mondeafrique',
                'arte.arte',
                'euronews.euronews',
                'france24.france24',
                'nhkworld.nhkworld',
                'tv5monde.tv5monde',
                'tv5monde.tivi5monde'
            }

        },

        ('replay', 'root'): {

            ('be', 'root'): {
                ('rtbf.auvio', 'replay_entry'),
                ('bvn.bvn', 'replay_entry'),
                ('brf.brf', 'replay_entry'),
                ('rtl.rtltvi', 'replay_entry'),
                ('rtl.plugrtl', 'replay_entry'),
                ('rtl.clubrtl' 'replay_entry')
            },

            ('fr', 'root'): {
                ('tf1.tf1', 'replay_entry'),
                ('pluzz.france2', 'replay_entry'),
                ('pluzz.france3', 'replay_entry'),
                ('groupecanal.cplus', 'replay_entry'),
                ('pluzz.france5', 'replay_entry'),
                ('6play.m6', 'replay_entry'),
                ('groupecanal.c8', 'replay_entry'),
                ('6play.w9', 'replay_entry'),
                ('tf1.tmc', 'replay_entry'),
                ('tf1.nt1', 'replay_entry'),
                ('nrj.nrj12', 'replay_entry'),
                ('pluzz.france4', 'replay_entry'),
                ('bfmtv.bfmtv', 'replay_entry'),
                ('groupecanal.cnews', 'replay_entry'),
                ('groupecanal.cstar', 'replay_entry'),
                ('gulli.gulli', 'replay_entry'),
                ('pluzz.franceo', 'replay_entry'),
                ('tf1.hd1', 'replay_entry'),
                ('lequipe.lequipe', 'replay_entry'),
                ('6play.6ter', 'replay_entry'),
                ('numero23.numero23', 'replay_entry'),
                ('nrj.cherie25', 'replay_entry'),
                ('pluzz.la_1ere', 'replay_entry'),
                ('pluzz.franceinfo', 'replay_entry'),
                ('bfmtv.bfmbusiness', 'replay_entry'),
                ('bfmtv.rmc', 'replay_entry'),
                ('bfmtv.01net', 'replay_entry'),
                ('tf1.tfou', 'replay_entry'),
                ('tf1.xtra', 'replay_entry'),
                ('tf1.lci', 'replay_entry'),
                ('lcp.lcp', 'replay_entry'),
                ('bfmtv.rmcdecouverte', 'replay_entry'),
                ('6play.stories', 'replay_entry'),
                ('6play.bruce', 'replay_entry'),
                ('6play.crazy_kitchen', 'replay_entry'),
                ('6play.home', 'replay_entry'),
                ('6play.styles', 'replay_entry'),
                ('6play.comedy', 'replay_entry'),
                ('publicsenat.publicsenat', 'replay_entry'),
                ('pluzz.france3regions', 'replay_entry'),
                ('pluzz.francetvsport' 'replay_entry')
            },

            ('jp', 'root'): {
                ('nhk.nhknews', 'replay_entry'),
                ('nhk.nhklifestyle', 'replay_entry'),
                ('tbs.tbsnews' 'replay_entry')
            },

            ('ch', 'root'): {
                ('srgssr.rts', 'replay_entry'),
                ('srgssr.rsi', 'replay_entry'),
                ('srgssr.srf', 'replay_entry'),
                ('srgssr.rtr', 'replay_entry'),
                ('srgssr.swissinfo' 'replay_entry')
            },

            ('gb', 'root'): {
                ('blaze.blaze', 'replay_entry'),
                ('uktvplay.dave', 'replay_entry'),
                ('uktvplay.really', 'replay_entry'),
                ('uktvplay.yesterday', 'replay_entry'),
                ('uktvplay.drama' 'replay_entry')
            },

            ('wo', 'root'): {
                ('tv5monde.tv5mondeafrique', 'replay_entry'),
                ('arte.arte', 'replay_entry'),
                ('euronews.euronews', 'replay_entry'),
                ('france24.france24', 'replay_entry'),
                ('nhkworld.nhkworld', 'replay_entry'),
                ('tv5monde.tv5monde', 'replay_entry'),
                ('tv5monde.tivi5monde' 'replay_entry')
            }

        },

        ('websites', 'root'): {
            ('allocine', 'website_entry'),
            ('tetesaclaques', 'website_entry'),
            ('taratata', 'website_entry'),
            ('noob', 'website_entry'),
            ('culturepub', 'website_entry')
        }
    }
}

