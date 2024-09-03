[![banner image](https://miku.earth/static/banner.png)](https://miku.earth)

# [miku.earth](https://miku.earth)

A showcase of the world's cultural clothing, as portrayed by local artists.

## Todo

- [ ] Bug: showcase/hovered mikus not coming to forefront
- [ ] Bug: `get(showcase_i)` errors
- [ ] Investigate Chrome
- [ ] Find or set up a nicer map provider

## Under the hood

### Post collation

Pulls posts from [@miku-earth on tumblr](https://miku-earth.tumblr.com) using `pytumblr2`, a version of `pytumblr` I really should go upload at some point in time. Stores in one big JSON file, using a handful of tools to fetch, post-process and otherwise help me do my thang.

Due to the tagging system I use with `pytumblr2` I can't provide commentary ;-;

Inside `mikus.json` each post has the tags, typically strings:
- `id`: Tumblr post ID (avoid duplicates)
- `post_url`: URL to link to on image
- `artist`: Artist username
- `artist_url`: Artist URL
- `name`: Name of artwork
- `wikipedia`: Wikipedia article to link to on artwork name (if not present, `name` is used instead)
- `country`: [ISO 3166-1 alpha-2 country code](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2)
- `thumb`: The thumbnail to use for the map marker.
- `srcset`: The `<img>` srcset to use if the image should be loaded larger. Presently unused.
- `coords` ([number, number]): The longitude and latitude of the marker.
- `shiny` (bool): If true, this is a small easter egg post; on the map it is rendered golden and smaller.
- `meta` (bool): If true, skip this post; it is not an artwork.
- `tags` (optional list of strings): Tags for collation.

### Mapping

`maplibregl` handles rendering.
In the past a MapTiler custom style was lovingly handcrafted to de-emphasise world borders and show a natural Earth, allowing the artwork to take prominence in showing local cultures.
Sadly it turns out it would be a tad bit expensive; after using $32 of credit for one day of mapping I bit the bullet and switched to OpenStreetMap, which has world borders and is less fancy, but is lovingly free forever, which I appreciate. I might experiment later with emulating the old style, but given the cost it's kinda out of my hands.