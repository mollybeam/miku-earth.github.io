[![banner image](https://miku.earth/static/banner.png)](https://miku.earth)

# [miku.earth](https://miku.earth)

<a href="https://www.maptiler.com">
<img src="static/maptiler.png" alt="MapTiler logo" width="100"/>
</a>

A showcase of the world's cultural clothing, as portrayed by local artists.

## Under the hood

This is a static website hosted on GitHub Pages.

### Mapping

Mapping is handled with [MapLibre GL JS](https://maplibre.org).

The map style _« world is hers »_ was designed to deemphasise political borders and names, allowing artwork to take prominence, with a playful style showing Earth topology.

Sincerest thanks to [**MapTiler**](https://www.maptiler.com), who have charitably donated a considerable amount of free hosting allowance.

### Post collation

Pulls posts from [@miku-earth on tumblr](https://miku-earth.tumblr.com) using `pytumblr2`, a custom library of mine I really should go upload at some point in time. I use a handful of tools to fetch, post-process and otherwise help me do my thang.

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

## Todo

- [ ] Bug: hovered posts not coming to forefront
- [ ] Bug: `get(showcase_i)` errors
- [ ] Investigate Chrome issues
- [ ] Reduce on-zoom lag: maybe only redraw `--miku-width` after a certain zoom level is reached?