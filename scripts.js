function toggle_visibility(id_name, button) {
    document.getElementById(id_name).classList.toggle('hidden')
    button.classList.toggle('plus')
    button.classList.toggle('minus')
}

function fadeEffect() {
    var preloader = document.querySelector('#preload');
    
    while (preloader != null && (preloader.style.opacity == "" || preloader.style.opacity > 0)) {
        if (preloader.style.opacity == "") {
            preloader.style.opacity = 1;
        }
        else if (preloader.style.opacity > 0) {
            preloader.style.opacity -= .1;
        }
    }

    if (preloader) {
        preloader.remove();
    }
}

var interval = setInterval(function() {
    if(document.readyState === 'complete') {
        clearInterval(interval);
        fadeEffect();
        done();
    }    
}, 100);
// window.onload('load', fadeEffect);