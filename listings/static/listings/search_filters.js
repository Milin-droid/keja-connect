document.addEventListener('DOMContentLoaded', () => {
  const county = document.getElementById('county');
  const town = document.getElementById('town');
  const neighbourhood = document.getElementById('neighbourhood');

  if (!county || !town || !neighbourhood) return;

  const updateLocations = () => {
    for (const option of town.options) {
      option.hidden = Boolean(
        option.value && county.value && option.dataset.county !== county.value
      );
    }

    for (const option of neighbourhood.options) {
      option.hidden = Boolean(
        option.value && town.value && option.dataset.town !== town.value
      );
    }

    if (town.selectedOptions[0]?.hidden) town.value = '';
    if (neighbourhood.selectedOptions[0]?.hidden) neighbourhood.value = '';
  };

  county.addEventListener('change', () => {
    town.value = '';
    neighbourhood.value = '';
    updateLocations();
  });

  town.addEventListener('change', () => {
    neighbourhood.value = '';
    updateLocations();
  });

  updateLocations();
});
