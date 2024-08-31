
let today = new Date()
if (today.getMonth() == 7 && today.getDate() == 31) {
    // happy birthday miku!

    function xy(elem) {
        let vw = Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0)
        let vh = Math.max(document.documentElement.clientHeight || 0, window.innerHeight || 0)
        let { x, y } = elem.getBoundingClientRect()

        return { 'x': x / vw, 'y': y / vh };
    }

    let cake = $('a')
    cake.innerText = '🎂'
    cake.style = 'cursor: pointer'
    cake.title = "happy birthday miku!"
    const title = document.getElementById('title')
    title.appendChild($space())
    title.appendChild(cake)

    let confettisrc = $('script')
    confettisrc.src = "https://cdn.jsdelivr.net/npm/canvas-confetti@1.9.3/dist/confetti.browser.min.js";
    document.body.appendChild(confettisrc)


    let N = 0;

    cake.onclick = () => {
        N += 1;
        let colors = N % 10 ? ['#3dbdd5'] : undefined;
        let count = N % 10 ? 20 : 100;

        if (MIKUS[showcase_i].name == "Brazil") {
            count = 100;
            colors = [
                '#009B3A',
                '#FEDF00',
                '#002776'
            ]
        }
        if (MIKUS[showcase_i].shiny) {
            count = 50;
            colors = ['#ffd700']
        }

        confetti({
            'origin': xy(get(showcase_i)),
            'spread': 140,
            'particleCount': 100,
            'ticks': 100,
            'gravity': 0.3,
            'colors': colors,
            'shapes': ['square', 'square', 'star'],
            'disableForReducedMotion': true,
        });
    }
}