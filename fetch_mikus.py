# Fetches static/mikus.json from tumblr.

from datetime import datetime
import json
from pathlib import Path

from pytumblr2 import Post, Client

CACHE_POSTS = Path('.cache/posts.json')
CACHE_ROOTS = Path('.cache/rootposts/')

MIKUS = Path('static/mikus.js')
JS_HEADER = 'const MIKUS = '

MIKUS_SEEN = dict()

fetch_after = 0
if MIKUS.is_file():
    text = MIKUS.read_text().removeprefix(JS_HEADER)
    mikus = json.loads(text)
    MIKUS_SEEN = {miku['id']: miku for miku in mikus}
    N_ALREADY = len(mikus)

    final_dt = datetime.fromisoformat(mikus[-1]['date'])
    fetch_after = int(final_dt.timestamp())
    print(fetch_after)

# exit()

client = Client.from_keys('.keys', '.cache')
posts = client.get_posts_with_cache('miku-earth', after=fetch_after)

def dig(obj: dict):
    for k, v in obj.items():
        print(f'{k:30} {type(v).__name__} {v!r}')

for post in posts:
    post_id = post['id_string']
    miku = MIKUS_SEEN.get(post_id, {})
    if miku:
        continue

    tags: list = post['tags']

    miku.update({
        'id': post_id,
        'post_url': post['short_url'],
        'meta': 'meta' in tags or 'various' in tags,
        'collated_at': str(Post.get_date(post)),
    })
    mikus.append(miku)
    if miku['meta']:
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

    miku.update({
        'img_min_url': srcset.get(75),
        'img_max_url': srcset.get('max'),
        'artist': artist,
        'artist_url': artist_url,
        'date': str(dt),
        'continent': continent,
        'loc': loc,
    })
    # mikus.append(miku)

    print(f'{artist:20} {dt} {continent:10} {loc}')

N_NEW = len(mikus) - N_ALREADY
print(f'{N_ALREADY} + {N_NEW} new = {len(mikus)} total')
mikus.sort(key=lambda x: x.get('collated_at', ''))
MIKUS.write_text(JS_HEADER + json.dumps(mikus, indent=2))