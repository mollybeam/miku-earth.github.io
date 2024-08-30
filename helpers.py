from typing import TypedDict

import json
from pathlib import Path

from pytumblr2 import Client

client = Client.from_keys('.keys', '.cache')

class Miku(TypedDict):
    id: str
    collated_at: str  # timestamp
    post_url: str  # short url

    meta: bool

    # if not meta:
    date: str
    thumb: str  # url
    srcset: str
    artist: str
    artist_url: str
    continent: str
    loc: list[str]

    historical: bool

    # hand-tagged
    name: str
    wikipedia: str


MIKUS = Path('static/mikus.js')
JS_HEADER = 'const MIKUS = '
def load_mikus() -> list[Miku]:
    if MIKUS.is_file():
        return json.loads(MIKUS.read_text().removeprefix(JS_HEADER))
    return []

def save_mikus(mikus: list[Miku], sort_key: str = 'collated_at'):
    if sort_key:
        mikus.sort(key=lambda x: x.get(sort_key, ''))
    MIKUS.write_text(JS_HEADER + json.dumps(mikus, indent=2))

# useful analysis:
def dig(obj: dict):
    for k, v in obj.items():
        print(f'{k:30} {type(v).__name__} {v!r}')