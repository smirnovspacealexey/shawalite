/**
 * Created by paul on 15.07.17.
 */
var preorder_checkbox;
var pickup_checkbox;
const channel = new BroadcastChannel('app-data');

$(document).ready(function () {
        initiate()
});

function initiate() {
    $('#menu').addClass('header-active');
    $('.menu-item').hide();
    $('.subm').prop('disabled', false);
    $('#cook_none').prop('checked', true);
    $('[name="discount"]').prop('checked', false);
    preorder_checkbox = $('[name=preorder_checkbox]');
    preorder_checkbox.prop("checked", false);
    pickup_checkbox = $('[name=pickup_checkbox]');
    pickup_checkbox.prop("checked", false);

    // Get the modal
    var modal = document.getElementById('modal-edit');
    var modalStatus = document.getElementById('modal-status');

    // Get the <span> element that closes the modal
    var span = document.getElementById("close-modal");
    var spanStatus = document.getElementById("close-modal-status");

    // When the user clicks on <span> (x), close the modal
    span.onclick = function () {
        CloseModalEdit();
    };
    // spanStatus.onclick = function () {
    //     CloseModalStatus();
    // };

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function (event) {
        if (event.target == modal) {
            CloseModalEdit();
        }
        // else {
        //     if (event.target == modalStatus) {
        //         CloseModalStatus();
        //     }
        // }
    }
}

var currOrder = [];
var current_retries = 0;
var max_retries = 135;
var total = 0;
var res = "";
var csrftoken = $("[name=csrfmiddlewaretoken]").val();


$(function () {
    $('.subm').on('click', SendOrder);
});

function SendOrder() {
    if (currOrder.length > 0) {
        for (let i = 0; i < currOrder.length; i++) {
            if (currOrder[i]['qr_req'] && currOrder[i]['qr'] === '') {
                alert("QR обязатален: " + currOrder[i]['title']);
                ShowModalEdit(i)
                return
            }
        }
        current_retries = 0;
        var OK = $('#status-OK-button');
        var cancel = $('#status-cancel-button');
        var retry = $('#status-retry-button');
        var retry_cash = $('#status-retry-cash-button');
        var change_label = $('#order-change-label');
        var change = $('#order-change');
        var change_display = $('#change-display');
        var status = $('#status-display');
        var payment_choose = $('[name=payment_choose]:checked');
        var loading_indiactor = $('#loading-indicator');
        var is_modal = $('#is-modal');
        var delivery_daily_number = $('#delivery_daily_number');
        var confirmation = confirm("Подтвердить заказ?");
        var form = $('.subm');

        if (confirmation == true) {
            ShowModalStatus();
            OK.prop('disabled', true);
            cancel.prop('disabled', true);
            retry.prop('disabled', true);
            loading_indiactor.show();
            status.text('Отправка заказа...');
            if (payment_choose.val() == "paid_with_cash") {
                change.show();
                change.select();
                change_label.show();
                change_display.show();
            }
            var order_data = {
                "order_content": JSON.stringify(currOrder),
                "payment": $('[name=payment_choose]:checked').val(),
                "delivery_daily_number": delivery_daily_number.val(),
                "cook_choose": $('[name=cook_choose]:checked').val(),
                "discount": $('[name=discount]:checked').val() ? parseFloat($('[name=discount]:checked').val()) : 0,
                "is_preorder": preorder_checkbox.prop("checked") ? 1 : 0,
                "is_pickup": pickup_checkbox.prop("checked") ? 1 : 0
            };
            var order_id = $('#order_id').val();
            if (order_id)
                order_data["order_id"] = order_id;

            $('.subm').prop('disabled', true);
            $.ajaxSetup({
                beforeSend: function (xhr, settings) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken)
                }
            });
            $.ajax({
                    type: 'POST',
                    url: form.attr('data-send-url'),
                    data: order_data,
                    dataType: 'json',
                    success: function (data) {
                        if (data['success']) {
                            if (payment_choose.val() != "not_paid" && payment_choose.val() != "paid_web") {
                                if (payment_choose.val() == "paid_with_cash") {
                                    status.text('Заказ №' + data.display_number + ' добавлен! Введите полученную сумму:');
                                    //var cash = prompt('Заказ №' + data.daily_number + ' добавлен!, Введите полученную сумму:', "");
                                    //alert("Сдача: " + (parseInt(cash) - total))
                                }
                                else {
                                    status.text('Заказ №' + data.display_number + ' добавлен! Активация платёжного терминала...');
                                    //alert('Заказ №' + data.daily_number + ' добавлен!');
                                }
                                setTimeout(function () {
                                    StatusRefresher(data['guid']);
                                }, 1000);
                            }
                            else {
                                status.text('Заказ №' + data.display_number + ' добавлен!');
                                OK.prop('disabled', false);
                                cancel.prop('disabled', true);
                                retry.prop('disabled', true);
                                if (is_modal.val() == 'True') {
                                    OK.off('click');
                                    OK.unbind('click', OKHandeler);
                                    OK.click(function () {
                                        DeliveryOKHandeler(data['pk']);
                                    });
                                }
                                OK.focus();
                                loading_indiactor.hide();
                                cleanDeliveryForm();
                            }

                        }
                        else {
                            status.text(data['message']);
                            OK.prop('disabled', true);
                            cancel.prop('disabled', false);
                            retry.prop('disabled', false);
                            loading_indiactor.hide();
                        }
                    }
                }
            ).fail(function () {
                loading_indiactor.hide();
                status.text('Необработанное исключение!');
            });
        }
    }
    else {
        alert("Пустой заказ!");
    }
}

function StatusRefresher(guid) {
    var status = $('#status-display');
    var OK = $('#status-OK-button');
    var cancel = $('#status-cancel-button');
    var retry = $('#status-retry-button');
    var retry_cash = $('#status-retry-cash-button');
    var payment_choose = $('[name=payment_choose]:checked');
    var loading_indiactor = $('#loading-indicator');
    if (current_retries < max_retries) {
        current_retries++;
        status.text('Попытка ' + current_retries + ' из ' + max_retries);
        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken)
            }
        });
        $.ajax({
                type: 'POST',
                url: $('#menu-urls').attr('data-status-refresh-url'),
                data: {
                    "order_guid": guid
                },
                dataType: 'json',
                success: function (data) {
                    if (data['success']) {
                        switch (data['status']) {
                            case 0:
                                setTimeout(function () {
                                    StatusRefresher(data['guid']);
                                }, 1000);
                                break;
                            case 397:
                            case 396:
                            case 395:
                            case 394:
                            case 391:
                            case 390:
                                OK.prop('disabled', true);
                                cancel.prop('disabled', false);
                                retry.prop('disabled', false);
                                if (payment_choose.val() != "paid_with_cash")
                                    retry_cash.show();
                                break;
                            // case 396:
                            //     OK.prop('disabled', true);
                            //     cancel.prop('disabled', false);
                            //     retry.prop('disabled', false);
                            //     break;
                            case 393:
                            case 392:
                                if (payment_choose == "paid_with_cash")
                                    status.text('Заказ №' + data.daily_number + '. ' + data['message'] + ' Введите полученную сумму, отдайте клиенту сдачу и нажмите ОК');
                                else
                                    status.text('Заказ №' + data.daily_number + '. ' + data['message'] + ' проведён в 1С! Операция безналичного расчёта завершена успешно! Нажмите ОК');
                                OK.prop('disabled', false);
                                cancel.prop('disabled', true);
                                retry.prop('disabled', true);
                                OK.focus();
                                break;
                            case 200:
                                if (payment_choose.val() == "paid_with_cash")
                                    status.text('Заказ №' + data.daily_number + ' проведён в 1С! Введите полученную сумму, отдайте клиенту сдачу и нажмите ОК');
                                else
                                    status.text('Заказ №' + data.daily_number + ' проведён в 1С! Операция безналичного расчёта завершена успешно! Нажмите ОК');
                                OK.prop('disabled', false);
                                cancel.prop('disabled', true);
                                retry.prop('disabled', true);
                                OK.focus();
                                break;
                            default:
                                OK.prop('disabled', true);
                                cancel.prop('disabled', false);
                                retry.prop('disabled', false);
                                break;
                        }
                        if (data['status'] != 0)
                            loading_indiactor.hide();
                        if (data['status'] != 200)
                            status.text('Заказ №' + data.daily_number + '. ' + data['message']);
                    }
                    else {
                        OK.prop('disabled', true);
                        cancel.prop('disabled', false);
                        retry.prop('disabled', false);
                        status.text(data['message']);
                        loading_indiactor.hide();
                    }
                }
            }
        ).fail(function () {
            OK.prop('disabled', false);
            cancel.prop('disabled', true);
            retry.prop('disabled', true);
            loading_indiactor.hide();
            status.text('Необработанное исключение!');
        });
    }
    else {
        OK.prop('disabled', false);
        cancel.prop('disabled', true);
        retry.prop('disabled', true);
        status.text('Превышено количество попыток!');
    }
}

function OKHandeler() {
    currOrder = [];
    DrawOrderTable();
    CalculateTotal();
    $('#cook_auto').prop('checked', true);
    CloseModalStatus();
    console.log('OKHandler fired.');
    location.reload();
}

function DeliveryOKHandeler(order_pk) {
    var modal_window = $('#modal-menu');
    var customer_pk = $('#current-order-data').attr('customer-pk');
    //CreateDeliveryOrder(-1, customer_pk, -1, order_pk);
    $("#id_order").val(order_pk);
    $("#id_moderation_needed").val("False");
    currOrder = [];
    DrawOrderTable();
    CalculateTotal();
    $('#cook_auto').prop('checked', true);
    CloseModalStatus();
    // location.reload();
    modal_window.html('');
    modal_window.hide();
    CheckOrderIdPresence();
    console.log('DeliveryOKHandeler fired.');
}

function CancelHandler() {
    currOrder = [];
    DrawOrderTable();
    CalculateTotal();
    $('#cook_auto').prop('checked', true);
    CloseModalStatus();
    console.log('CancelHandler fired.');
    location.reload();
}

function RetryHandler() {
    CloseModalStatus();
    SendOrder();
}

function RetryCashHandler() {
    $('#paid_with_cash').prop('checked', true);
    CloseModalStatus();
    SendOrder();
}

function Remove(index) {
    var quantity = $('#count-to-remove-' + index).val();
    if (currOrder[index]['quantity'] - quantity <= 0)
        currOrder.splice(index, 1);
    else
        currOrder[index]['quantity'] = parseInt(currOrder[index]['quantity']) - parseInt(quantity);
    CalculateTotal();
    DrawOrderTable();
    channel.postMessage(JSON.stringify(currOrder));
}

function AddOne(id, title, price, qr_req) {
    var quantity = 1;
    var note = '';
    var index = FindItem(id, note);
    if (index == null) {
        currOrder.push(
            {
                'id': id,
                'title': title,
                'price': price,
                'quantity': quantity,
                'note': note,
                'qr': '',
                'qr_req': qr_req,
            }
        );
    }
    else {
        currOrder[index]['quantity'] = parseInt(quantity) + parseInt(currOrder[index]['quantity']);
    }
    channel.postMessage(JSON.stringify(currOrder));
    CalculateTotal();
    DrawOrderTable();
}

function EditNote(id, note) {
    var newnote = prompt("Комментарий", note);
    if (newnote != null) {
        var index = FindItem(id, note);
        if (index != null) {
            currOrder[index]['note'] = newnote;
        }
    }
    DrawOrderTable();
}

function SelectSuggestion(id, note) {
    // var newnote = prompt("Комментарий", note);
    // if (newnote != null) {
    //     var index = FindItem(id, note);
    //     if (index != null) {
    //         currOrder[index]['note'] = newnote;
    //     }
    // }
    $('#note-' + id).val(note);
    $('#item-note').val(note);
    if (id != null) {
        currOrder[id]['note'] = $('#item-note').val();
    }
    DrawOrderTable();
    channel.postMessage(JSON.stringify(currOrder));
}

function Add(id, title, price) {
    var quantity = $('#count-' + id).val();
    var note = $('#note-' + id).val();
    $('#note-' + id).val('');
    $('#count-' + id).val('1');
    var index = FindItem(id, note);
    if (index == null) {
        currOrder.push(
            {
                'id': id,
                'title': title,
                'price': price,
                'quantity': quantity,
                'note': note
            }
        );
    }
    else {
        currOrder[index]['quantity'] = parseInt(quantity) + parseInt(currOrder[index]['quantity']);
    }
    CalculateTotal();
    DrawOrderTable();
    channel.postMessage(JSON.stringify(currOrder));
}

function PlusOneItem(index) {
    var quantity = $('#item-quantity');
    currOrder[index]['quantity'] += 1;
    quantity.val(currOrder[index]['quantity']);
    CalculateTotal();
    DrawOrderTable();
    channel.postMessage(JSON.stringify(currOrder));
}

function MinusOneItem(index) {
    var quantity = $('#item-quantity');
    var modal = document.getElementById('modal-edit');
    if (currOrder[index]['quantity'] - 1 > 0) {
        currOrder[index]['quantity'] -= 1;
        quantity.val(currOrder[index]['quantity']);
    }
    else {
        currOrder[index]['quantity'] = 0;
        currOrder.splice(index, 1);
        CloseModalEdit();
    }
    CalculateTotal();
    DrawOrderTable();
    channel.postMessage(JSON.stringify(currOrder));
}

function UpdateQuantity(index) {
    var quantity = $('#item-quantity');
    var modal = document.getElementById('modal-edit');
    var aux_quantity = parseFloat((quantity.val()).replace(/,/g, '.'));
    if (aux_quantity > 0) {
        currOrder[index]['quantity'] = aux_quantity;
        quantity.val(currOrder[index]['quantity']);
    }
    else {
        currOrder[index]['quantity'] = 0;
        currOrder.splice(index, 1);
        CloseModalEdit();
    }
    CalculateTotal();
    DrawOrderTable();
    channel.postMessage(JSON.stringify(currOrder));
}

function FindItem(id, note) {
    var index = null;
    for (var i = 0; i < currOrder.length; i++) {
        if (currOrder[i]['id'] == id && currOrder[i]['note'] == note) {
            index = i;
            break;
        }
    }
    return index;
}

// onclick="EditNote(' + currOrder[i]['id'] + ',\'' + currOrder[i]['note'] + '\')"
// <div id="dropdown-list-container"></div>
function DrawOrderTable() {
    $('#menu-order-display tbody tr').remove();
    for (var i = 0; i < currOrder.length; i++) {
        let qr_str = ''
        if (currOrder[i]['qr_req']) {
            if (currOrder[i]['qr'] === '') {
                qr_str = '<img style="border: 2px double #FF0000;" title="QR обязателен❗" height="22" src="data:image/png;base64,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" />'
            } else {
                qr_str = '<img style="border: 2px double #1aff00;" title="QR введён ✓" height="20" src="data:image/png;base64,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" />'
            }
        }

        $('#menu-order-display').append(
            // '<tr class="currentOrderRow" index="' + i + '"><td class="currentOrderTitleCell" onclick="ShowModalEdit(' + i + ')">' +
            // '<div>' + currOrder[i]['title'] + '</div><div class="noteText">' + currOrder[i]['note'] + '</div>' +
            // '</td><td class="currentOrderActionCell">' + 'x' + currOrder[i]['quantity'] +
            // '<input type="text" value="1" class="quantityInput" id="count-to-remove-' + i + '">' +
            // '<button class="btnRemove" onclick="Remove(' + i + ')">Убрать</button>' +
            // '<input type="text" value="' + currOrder[i]['note'] + '" class="live-search-box" id="note-' + i + '" onkeyup="ss(' + i + ','+currOrder[i]['id']+')">' +
            // '' +
            // '</td></tr>'
            '<tr class="currentOrderRow" index="' + i + '"><td class="currentOrderTitleCell" onclick="ShowModalEdit(' + i + ')">' +
            '<div class="table-item-title">' + currOrder[i]['title'] + qr_str + '</div><div class="noteText">' + currOrder[i]['note'] + '</div>' +
            '</td><td class="currentOrderActionCell">' + 'x' + currOrder[i]['quantity'] + '<button class="small-btn danger" onclick="MinusOneItem(' + i + ')">-1</button></td></tr>'
        );
    }
}

function ShowModalEdit(index) {
    var title = $('#item-title');
    var quantity = $('#item-quantity');
    var note = $('#item-note');
    var qr = $('#item-qr');
    var plus = $('#plus-button');
    var minus = $('#minus-button');

    var cheese = $('#cheese-button');
    var greens = $('#greens-button');
    var spicy = $('#spicy-button');
    var spicy30 = $('#spicy30-button');
    var yellow = $('#yellow-button');
    var noOnion = $('#noOnion-button');
    var saucePlus = $('#saucePlus-button');
    var sauceMinus = $('#sauceMinus-button');
    var noVegetables = $('#noVegetables-button');
    var frenchFries = $('#frenchFries-button');
    var chile = $('#chile-button');
    var mushrooms = $('#mushrooms-button');
    var jalapeno = $('#jalapeno-button');
    var bellPepper = $('#bellPepper-button');

    var note1 = $('#note1');
    var note2 = $('#note2');
    var note3 = $('#note3');
    var note4 = $('#note4');
    var note5 = $('#note5');
    var note6 = $('#note6');
    var note7 = $('#note7');
    var note8 = $('#note8');
    var note9 = $('#note9');
    var note10 = $('#note10');
    var note11 = $('#note11');
    var note12 = $('#note12');
    var note13 = $('#note13');
    var note14 = $('#note14');
    var note15 = $('#note15');
    var note16 = $('#note16');
    var note17 = $('#note17');
    var note18 = $('#note18');
    var note19 = $('#note19');
    var note20 = $('#note20');

    title.text(currOrder[index]['title']);
    quantity.val(currOrder[index]['quantity']);
    quantity.blur(
        function () {
            UpdateQuantity(index);
        }
    );
    quantity.keyup(
        function (event) {
            if (event.keyCode === 13) {
                UpdateQuantity(index);
                CloseModalEdit();
            }
        }
    );
    note.val(currOrder[index]['note']);
    qr.val(currOrder[index]['qr']);
    note.keyup(
        function (event) {
            if (event.keyCode === 13) {
                SelectSuggestion(index, note.val());
                CloseModalEdit();
            }
            else {
                ss(index, currOrder[index]['id']);
            }
        }
    );
    note.blur(
        function () {
            SelectSuggestion(index, note.val());
        }
    );

    qr.off("input",);
    qr.off("keydown",);

    qr.keydown(function(e) {
        if(e.keyCode === 9) {
            setTimeout(tabBack, 50)
            function tabBack() {
                qr.focus()
            }
            let qr_val = rus_to_latin(qr.val() + '☯')
            qr.val(qr_val);
            currOrder[index]['qr'] = qr_val;
        }
    });

    // qr.on('input', function() {
    //     addSymbolInQR(index, qr)
    // })


    plus.click(
        function () {
            PlusOneItem(index);
        }
    );
    minus.click(
        function () {
            MinusOneItem(index);
        }
    );
    cheese.click(
        function () {
            var str = ' Сыр';
            if (note.val().includes(str)) {
                note.val(note.val().replace(str, ''));
            }
            else {
                note.val(note.val() + str);
            }
            SelectSuggestion(index, note.val());
        }
    );
    greens.click(
        function () {
            var str = ' Зелень';
            if (note.val().includes(str)) {
                note.val(note.val().replace(str, ''));
            }
            else {
                note.val(note.val() + str);
            }
            SelectSuggestion(index, note.val());
        }
    );
    spicy.click(
        function () {
            var str = ' Острая';
            if (note.val().includes(str)) {
                note.val(note.val().replace(str, ''));
            }
            else {
                note.val(note.val() + str);
            }
            SelectSuggestion(index, note.val());
        }
    );
    spicy30.click(
        function () {
            var str = ' Чуть-Острая';
            if (note.val().includes(str)) {
                note.val(note.val().replace(str, ''));
            }
            else {
                note.val(note.val() + str);
            }
            SelectSuggestion(index, note.val());
        }
    );
    yellow.click(
        function () {
            var str = ' Ж';
            if (note.val().includes(str)) {
                note.val(note.val().replace(str, ''));
            }
            else {
                note.val(note.val() + str);
            }
            SelectSuggestion(index, note.val());
        }
    );
    noOnion.click(
        function () {
            var str = ' Без лука';
            if (note.val().includes(str)) {
                note.val(note.val().replace(str, ''));
            }
            else {
                note.val(note.val() + str);
            }
            SelectSuggestion(index, note.val());
        }
    );
    saucePlus.click(
        function () {
            var str = ' Больше соуса';
            if (note.val().includes(str)) {
                note.val(note.val().replace(str, ''));
            }
            else {
                note.val(note.val() + str);
            }
            SelectSuggestion(index, note.val());
        }
    );
    sauceMinus.click(
        function () {
            var str = ' Меньше соуса';
            if (note.val().includes(str)) {
                note.val(note.val().replace(str, ''));
            }
            else {
                note.val(note.val() + str);
            }
            SelectSuggestion(index, note.val());
        }
    );
    noVegetables.click(
        function () {
            var str = ' Без овощей';
            if (note.val().includes(str)) {
                note.val(note.val().replace(str, ''));
            }
            else {
                note.val(note.val() + str);
            }
            SelectSuggestion(index, note.val());
        }
    );
    frenchFries.click(
        function () {
            var str = ' Фри';
            if (note.val().includes(str)) {
                note.val(note.val().replace(str, ''));
            }
            else {
                note.val(note.val() + str);
            }
            SelectSuggestion(index, note.val());
        }
    );

    note1.click(
        function () {
            addNote(note1.attr('title'))
        }
    );
    note2.click(
        function () {
            addNote(note2.attr('title'))
        }
    );
    note3.click(
        function () {
            addNote(note3.attr('title'))
        }
    );
    note4.click(
        function () {
            addNote(note4.attr('title'))
        }
    );
    note5.click(
        function () {
            addNote(note5.attr('title'))
        }
    );
    note6.click(
        function () {
            addNote(note6.attr('title'))
        }
    );
    note7.click(
        function () {
            addNote(note7.attr('title'))
        }
    );
    note8.click(
        function () {
            addNote(note8.attr('title'))
        }
    );
    note9.click(
        function () {
            addNote(note9.attr('title'))
        }
    );
    note10.click(
        function () {
            addNote(note10.attr('title'))
        }
    );
    note11.click(
        function () {
            addNote(note11.attr('title'))
        }
    );
    note12.click(
        function () {
            addNote(note12.attr('title'))
        }
    );
    note13.click(
        function () {
            addNote(note13.attr('title'))
        }
    );
    note14.click(
        function () {
            addNote(note14.attr('title'))
        }
    );
    note15.click(
        function () {
            addNote(note15.attr('title'))
        }
    );
    note16.click(
        function () {
            addNote(note16.attr('title'))
        }
    );
    note17.click(
        function () {
            addNote(note17.attr('title'))
        }
    );
    note18.click(
        function () {
            addNote(note18.attr('title'))
        }
    );
    note19.click(
        function () {
            addNote(note19.attr('title'))
        }
    );
    note20.click(
        function () {
            addNote(note20.attr('title'))
        }
    );

    function addNote(title) {
        var str = ' ' + title;
        if (note.val().includes(str)) {
            note.val(note.val().replace(str, ''));
        }
        else {
            note.val(note.val() + str);
        }
        SelectSuggestion(index, note.val());
    }


    chile.click(
        function () {
            var str = ' Чили';
            if (note.val().includes(str)) {
                note.val(note.val().replace(str, ''));
            }
            else {
                note.val(note.val() + str);
            }
            SelectSuggestion(index, note.val());
        }
    );
    mushrooms.click(
        function () {
            var str = ' Грибы';
            if (note.val().includes(str)) {
                note.val(note.val().replace(str, ''));
            }
            else {
                note.val(note.val() + str);
            }
            SelectSuggestion(index, note.val());
        }
    );
    jalapeno.click(
        function () {
            var str = ' Халапеньо';
            if (note.val().includes(str)) {
                note.val(note.val().replace(str, ''));
            }
            else {
                note.val(note.val() + str);
            }
            SelectSuggestion(index, note.val());
        }
    );
    bellPepper.click(
        function () {
            var str = ' Болгарский перец';
            if (note.val().includes(str)) {
                note.val(note.val().replace(str, ''));
            }
            else {
                note.val(note.val() + str);
            }
            SelectSuggestion(index, note.val());
        }
    );

    // Get the modal
    var modal = document.getElementById('modal-edit');

    modal.style.display = "block";

    if (currOrder[index]['qr_req']) {
        title.append('<span style="margin-left: 20px; color: rgba(246,96,2,0.76); font-size: 8pt;">QR</span>');
        qr.focus();
        qr.css({"outline": "3px solid rgba(246,96,2,0.76)"});
        qr.attr('placeholder', 'QR код товара (!ОБЯЗАТЕЛЕН)')
    } else {
        qr.attr("style", "outline: 0px hidden");
        qr.attr('placeholder', 'QR код товара')
        note.focus()
    }

}

function CloseModalEdit() {
    var title = $('#item-title');
    var quantity = $('#item-quantity');
    var note = $('#item-note');
    var plus = $('#plus-button');
    var minus = $('#minus-button');

    var cheese = $('#cheese-button');
    var greens = $('#greens-button');
    var spicy = $('#spicy-button');
    var spicy30 = $('#spicy30-button');
    var yellow = $('#yellow-button');
    var noOnion = $('#noOnion-button');
    var saucePlus = $('#saucePlus-button');
    var sauceMinus = $('#sauceMinus-button');
    var noVegetables = $('#noVegetables-button');
    var frenchFries = $('#frenchFries-button');
    var chile = $('#chile-button');
    var mushrooms = $('#mushrooms-button');
    var jalapeno = $('#jalapeno-button');
    var bellPepper = $('#bellPepper-button');

    var note1 = $('#note1');
    var note2 = $('#note2');
    var note3 = $('#note3');
    var note4 = $('#note4');
    var note5 = $('#note5');
    var note6 = $('#note6');
    var note7 = $('#note7');
    var note8 = $('#note8');
    var note9 = $('#note9');
    var note10 = $('#note10');
    var note11 = $('#note11');
    var note12 = $('#note12');
    var note13 = $('#note13');
    var note14 = $('#note14');
    var note15 = $('#note15');
    var note16 = $('#note16');
    var note17 = $('#note17');
    var note18 = $('#note18');
    var note19 = $('#note19');
    var note20 = $('#note20');

    var modal = document.getElementById('modal-edit');

    quantity.off("blur");
    quantity.off("keyup");
    note.off("keyup");
    note.off("blur");
    plus.off("click");
    minus.off("click");

    cheese.off("click");
    greens.off("click");
    spicy.off("click");
    spicy30.off("click");
    yellow.off("click");
    noOnion.off("click");
    saucePlus.off("click");
    sauceMinus.off("click");
    noVegetables.off("click");
    frenchFries.off("click");
    chile.off("click");
    mushrooms.off("click");
    jalapeno.off("click");
    bellPepper.off("click");

    note1.off("click");
    note2.off("click");
    note3.off("click");
    note4.off("click");
    note5.off("click");
    note6.off("click");
    note7.off("click");
    note8.off("click");
    note9.off("click");
    note10.off("click");
    note11.off("click");
    note12.off("click");
    note13.off("click");
    note14.off("click");
    note15.off("click");
    note16.off("click");
    note17.off("click");
    note18.off("click");
    note19.off("click");
    note20.off("click");

    modal.style.display = "none";
    DrawOrderTable()
}

function ShowModalStatus() {
    var retry_cash = $('#status-retry-cash-button');
    var change_label = $('#order-change-label');
    var change = $('#order-change');

    // Get the modal
    var modal = document.getElementById('modal-status');
    retry_cash.hide();

    modal.style.display = "block";
}

function CloseModalStatus() {
    var change_label = $('#order-change-label');
    var change = $('#order-change');
    var change_display = $('#change-display');
    var retry_cash = $('#status-retry-cash-button');
    var modal = document.getElementById('modal-status');

    change.val(0);
    change.hide();
    change_label.hide();
    change_display.text("Сдача...");
    change_display.hide();
    retry_cash.hide();

    modal.style.display = "none";
}

function CalculateTotal() {
    total = 0;
    for (var i = 0; i < currOrder.length; i++) {
        total += currOrder[i]['price'] * currOrder[i]['quantity'];
    }
    $('p.totalDisplay').each(function () {
        try {
            setPriceUnderMap()
        } catch (e) {
        }
        let res = Number(total.toFixed(2))
        $(this).text(res);
    });
}

function CalculateChange() {
    var cash_input = $('#order-change');
    var change_display = $('#change-display');
    var change = parseFloat((cash_input.val()).replace(/,/g, '.')) - total;
    change_display.text('Сдача ' + change + ' р.');
}

function ChangeCategory(category) {
    $('.menu-item').hide();
    $('[category=' + category + ']').show();
}

function ShowDialog(Text) {
    var promptbox = document.createElement('div');
    promptbox.setAttribute('id', 'promptbox');
    promptbox.setAttribute('class', 'promptbox');
    promptbox.innerHTML = '<input class="note-input" id="note-input"/>';
    promptbox.innerHTML = '<button class="note-OK" id="note-OK"/>';
    promptbox.innerHTML = '<button class="note-Cancel" id="note-Cancel"/>';
    $('#note-OK').onclick();
    $('#note-Cancel').onclick();
    $('#note-input').val(Text);
}

function SearchSuggestion(id) {
    var input = $('#note-' + id);
    var input_pos = input.position();
    var old_html = (input.parent()).html();
    var html_st = '<div id="dropdown-list"> sdf</div>';
    (input.parent()).html(old_html + html_st);
    $('#dropdown-list').css({
        left: input_pos.left,
        top: input_pos.top + input.height(),
        position: 'absolute',
        width: input.width()
    });
}

function ss(index, id) {
//     var input = $('#note-' + index);
//     var input_pos = input.position();
//     var searchTerm = $('#note-' + index).val();
    var input = $('#item-note');
    var input_pos = input.position();
    var searchTerm = $('#item-note').val();
    currOrder[index]['note'] = searchTerm;
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken)
        }
    });
    $.ajax({
            type: 'POST',
            url: $('#menu-urls').attr('data-search-comment'),
            data: {
                "id": index,
                "note": searchTerm
            },
            dataType: 'json',
            success: function (data) {
                $('#dropdown-list-container').html(data['html']);
                var dropdown_list = $('#dropdown-list');
                var is_visible = isScrolledIntoView(dropdown_list);

                dropdown_list.css({
                    left: input_pos.left,
                    top: is_visible ? input_pos.top + input.height() - 10 : input_pos.top - dropdown_list.height() - input.height() - 25,
                    position: 'absolute'
                });
                dropdown_list.append('<div id="close-cross">x</div>');
                $('#close-cross').css({
                    left: dropdown_list.width() + 10,
                    top: 5,
                    position: 'absolute',
                    cursor: 'pointer'
                });
                $('#close-cross').click(function () {
                    $('#dropdown-list').remove();
                });
            }
        }
    ).fail(function (jqXHR, textStatus) {
        alert('Необработанное искюение!' + textStatus);
        console.log(jqXHR + ' ' + textStatus);
    });


    $('.live-search-list li').each(function () {

        if ($(this).filter('[data-search-term *= ' + searchTerm + ']').length > 0 || searchTerm.length < 1) {
            $(this).show();
        } else {
            $(this).hide();
        }

    });
}

function isScrolledIntoView(elem) {
    var $elem = $(elem);
    var $window = $(window);

    var docViewTop = window.scrollY;
    var docViewBottom = docViewTop + window.innerHeight;

    var elemTop = $elem.offset().top;
    var elemBottom = elemTop + $elem.height();

    return ((elemBottom <= docViewBottom) && (elemTop >= docViewTop));
}

// let inputing = false;

// function addSymbolInQR(index, qr) {
//     console.log(index)
//     console.log(qr)
//     inputing = true;
//
//     setTimeout(checkInputing, 2000);
//     function checkInputing() {
//         if (inputing) {
//             qr.val(rus_to_latin(qr.val()))
//         } else {
//             inputing = false;
//         }
//
//         // if (qr.val().length === 37) {
//         //     qr.val(qr.val() + '☯');
//         //     currOrder[index]['qr'] = qr.val();
//         // } else if (qr.val().length > 37) {
//         //     if (qr.val().length - qr.val().lastIndexOf('☯') === 38) {
//         //         qr.val(qr.val() + '☯');
//         //         currOrder[index]['qr'] = qr.val();
//         //     }
//         // }
//     }
//
// }

function rus_to_latin (str) {
    var ru = {
        'й': 'q', 'ц': 'w', 'у': 'e', 'к': 'r', 'е': 't', 'н': 'y', 'г': 'u', 'ш': 'i', 'щ': 'o', 'з': 'p', 'х': '[', 'ъ': ']', 'ф': 'a', 'ы': 's', 'в': 'd', 'а': 'f', 'п': 'g', 'р': 'h', 'о': 'j', 'л': 'k', 'д': 'l', 'ж': ';', 'э': "'", 'я': 'z', 'ч': 'x', 'с': 'c', 'м': 'v', 'и': 'b', 'т': 'n', 'ь': 'm', 'б': ',', 'ю': '.', '.': '/',
        'Й': 'Q', 'Ц': 'W', 'У': 'E', 'К': 'R', 'Е': 'T', 'Н': 'Y', 'Г': 'U', 'Ш': 'I', 'Щ': 'O', 'З': 'P', 'Х': '[', 'Ъ': ']', 'Ф': 'A', 'Ы': 'S', 'В': 'D', 'А': 'F', 'П': 'G', 'Р': 'H', 'О': 'J', 'Л': 'K', 'Д': 'L', 'Ж': ';', 'Э': "'", 'Я': 'Z', 'Ч': 'X', 'С': 'C', 'М': 'V', 'И': 'B', 'Т': 'N', 'Ь': 'M', 'Б': ',', 'Ю': '.',

    }, n_str = [];

    for ( var i = 0; i < str.length; ++i ) {
        n_str.push(
            ru[ str[i] ]
            || ru[ str[i].toLowerCase() ] == undefined && str[i]
            || ru[ str[i].toLowerCase() ].replace(/^(.)/, function ( match ) { return match.toUpperCase() })
        );
    }
    return n_str.join('');
}