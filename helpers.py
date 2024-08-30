from typing import Literal, TypedDict

import json
from pathlib import Path

from pytumblr2 import Client

client = Client.from_keys('.keys', '.cache')

class Miku(TypedDict):
    id: str
    post_url: str  # short url

    meta: bool

    # if not meta:
    source: Literal['tumblr', 'twitter']
    artist_url: str

    date: str
    thumb: str  # url
    srcset: str
    artist: str

    continent: str
    loc: list[str]

    historical: bool

    # hand-tagged
    name: str
    wikipedia: str


def process_tags(tags: list[str]) -> Miku:
    "extract partial info from tags"

    source = 'tumblr'
    match tags.pop():
        case '(from twitter)':
            source = 'twitter'
        case not_a_source:
            tags.append(not_a_source)

    continent, *loc, artist = tags
    match source:
        case 'tumblr':
            artist_url = f'https://tumblr.com/{artist}'
        case 'twitter':
            artist_url = f'https://twitter.com/{artist}'

    return {
        'source': source,
        'artist': artist,
        'artist_url': artist_url,
        'continent': continent,
        'loc': loc,
    }

MIKUS = Path('static/mikus.js')
JS_HEADER = 'const MIKUS = '
def load_mikus() -> list[Miku]:
    if MIKUS.is_file():
        return json.loads(MIKUS.read_text().removeprefix(JS_HEADER))
    return []

def save_mikus(mikus: list[Miku], sort_key: str = 'date'):
    if sort_key:
        mikus.sort(key=lambda x: x.get(sort_key, ''))
    MIKUS.write_text(JS_HEADER + json.dumps(mikus, indent=2))

# useful analysis:
def dig(obj: dict):
    for k, v in obj.items():
        print(f'{k:30} {type(v).__name__} {v!r}')