"""
Display the queue and its tags.
"""

from pytumblr2 import Post

from helpers import client, process_tags

N = 1

for post in client.get_posts("miku-earth", queue=True):
    N += 1
    page = N // 20

    # print(post)
    post: Post

    miku = process_tags(post['tags'])

    url = post['id_string']
    source = miku['source']
    loc = ', '.join(miku['loc']) if 'loc' in miku else miku['name']

    print(f'{page:2} {loc}')
