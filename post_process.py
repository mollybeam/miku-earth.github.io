"""
Post-processing, imbuing e.g. descriptions and other useful metadata.
"""

from helpers import load_mikus, save_mikus

mikus = load_mikus()
mikus = [m for m in mikus if not m.get('meta', False)]
for m in mikus:
    if m.get('meta', None) is False:
        m.pop('meta')

    m.pop('collated_at', None)
    m.pop('source', None)
    m.pop('continent', None)

    loc = ''
    if 'loc' in m:
        loc = ', '.join(m['loc'])

    if 'coords' not in m:
        print('coords needed:', m['id'], loc or m['name'])
        continue
    if 'name' not in m:
        print('name   needed:', m['id'], loc)
        continue

    # coord and name assigned: we can remove loc
    m.pop('loc', None)

save_mikus(mikus)
