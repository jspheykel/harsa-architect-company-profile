  document.addEventListener('DOMContentLoaded', () => {
    const flashMessages = document.querySelector('.flash-messages');
    if (flashMessages) {
      setTimeout(() => {
        flashMessages.style.display = 'none';
      }, 5000); // Hide after 5 seconds
    }
  });