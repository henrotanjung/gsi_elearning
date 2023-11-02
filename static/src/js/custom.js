"use strict"

function onchangePekerjaan() {
    let pekerjaanElem = document.getElementById("pekerjaan");
    let pekerjaanLainnya = document.getElementById("pekerjaan_lainnya");
    if (pekerjaanElem.value === 'pekerjaan_lainnya') {
        pekerjaanLainnya.style.display = 'block';
    }
    if (pekerjaanElem.value !== 'pekerjaan_lainnya') {
        pekerjaanLainnya.style.display = 'none';
    }
}

function onchangeReff() {
    let reffElem = document.getElementById("referensi");
    let reffLainnya = document.getElementById("referensi_lainnya");
    if (reffElem.value === 'referensi_lainnya') {
        reffLainnya.style.display = 'block';
    }
    if (reffElem.value !== 'referensi_lainnya') {
        reffLainnya.style.display = 'none';
    }
}

function checkUrl() {
    let url = window.location.href;
    if (url.includes('web/login')) {
        let loginEl = document.getElementsByClassName("login");
        let signupEl = document.getElementsByClassName("signup");
        loginEl[0].style.color = "#0080BB";
        signupEl[0].style.color = "#cdd5d8";
    } else if (url.includes('web/signup')) {
        let loginEl = document.getElementsByClassName("login");
        let signupEl = document.getElementsByClassName("signup");
        loginEl[0].style.color = "#cdd5d8";
        signupEl[0].style.color = "#0080BB";
    }
}
checkUrl();

function submitCheck() {
    var nama = document.getElementById('name');
    var phone = document.getElementById('phone');
    var login = document.getElementsByName('login');
    var signup_footer = document.getElementById('signup_footer');
    var alert_hp = document.getElementById('alert_hp');
    var alert_nama = document.getElementById('alert_nama');
    var alert_email = document.getElementById('alert_email');
    var numb_alert = 0;
    if (phone.value == '') {
        numb_alert += 1;
        alert_hp.style.display = 'block';
    } else {
        alert_hp.style.display = 'none';
    }
    if (nama.value == '') {
        numb_alert += 1;
        alert_nama.style.display = 'block'
    } else {
        numb_alert += 1;
        alert_nama.style.display = 'none';
    }
    console.log(login[0].value);
    if (login[0].value == '') {
        numb_alert += 1;
        alert_email.style.display = 'block'
    } else {
        alert_email.style.display = 'none';
    }
    if (numb_alert > 0) {
        signup_footer.style.marginTop = 620;
    }
}
window.onload = function() {
    var selItem = sessionStorage.getItem("SelItem");
    var referensi_lainnya = sessionStorage.getItem("referensi_lainnya");
    var pekerjaan = sessionStorage.getItem("pekerjaan");
    var pekerjaan_lainnya = sessionStorage.getItem("pekerjaan_lainnya");
    var title_field = sessionStorage.getItem("title_field");
    $('#referensi').val(selItem);
    $('#referensi_lainnya').val(referensi_lainnya);
    $('#pekerjaan').val(pekerjaan);
    $('#pekerjaan_lainnya').val(pekerjaan_lainnya);
    if (title_field != null) {
        $('#title_field').val(title_field);
    }
    let reffLainnya = document.getElementById("referensi_lainnya");
    let pekerjaanLainnya = document.getElementById("pekerjaan_lainnya");
    if (sessionStorage.getItem("SelItem") === 'referensi_lainnya') {
        reffLainnya.style.display = 'block';
    }
    if (sessionStorage.getItem("pekerjaan") === 'pekerjaan_lainnya') {
        pekerjaanLainnya.style.display = 'block';
    }
}
$('#referensi').change(function() {
    var selVal = $(this).val();
    sessionStorage.setItem("SelItem", selVal);
});
$('#referensi_lainnya').change(function() {
    var referensiLainnyaVal = $(this).val();
    sessionStorage.setItem("referensi_lainnya", referensiLainnyaVal);
});
$('#pekerjaan').change(function() {
    var pekerjaanVal = $(this).val();
    sessionStorage.setItem("pekerjaan", pekerjaanVal);
});
$('#pekerjaan_lainnya').change(function() {
    var pekerjaanLainnyaVal = $(this).val();
    sessionStorage.setItem("pekerjaan_lainnya", pekerjaanLainnyaVal);
});
$('#title_field').change(function() {
    var titleFieldVal = $(this).val();
    sessionStorage.setItem("title_field", titleFieldVal);
});