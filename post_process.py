"""
Post-processing, imbuing e.g. descriptions and other useful metadata.
"""

from helpers import load_mikus, save_mikus

mikus = load_mikus()
for m in mikus:
    del m['collated_at']

    if m['meta']:
        continue

    loc = ''
    if 'loc' in m:
        loc = ', '.join(m['loc'])

    if 'coords' not in m:
        print('coords needed:', m['id'], loc)
        continue
    if 'name' not in m:
        print('name   needed:', m['id'], loc)
        continue

    # coord and name assigned: we can remove loc
    m.pop('loc', None)

save_mikus(mikus)
