# Fetches static/mikus.json from tumblr.

import json
from pathlib import Path

from pytumblr2 import Post, Client

CACHE_POSTS = Path('.cache/posts.json')
CACHE_ROOTS = Path('.cache/rootposts/')

MIKUS = Path('static/mikus.js')
JS_HEADER = 'const MIKUS = '

MIKUS_SEEN = dict()
if MIKUS.is_file():
    text = MIKUS.read_text().removeprefix(JS_HEADER)
    mikus = json.loads(text)
    MIKUS_SEEN = {miku['id']: miku for miku in mikus}

    # TODO: find the date ID so we don't spam tumblr
    # and can continually fetch!


client = Client.from_keys('.keys', '.cache')
posts = client.get_posts_with_cache('miku-earth')

def dig(obj: dict):
    for k, v in obj.items():
        print(f'{k:30} {type(v).__name__} {v!r}')

mikus = []
for post in posts:
    miku = {}
    post_id = post['id_string']
    miku = MIKUS_SEEN.get(post_id, {})

    tags: list = post['tags']
    if 'meta' in tags:
        continue

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

    dt = Post.get_date(client.get_root_post(post))
    # HACK: this ignores twitter because. not gonna go there tbh.
    srcset = Post.get_first_image(post)
    post_url = post['short_url']

    miku.update({
        'id': post_id,
        'img_min_url': srcset.get(75),
        'img_max_url': srcset.get('max'),
        'artist': artist,
        'artist_url': artist_url,
        'date': str(dt),
        'post_url': post_url,
        'continent': continent,
        'loc': loc,
    })
    mikus.append(miku)

    print(f'{artist:20} {post_url} {dt} {continent:10} {loc}')

print(mikus)
mikus.sort(key=lambda x: x['date'])
MIKUS.write_text(JS_HEADER + json.dumps(mikus, indent=2))