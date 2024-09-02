#! /usr/bin/env python3.12
"""
Post-process, imbuing e.g. descriptions and other useful metadata.
"""

from helpers import load_mikus, save_mikus

mikus = load_mikus()
mikus = [m for m in mikus if not m.get('meta', False)]
for m in mikus:
    m.pop('collated_at', None)
    # m.pop('source', None)
    m.pop('continent', None)

    loc = ''
    if 'loc' in m:
        loc = ', '.join(m['loc'])

    if 'coords' not in m:
        print('coords:', m['id'], loc or m['name'])
        continue
    if 'name' not in m:
        print('name:  ', m['id'], loc)
        continue

    if 'artist_url' not in m:
        artist = m['artist']
        source = m.get('source', None)
        if not source:
            source = 'tumblr'
            print('check if this is tumblr:', m['post_url'])
        m['artist_url'] = f'https://{source}.com/{artist}'

    # coord and name assigned: we can remove loc
    m.pop('loc', None)

save_mikus(mikus)
