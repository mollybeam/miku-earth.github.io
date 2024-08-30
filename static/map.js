const do_animate = false;

// yes i styled my own map. it was fun and hopefully makes for a nicer map experience!

const KEY = "7u4GIZgEyI3d1WRGQSI0";
var map = new maplibregl.Map({
    container: 'map', // container id
    style: `https://api.maptiler.com/maps/04d81168-126c-4527-92a3-10840848932d/style.json?key=${KEY}`,
    center: [0, 0], // starting position [lng, lat]
    zoom: 1 // starting zoom
});

function attribute(map, text, url) {
    let a = document.createElement(url ? 'a' : 'span')
    a.innerText = ' ' + text
    if (url) {
        a.href = url
        a.target = '_blank'
    }
    let attrib = map.getContainer()
        .querySelector('.maplibregl-ctrl-attrib-inner')
    attrib.appendChild(document.createTextNode(" "))
    attrib.appendChild(a)
}
function shuffle(array) {
    // fisher-yates
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
}

map.on('load', () => {
    attribute(map, "© the respective artists")
    shuffle(MIKUS);

    const mikustyle = document.createElement('style');
    document.querySelector('head').appendChild(mikustyle)
    mikustyle.innerText = "";
    let setSize = () => {
        let z = map.getZoom();
        w = 3 ** (z / 5 + 1);
        // console.log(z, w)
        mikustyle.innerText = `.miku {--miku-width: ${w}em !important;}`
    }
    setSize()
    map.on('zoom', setSize)

    const ANIMATION_TOTAL_SECONDS = 2.5;
    const ANIM_T = ANIMATION_TOTAL_SECONDS / MIKUS.length;

    let N = 0
    MIKUS.forEach(miku => {
        if (miku.meta) return;
        if (!miku.coords)
            return console.log(miku.id, "no coords")
        if (!miku.name)
            console.log(miku.id, "no name")

        N++;

        const $ = x => document.createElement(x);

        // // // MIKU ELEMENT

        // div.miku
        //   a.summary
        //     img
        //   article

        // create a DOM element for the marker
        const div = $('div');
        div.id = `miku${miku.id}`;
        div.className = 'miku';

        const a = $('a')
        a.className = 'summary'
        a.target = '_blank'
        a.rel = 'nofollow'
        a.href = miku.post_url
        div.appendChild(a)

        const img = $('img')
        img.classList.add('preview')
        img.src = miku.thumb
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
            element: div,
            anchor: 'bottom',
        })
            .setLngLat(miku.coords)
            .addTo(map);
    });
    const count = document.getElementById('count');
    // why N and not length? we want to ignore meta posts.
    // (for timing purposes that's a trivial difference though!)
    count.innerText = N;
    count.classList.remove('transparent');
})