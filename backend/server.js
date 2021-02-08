const express = require('express')
const cors = require('cors')

const app = express();

// Allow all cors requests temporarily to work with POstman
app.use(cors());
app.use(express.json({extended: false}))


const DEFAULT_PORT = 5000;
const PORT = process.env.PORT || DEFAULT_PORT;

app.listen(PORT, () => {
    console.log(`Server started on port ${PORT}`);
});

app.get('/', (req, res) => {
    res.send('Api running');
});


