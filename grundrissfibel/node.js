const express = require('express');
const app = express();
const PORT = 3000;

const grundrisse = [
    { id: 1, imagePath: '/images/grundriss1.jpg', typology: 'zentral', form: 'rechteckig', size: 75 },
    { id: 2, imagePath: '/images/grundriss2.jpg', typology: 'seitlich', form: 'L-förmig', size: 120 },
    // Weitere Einträge...
];

app.use(express.json());

app.post('/api/grundrisse', (req, res) => {
    const { typology, form, sizeMin, sizeMax } = req.body;
    const filtered = grundrisse.filter(g => 
        (!typology || g.typology === typology) &&
        (!form || g.form === form) &&
        g.size >= sizeMin &&
        g.size <= sizeMax
    );
    res.json(filtered);
});

app.listen(PORT, () => console.log(`Server läuft auf http://localhost:${PORT}`));
