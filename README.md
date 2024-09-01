[![banner image](https://miku.earth/static/banner.png)](https://miku.earth)

# [miku.earth](https://miku.earth)

A showcase of the world's cultural clothing, as portrayed by local artists.

## Todo

- [ ] Bug: showcase/hovered mikus not coming to forefront
- [ ] Bug: `get(showcase_i)` errors
- [ ] Investigate Chrome
- [ ] Find or set up a nicer map provider

## Under the hood

Pulls posts from [@miku-earth on tumblr](https://miku-earth.tumblr.com) using `pytumblr2`, a version of `pytumblr` I really should go upload at some point in time. Stores in one big JSON file, using a handful of tools to fetch, post-process and otherwise help me do my thang.

Post tags are essential -- they help me to hand-tag each with a `name`, `coords` and optionally `wikipedia` link (if it differs from `name`). An older tagging system gave me mild RSI while storing redundant info, so a newer system typically means I only need to provide one tag. Sadly this means I can't provide commentary in the tags :(

`maplibregl` handles rendering.
In the past a MapTiler custom style was lovingly handcrafted to de-emphasise world borders and show a natural Earth, allowing the artwork to take prominence in showing local cultures.
Sadly it turns out it would be a tad bit expensive; after using $32 of credit for one day of mapping I bit the bullet and switched to OpenStreetMap, which has world borders and is less fancy, but is lovingly free forever, which I appreciate. I might experiment later with emulating the old style, but given the cost it's kinda out of my hands.