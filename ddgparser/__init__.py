#!/usr/bin/python3

#
# A DuckDuckGo parser.
# Copyright (C) 2020 Alice Wonderland
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from lxml import html
import requests
from urllib.parse import unquote


'''
DuckDuckGo parser

@author:    Alice Wonderland
@license:   GPL-v3-0-or-later
'''

# q - query
# kl - language e.g. en-us
SEARCH_URL = 'https://html.duckduckgo.com/html/?q={q}&kl={kl}'

HEADERS = {
    'User-Agent': 'Opera/5.11 (Windows 98; U)  [en]'
}

def search(q: str, kl: str = 'en-us'):
    '''
    Search.

    Returned dict example:
    {
        'request': requests.Request,
        'q': str,
        'kl': str,
        'instant': {
            'title': str,
            'desc': str,
            'url': str
        },
        'results': [
            {
                'title': str,
                'desc': str,
                'url': str
            },
            ...
        ]
    }

    :return dict
    '''

    # Make a request
    r = requests.get(SEARCH_URL.format(
        q=q,
        kl=kl
    ), headers=HEADERS)

    if r.status_code != 200:
        raise requests.exceptions.HTTPError(
            'Unexpected status code: {}'.format(r.status_code)
        )

    # Parse HTML
    # FIX: text() can't work with <b> elements
    html_text = r.text.replace('<b>', '')
    html_text = html_text.replace('</b>', '')

    tree = html.fromstring(html_text)

    # with open(f'{q}.html', 'w') as f:
    #     f.write(html_text)

    # Instant Answer
    try:
        ia_html = tree.xpath('//div[@class="zci"]')[0]

        instant = {
            'title': ia_html.xpath('.//h1/a/text()')[0],
            'desc': ia_html.xpath('.//div/text()')[0].strip(),
            'url': ia_html.xpath('.//h1/a/@href')[0]
        }
    except IndexError:
        instant = {}  # Instant Answer is not available

    # Results
    results = []
    results_html = tree.xpath('//div[@id="links"]/div/div')

    try:
        for i in results_html:
            title = i.xpath('.//h2/a/text()')[0]

            desc = i.xpath('.//a[@class="result__snippet"]/text()')[0]

            url = i.xpath('.//a/@href')[0]
            url = url[url.find('?uddg=')+6:]  # Delete redirect links
            url = unquote(url)  # Decode the cleaned URL

            results.append({
                'title': title.strip(),
                'desc': desc.strip(),
                'url': url.strip()
            })
    except IndexError:
        results = []  # Nothing was found

    # Return a dict
    return {
        'request': r,
        'q': q,
        'kl': kl,
        'instant': instant,
        'results': results
    }
