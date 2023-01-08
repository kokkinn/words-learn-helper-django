var row_cur = null;
var row_prev = null;

function listener_WlTableTd_Click(ev1) {
    ev1.preventDefault()
    let row_id = ev1.currentTarget.parentNode.id;
    console.log(`TD click fired for ${row_id}`)


    let menu = document.querySelector('.wl-menu-box');
    menu.classList.add('off');
    const a_upd = "{% url 'words:update' 0 %}".replace('0', row_id);

    menu.querySelectorAll('.wl-menu-item a')[0].href = a_upd;
    menu.id = row_id;
    menu.style.top = `${ev1.clientY - 20}px`;
    menu.style.left = `${ev1.clientX - 20}px`;
    menu.classList.remove('off');
    let elem = document.querySelector('.wl-menu-box .wl-menu-item a')
    elem.replaceWith(elem.cloneNode(true));
    $('.wl-menu-box .wl-menu-item a').click(function (ev2) {

        ev2.preventDefault();
        $(`[id=${row_id}] td input`)[0].classList.remove('off')
        $(`[id=${row_id}] td button`)[0].classList.remove('off')
        let input_field = document.querySelector('#sort-table tbody tr td:not(.wl-table-action) input')
        if (typeof (input_field) != 'undefined' && input_field != null) {
            let active_edit_id = input_field.parentNode.parentNode.id;
            let active_row = input_field.parentNode.parentNode;
            console.log(`Active EDIT found with ID ${active_edit_id}`);
            active_row.replaceWith(row_prev)
            $('.wl-table').trigger("update");
            $(`[id=${active_edit_id}] td:not(.wl-table-action)`).bind('click', listener_WlTableTd_Click);
            $(`[id=${active_edit_id}] td input`)[0].classList.add('off')
            $(`[id=${active_edit_id}] td button`)[0].classList.add('off')
        }
        row_prev = document.querySelector(`[id=${CSS.escape(row_id)}]:not(.wl-menu-box)`).cloneNode(true)
        $(`[id=${row_id}] td:not(.wl-table-action)`).unbind('click');
        let w1 = document.querySelector(`[id=${CSS.escape(row_id)}]:not(.wl-menu-box)`).cloneNode(true).firstElementChild.innerHTML;
        let w2 = document.querySelector(`[id=${CSS.escape(row_id)}]:not(.wl-menu-box)`).cloneNode(true).childNodes[3].innerHTML;
        $(`[id=${row_id}] td:not(.wl-table-action)`)[0].innerHTML =
            `<input maxlength="5000" required value=${w1}>`;
        $(`[id=${row_id}] td`)[1].innerHTML =
            `<input maxlength="5000" required value="${w2}">`;


    });
}

$('[id={{ word.id }}] td:not(.wl-table-action)').bind('click', listener_WlTableTd_Click);


document.querySelector('.wl-menu-box').addEventListener('mouseleave', function () {
    document.querySelector('.wl-menu-box').classList.add('off')
})


$('[id={{ word.id }}] td [id=table-confirm]').click(function (ev) {
    ev.preventDefault();
    let uuid = '{{ word.id }}';
    let w_1 = $('[id={{ word.id }}]:not(.wl-menu-box)').children('td')[0].children[0].value;
    let w_2 = $('[id={{ word.id }}]:not(.wl-menu-box)').children('td')[1].children[0].value;
    $.ajax({
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        data: {
            'word1': w_1,
            'word2': w_2
        },
        type: 'POST',
        url: '{% url 'words: update' 0 %}'.replace('0', uuid),
        success: function (response) {
            console.log('SUCCESS')
            $('[id={{ word.id }}]:not(.wl-menu-box)').children('td')[0].children[0].replaceWith(w_1)
            $('[id={{ word.id }}]:not(.wl-menu-box)').children('td')[1].children[0].replaceWith(w_2)

            $(`[id=${uuid}] td:not(.wl-table-action)`).bind('click', listener_WlTableTd_Click);
            $(`[id=${uuid}] td input`)[0].classList.add('off')
            $(`[id=${uuid}] td button`)[0].classList.add('off')
            jQuery('.wl-table').trigger("update");

        }
    })
})
