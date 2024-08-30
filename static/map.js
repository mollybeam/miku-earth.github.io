// yes i styled my own map. it was fun and hopefully makes for a nicer map experience!

const MIKU_KEY = "7u4GIZgEyI3d1WRGQSI0";
const KEY = MIKU_KEY;
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

    // map
    //     .addSource('areas', {
    //         type: 'vector',
    //         url: `https://api.maptiler.com/data/ae1502a2-aa65-426a-8c80-6fa0685e0cd2/features.json?key=${KEY}`
    // })
    // .addLayer({
    //     id: 'areas',
    //     type: 'fill',
    //     source: 'areas',
    //     'source-layer': 'features',
    //     paint: {
    //         'fill-color': '#888888',
    //         'fill-opacity': 0.5
    //     },
    //     // filter: ['==', ['get', 'name'], 'moravia1']
    // }, "")

    const mikustyle = document.createElement('style');
    document.querySelector('head').appendChild(mikustyle)
    mikustyle.innerText = "";
    let setSize = () => {
        let z = map.getZoom();
        w = 3 ** (z / 5 + 1);
        // console.log(z, w)
        mikustyle.innerText = `.miku img {width: ${w}em !important; height: ${w}em !important; overflow: hidden}`
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

        // create a DOM element for the marker
        const a = document.createElement('a');
        a.className = 'miku';
        a.id = `miku${miku.id}`;
        let delay = N * ANIM_T
        a.style = `opacity: 0; animation: fade-in 2.5s ${delay}s forwards`
        a.title = `${miku.name} / @${miku.artist}`

        const img = document.createElement('img')
        img.classList.add('preview')
        img.src = miku.thumb

        // img.srcset = miku.srcset
        // img.style = `width: 4em !important;`

        a.appendChild(img)
        a.href = miku.post_url
        // <article>
        // ${miku.artist}
        // </article>

        a.addEventListener('mouseover', () => {
            console.log(miku);
            // img.srcset = miku.srcset;
            // img.width = '500px';
        });

        let marker = new maplibregl.Marker({ element: a })
            .setLngLat(miku.coords)
            .addTo(map);
    });
    const count = document.getElementById('count');
    // why N and not length? we want to ignore meta posts.
    // (for timing purposes that's a trivial difference though!)
    count.innerText = N;
    count.classList.remove('transparent');
})