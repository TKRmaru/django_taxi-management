const btn = document.querySelector('.btn-menu');
const nav = document.querySelector('.main-nav');

btn.addEventListener('click', () => {
  nav.classList.toggle('open-menu');
  if (btn.innerHTML === 'MENU') {
    btn.innerHTML = 'CLOSE';
  } else {
    btn.innerHTML = 'MENU';
  }
});

//DataInputView
document.addEventListener('DOMContentLoaded', function() {
    var rideTypeField = document.getElementById('id_ride_type');
    var customerNameWrapper = document.getElementById('customer_name_wrapper');
    var fareWrapper = document.getElementById('fare_wrapper');
    var fare = document.getElementById('id_fare');
    var checkboxWrapper = document.getElementById('checkbox_wrapper');
    var carField = document.getElementById('id_car');
    var mileageFromField = document.getElementById('id_mileage_from');
    var mileageToField = document.getElementById('id_mileage_to');

//ride_type='賃走'の場合のみcustomer_name, fare, checkboxを表示
    function toggleInputField() {
        if (rideTypeField.value === '賃走') {
            customerNameWrapper.style.display = 'block';
            fareWrapper.style.display = 'block';
            checkboxWrapper.style.display = 'flex';
        } else {
            customerNameWrapper.style.display = 'none';
            fareWrapper.style.display = 'none';
            checkboxWrapper.style.display = 'none';
        }
    }

//mileage情報を取得
    function updateMileageFrom() {
        var carId = carField.value;
        if (carId !== '') {
            fetch('/myapp/get_car_mileage/' + carId + '/')
                .then(response => response.json())
                .then(data => {
                    mileageFromField.value = data.car_mileage;
                    mileageToField.value = data.car_mileage;
                });
        } else {
            mileageFromField.value = '';
            mileageToField.value = '';
        }
    }

//エラーメッセージを表示
    var mileageError = document.getElementById('mileage-error');
    var fareError = document.getElementById('fare-error');
    var form = document.querySelector('form');

    form.addEventListener('submit', function(event) {
        if (mileageFromField.value === mileageToField.value) {
            event.preventDefault(); // mileage_fromとmileage_toが同じ場合は送信をキャンセル
            mileageError.style.display = 'block';
        } else {
            mileageError.style.display = 'none'
        }

        if(rideTypeField.value === '賃走'){
            if(!fare.value){
                event.preventDefault(); // fareが空欄の場合は送信をキャンセル
                fareError.style.display = 'block';
            }else{
                fareError.style.display = 'none'}
        }else{
            fareError.style.display = 'none'
        }
    });

    rideTypeField.addEventListener('change', toggleInputField);
    carField.addEventListener('change', updateMileageFrom);
    toggleInputField();
    updateMileageFrom();
});
