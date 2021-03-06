# -*- coding: utf-8 -*-

'''
#:'######::'####:'##::::'##:'####:'########::::'###:::::'######::
#'##... ##:. ##:: ##:::: ##:. ##::... ##..::::'## ##:::'##... ##:
# ##:::..::: ##:: ##:::: ##:: ##::::: ##:::::'##:. ##:: ##:::..::
# ##:::::::: ##:: ##:::: ##:: ##::::: ##::::'##:::. ##:. ######::
# ##:::::::: ##::. ##:: ##::: ##::::: ##:::: #########::..... ##:
# ##::: ##:: ##:::. ## ##:::: ##::::: ##:::: ##.... ##:'##::: ##:
#. ######::'####:::. ###::::'####:::: ##:::: ##:::: ##:. ######::
#:......:::....:::::...:::::....:::::..:::::..:::::..:::......:::

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import re

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['azmovie.to']
        self.base_link = 'https://azmovie.to'
        self.search_link = '/watch.php?title=%s'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            title = cleantitle.geturl(title).replace('-', '+')
            url = self.base_link + self.search_link % title
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            r = client.request(url)
            u = client.parseDOM(r, "ul", attrs={"id": "serverul"})
            qual = re.compile('span class="quality.+?">(.+?)<').findall(r)
            for i in qual:
                if '1080p' in i:
                    quality = '1080p'
                elif '700p' in i:
                    quality = '720p'
                elif 'HD' in i:
                    quality = '720p'
                else:
                    quality = 'SD'
            for t in u:
                u = client.parseDOM(t, 'a', ret='href')
                for url in u:
                    if 'getlink' in url:
                        continue
                    valid, host = source_utils.is_host_valid(url, hostDict)
                    sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})
                return sources
        except:
            return

    def resolve(self, url):
        return url
