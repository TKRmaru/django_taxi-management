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

//DataInputViewにてride_type='賃走'の場合のみcustomer_name, fare, checkboxを表示
document.addEventListener('DOMContentLoaded', function() {
    var rideTypeField = document.getElementById('id_ride_type');
    var customerNameWrapper = document.getElementById('customer_name_wrapper');
    var fareWrapper = document.getElementById('fare_wrapper');
    var checkboxWrapper = document.getElementById('checkbox_wrapper');

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
    rideTypeField.addEventListener('change', toggleInputField);
    toggleInputField();
});

