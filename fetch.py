#! /usr/bin/env python3.12
"""
Fetch published mikus and post them.
"""

from datetime import datetime

from pytumblr2 import Post, get_srcset
from helpers import client, load_mikus, process_tags, save_mikus

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
    })

    mikus.append(miku)
    if miku['meta']:
        continue

    miku.setdefault('artist', post['trail'][-1]['blog']['name'])
    dt = Post.get_date(client.get_root_post(post))
    miku.update(process_tags(post['tags']))

    artist = miku['artist']
    source = miku['source']
    artist_url = f'https://{source}.com/{artist}'

    TUMBLR_MEDIA = 'https://64.media.tumblr.com/'
    srcset_raw = Post.get_first_image(post)
    srcset = get_srcset(srcset_raw)

    if not srcset:
        mikus.remove(miku)
        print('error!', miku['id'], miku['post_url'])
        continue

    thumb = srcset.get(75).replace(TUMBLR_MEDIA, '')
    srcset_raw = srcset_raw.replace(srcset.get(75) + ' 75w, ', '').replace(TUMBLR_MEDIA, '')

    miku.update({
        'thumb': thumb,
        'srcset': srcset_raw,
        'date': str(dt),
    })

    print(f"{miku['artist']:20} {dt} {miku.get('loc', miku.get('name'))}")

N_NEW = len(mikus) - N_ALREADY
print(f'{N_ALREADY} + {N_NEW} new = {len(mikus)} total')
save_mikus(mikus)
