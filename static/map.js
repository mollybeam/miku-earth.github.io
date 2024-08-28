// yes i styled my own map. it was fun and hopefully makes for a nicer map experience!

const MIKU_KEY = "7u4GIZgEyI3d1WRGQSI0";
const DEV_KEY = "tKhcX9Y8K1Tuf3yejJxO";
const KEY = DEV_KEY;
var map = new maplibregl.Map({
    container: 'map', // container id
    style: `https://api.maptiler.com/maps/04d81168-126c-4527-92a3-10840848932d/style.json?key=${KEY}`,
    center: [0, 0], // starting position [lng, lat]
    zoom: 1 // starting zoom
});

map.on('load', () => {
    map
        .addSource('areas', {
            type: 'vector',
            url: `https://api.maptiler.com/data/ae1502a2-aa65-426a-8c80-6fa0685e0cd2/features.json?key=${KEY}`
        })
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

    let N = 0

    function shuffle(array) {
        // fisher-yates
        for (let i = array.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [array[i], array[j]] = [array[j], array[i]];
        }
        return array;
    }
    shuffle(MIKUS);

    const ANIMATION_TOTAL_SECONDS = 2.5;
    const ANIM_T = ANIMATION_TOTAL_SECONDS / MIKUS.length;

    MIKUS.forEach(miku => {
        if (!miku.coords) return;
        N++;

        // create a DOM element for the marker
        const el = document.createElement('a');
        el.className = 'miku';
        let delay = N * ANIM_T
        el.style = `opacity: 0; animation: fade-in 2.5s ${delay}s forwards`
        el.innerHTML = `
            <img class='preview' src="${miku.img_min_url}">
        `
        el.href = miku.post_url
        // <article>
        // ${miku.artist}
        // </article>

        el.addEventListener('mouseover', () => {
            console.log(miku);
        });

        let marker = new maplibregl.Marker({ element: el })
            .setLngLat(miku.coords)
            .addTo(map);
    });
    const count = document.getElementById('count');
    // why N and not length? we want to ignore meta posts.
    // (for timing purposes that's a trivial difference though!)
    count.innerText = N;
    count.classList.remove('transparent');
})