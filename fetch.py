# Fetches static/mikus.json from tumblr.

from datetime import datetime
import json
from pathlib import Path

from pytumblr2 import Post, get_srcset
from helpers import client, load_mikus, save_mikus

MIKUS_SEEN = dict()

fetch_after = 0
if mikus := load_mikus():
    MIKUS_SEEN = {miku['id']: miku for miku in mikus}
    N_ALREADY = len(mikus)

    final_dt = datetime.fromisoformat([m['date'] for m in mikus if 'date' in m][-1])
    fetch_after = int(final_dt.timestamp())
    print("fetching after", final_dt)

# fetch
posts = client.get_posts_with_cache('miku-earth', after=fetch_after)

for post in posts:
    post_id = post['id_string']
    if miku := MIKUS_SEEN.get(post_id, {}):
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

    srcset_raw = Post.get_first_image(post)
    srcset = get_srcset(srcset_raw)

    miku.update({
        'thumb': srcset.get(75),
        'srcset': srcset_raw,
        'artist': artist,
        'artist_url': artist_url,
        'date': str(dt),
        'continent': continent,
        'loc': loc,
    })

    print(f'{artist:20} {dt} {continent:10} {loc}')

N_NEW = len(mikus) - N_ALREADY
print(f'{N_ALREADY} + {N_NEW} new = {len(mikus)} total')
save_mikus(mikus)