function toggle_visibility(id_name, button) {
    document.getElementById(id_name).classList.toggle('hidden')
    button.classList.toggle('plus')
    button.classList.toggle('minus')
}

function verse_selection_loaded(id_name) {
    var h1_tag = document.querySelector(id_name)

    if (h1_tag.value.indexOf(' (Loading...)') != -1) {
        h1_tag.innerText(h1_tag.value.replace(' (Loading...)', ' (Loaded)'))
    }
}