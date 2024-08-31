#! /usr/bin/env python3.12
"""
Display the queue and its tags.
"""

from pytumblr2 import Post

from helpers import client, load_mikus, process_tags

for miku in load_mikus():
    artist = miku['artist']
    loc = ', '.join(miku['loc']) if 'loc' in miku else miku['name']
    print(f'   {artist:20} {loc}')

N = 0
for post in client.get_posts("miku-earth", queue=True):
    N += 1
    page = N // 20 + 1

    # print(post)
    post: Post
    
    miku = process_tags(post['tags'])
    miku.setdefault('artist', post['trail'][-1]['blog']['name'])

    url = post['id_string']
    source = miku['source']
    loc = ', '.join(miku['loc']) if 'loc' in miku else miku['name']
    artist = miku['artist']

    print(f'{page:2} {artist:20} {loc}')
