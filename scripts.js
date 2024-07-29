function toggle_visibility(id_name, button) {
    document.getElementById(id_name).classList.toggle('hidden')
    button.classList.toggle('plus')
    button.classList.toggle('minus')
}

function fadeEffect() {
    if (document.querySelector('script-py')) {
        var preloader = document.querySelector('#preload');
        
        if (preloader != null && (preloader.style.opacity == "" || preloader.style.opacity > 0)) {
            if (preloader.style.opacity == "") {
                preloader.style.opacity = 1;
            }
            else if (preloader.style.opacity > 0) {
                preloader.style.opacity -= .1;
            }
        }

        if (preloader && preloader.style.opacity == 0) {
            preloader.remove();
            clearInterval(fadeEffect);
        }
    }
}

setInterval(fadeEffect, 100);

// while (document.getElementById('py-0') == null);
// if (document.getElementById('py-0')) {
//     fadeEffect();
// }
// window.addEventListener('load', fadeEffect);