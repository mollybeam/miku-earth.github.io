#! /usr/bin/env python3.12
"""
Display the queue and its tags.
"""

from pytumblr2 import Post

from helpers import client, load_mikus, process_tags

for miku in load_mikus():
    if miku.get('meta', False):
        continue
    artist = miku['artist']
    loc = ', '.join(miku['loc']) if 'loc' in miku else miku['name']
    url = miku['post_url']
    print(f'   {artist:30} {loc:30} {url}')

N = 0
for post in client.get_posts("miku-earth", queue=True):
    N += 1
    page = N // 20 + 1

    # print(post)
    post: Post
    
    miku = process_tags(post['tags'])
    blogname = post['trail'][-1]['blog']['name']
    miku.setdefault('artist', blogname)

    url = post['id_string']
    source = miku['source']
    loc = ', '.join(miku['loc']) if 'loc' in miku else miku['name']
    artist = miku['artist']

    post_id = post['trail'][-1]['post']['id']
    url = f'https://tumblr.com/{blogname}/{post_id}'

    print(f'{page:2} {artist:30} {loc:30} {url}')
