const do_animate = true;

var map = new maplibregl.Map({
    container: 'map',
    style: "https://api.maptiler.com/maps/04d81168-126c-4527-92a3-10840848932d/style.json?key=7u4GIZgEyI3d1WRGQSI0",
    // style: 'static/mapstyle.json',
    hash: true,
    center: [30, 30],
    zoom: 1.2,
    maxZoom: 6,
});

const $space = () => document.createTextNode(" ");
const $ = x => document.createElement(x);
let get = i => document.getElementById("miku" + MIKUS[i].id);

function attribute(map, text, prepend) {
    let span = document.createElement('span')
    span.innerHTML = ' ' + text
    let attrib = map.getContainer()
        .querySelector('.maplibregl-ctrl-attrib-inner')
    if (prepend) {
        attrib.prepend($space())
        attrib.prepend(span)
    } else {
        attrib.appendChild($space())
        attrib.appendChild(span)
    }
}
function shuffle(array) {
    // fisher-yates
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
}

let showcase_i = 0;
map.on('load', () => {
    document.getElementById('mapfallback').remove()
    attribute(map, "© respective artists")
    attribute(map, "• collated by <a href='https://tumblr.com/ awnowimsad'>awnowimsad</a> & <a href='https://tumblr.com/mira-hildegard'>mira</a>")
    shuffle(MIKUS);

    // // // Zooming makes mikus slightly larger

    const mikustyle = document.createElement('style');
    document.querySelector('head').appendChild(mikustyle)
    mikustyle.innerText = "";
    let setSize = () => {
        let z = map.getZoom();
        // TODO: smaller miku, but gets larger on hover?
        w = Math.min(2.2 * 3 ** (z / 3), 8);
        mikustyle.innerText = `.miku {--miku-zoom-width: ${w}em !important;}`
    }
    setSize()
    map.on('zoom', setSize)

    // anim setup
    const ANIMATION_TOTAL_SECONDS = 5;
    const ANIM_T = ANIMATION_TOTAL_SECONDS / MIKUS.length;

    let N = 0
    MIKUS.forEach((miku, i) => {
        if (!miku.coords)
            return;
        if (!miku.coords.length)
            return;

        if (miku.name == "Brazil") {
            // always start the showcase where the trend started!
            showcase_i = i - 1;
        }
        N++;

        // // // MIKU ELEMENT

        // div.miku
        //   a.summary
        //     img
        //   article

        // create a DOM element for the marker
        const container = $('div');

        const div = $('div');
        div.id = `miku${miku.id}`;
        div.classList.add('miku');
        if (miku.shiny) {
            div.classList.add('shiny')
        }
        container.appendChild(div)

        const a = $('a')
        a.className = 'summary'
        a.target = '_blank'
        a.rel = 'nofollow'
        a.href = miku.post_url
        div.appendChild(a)

        const TUMBLR_MEDIA = 'https://64.media.tumblr.com/'
        let prefix = miku.thumb.startsWith('https://') ? "" : TUMBLR_MEDIA;

        const img = $('img')
        img.classList.add('preview')
        img.src = prefix + miku.thumb;
        a.appendChild(img)

        const article = $('article');
        div.appendChild(article)

        // // // ARTICLE

        let wiki = "https://en.wikipedia.org/wiki/"
            + (miku.wikipedia ? miku.wikipedia : miku.name).replace(" ", "_")

        article.innerHTML = `
        <div class='article-content'>
            <p class='title'>
                <a href="${wiki}" target='_blank' rel='nofollow'>${miku.name}</a>
            </p>
            <p class='artist'>
                <i>by
                    <a href='${miku.artist_url}' target='_blank' rel='nofollow'>
                        ${miku.artist}</a>
                </i>
            </p>
        </div>
        `

        if (do_animate) {
            let delay = N * ANIM_T
            div.style = `opacity: 0; animation: fade-in 2.5s ${delay}s forwards`
        }

        let marker = new maplibregl.Marker({
            element: container,
        })
            .setLngLat(miku.coords)
            .addTo(map);
    });
    const count = document.getElementById('count');
    // why N and not length? we want to ignore meta posts.
    // (for timing purposes that's a trivial difference though!)
    count.innerText = N;
    count.classList.remove('transparent');

    let inc = () => showcase_i = (showcase_i + 1) % MIKUS.length;
    // we have to skip meta posts
    let next = () => { inc(); while (!get(showcase_i)) inc(); }

    function new_showcase() {
        // console.log(showcase_i, get(showcase_i))
        get(showcase_i).classList.remove('hover')
        next()
        get(showcase_i).classList.add('hover')
    }
    window.setInterval(new_showcase, 5_000)
})