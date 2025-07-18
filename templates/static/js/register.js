document.addEventListener('DOMContentLoaded', () => {
  const form = document.querySelector('form');
  const button = document.querySelector('.button-sign-up');
  const password = document.querySelector('#password');
  const confirm = document.querySelector('#confirmPassword');
  const agree = document.querySelector('#agree');

  function validateConfirmPassword() {
    confirm.setCustomValidity(
      confirm.value === password.value ? '' : 'Passwords do not match'
    );
  }

  function updateButtonState() {
    validateConfirmPassword(); // always keep it synced
    if (form.checkValidity() && agree.checked) {
      button.disabled = false;
    } else {
      button.disabled = true;
    }
  }

  // Prevent submission if form is invalid (just in case)
  form.addEventListener('submit', (event) => {
    if (!form.checkValidity()) {
      event.preventDefault();
      event.stopPropagation();
    }
  });

  password.addEventListener('input', updateButtonState);
  confirm.addEventListener('input', updateButtonState);
  agree.addEventListener('change', updateButtonState);
  form.addEventListener('input', updateButtonState);
});