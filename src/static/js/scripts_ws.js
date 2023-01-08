function checker(ev) {
    const result = confirm('Are you sure ?');
    if (result === false) {
        ev.preventDefault()
    }

}

function getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== "") {
                const cookies = document.cookie.split(";");
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    if (cookie.substring(0, name.length + 1) === (name + "=")) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
async function notify(msg, type) {
    let not_area = document.getElementById('not-area')
    const id = Math.random().toString(36).slice(2);
    let n_a_child = document.createElement('div')
    n_a_child.classList.add('not-msg')
    switch (type) {
        case "error":
            n_a_child.style.backgroundColor = 'darkorange';
            break;
        case "info":
            n_a_child.style.background = 'goldenrod';
            break;
        case "success":
             n_a_child.style.background = 'goldenrod';
            break;
    }
    n_a_child.id = id
    n_a_child.innerText = msg
    not_area.appendChild(n_a_child)
    n_a_child.style.maxHeight = n_a_child.scrollHeight + 'px';
    await new Promise(r => setTimeout(r, 0));
    n_a_child.style.transform = 'translateX(-220px)'
    n_a_child.addEventListener('transitionend', async (event) => {
        await new Promise(r => setTimeout(r, 200));
        n_a_child.style.transform = 'translateX(220px)'
        n_a_child.addEventListener('transitionend', () => {
            n_a_child.style.border = 'none'
            n_a_child.style.maxHeight = '0';
            n_a_child.style.padding = '0';
            n_a_child.addEventListener('transitionend', () => {
                n_a_child.remove()
            })
        })
        ;

        // await new Promise(r => setTimeout(r, 1200));

    })
}


// function notifySuccess(message) {
//     notify("success", message);
// }
//
// function notifyError(message) {
//     notify("error", message);
// }
//
// function notifyInfo() {
//     notify("info", "This is demo info notification message");



