document.addEventListener('DOMContentLoaded', () => {
  const form = document.querySelector('form');
  const button = document.querySelector('.button-sign-in');

  // Initially disable the button
  button.disabled = true;

  form.addEventListener('input', () => {
    if (form.checkValidity()) {
      button.disabled = false;
    } else {
      button.disabled = true;
    }
  });
});