    const form = document.getElementById('estimatorForm');
    const resultBox = document.getElementById('resultBox');
    const resultText = document.getElementById('resultText');

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      const service = form.service.value;
      const area = parseFloat(form.area.value);

      // Dummy frontend-only estimate logic
      const baseRates = {
        architectural: 600000,
        interior: 500000,
        landscape: 400000,
        furniture: 300000,
        management: 250000
      };

      const estimate = baseRates[service] * area;
      resultText.textContent = `Rp ${estimate.toLocaleString('id-ID')} (estimated only)`;
      resultBox.style.display = 'block';
    });