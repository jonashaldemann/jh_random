document.getElementById('apply-filters').addEventListener('click', () => {
    const typology = document.getElementById('typology-filter').value;
    const form = document.getElementById('form-filter').value;
    const sizeMin = parseFloat(document.getElementById('size-min').value) || 0;
    const sizeMax = parseFloat(document.getElementById('size-max').value) || Infinity;

    fetch('/api/grundrisse', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ typology, form, sizeMin, sizeMax })
    })
    .then(response => response.json())
    .then(data => {
        const resultsContainer = document.getElementById('results');
        resultsContainer.innerHTML = '';
        data.forEach(item => {
            const img = document.createElement('img');
            img.src = item.imagePath;
            img.alt = item.name;
            resultsContainer.appendChild(img);
        });
    });
});
