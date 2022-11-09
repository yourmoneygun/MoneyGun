$(document).ready(function () {
    $('label').hide()
    $('br').hide()

    $('.helptext').hide()

    $('#id_username').attr('class', 'form_input').attr('placeholder', 'Электронная почта');
    $('#id_password').attr('class', 'form_input').attr('placeholder', 'Пароль');

    $('#id_email').attr('class', 'form_input').attr('placeholder', '* Электронная почта');
    $('#id_password1').attr('class', 'form_input').attr('placeholder', '* Пароль');
    $('#id_password2').attr('class', 'form_input').attr('placeholder', '* Повторить пароль');
    $('#id_referral_link_main_user').attr('class', 'form_input').attr('placeholder', 'Реферальный код');

    $('#id_old_password').attr('class', 'form_input').attr('placeholder', 'Старый пароль');
    $('#id_new_password1').attr('class', 'form_input').attr('placeholder', 'Новый пароль');
    $('#id_new_password2').attr('class', 'form_input').attr('placeholder', 'Повторить пароль');

    $('#id_wallet').attr('class', 'form_input').attr('placeholder', '* Номер кошелька');
    $('#id_money').attr('class', 'form_input').attr('placeholder', '* Сумма USDT');

    $('.errorlist li').each(function() {
    if ( $(this).text() === 'User с таким Email уже существует.' ) {
            $(this).text('Электронный адрес уже существует.')
        }
    });
});
