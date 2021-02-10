const express = require('express')
const cors = require('cors')
const constants = require("./constants");

const app = express();

// Allow all cors requests temporarily to work with POstman
app.use(cors());
app.use(express.json({extended: false}))

const PORT = process.env.PORT || constants.SERVER.DEFAULT_PORT;



app.get('/', (req, res) => {
    res.send('Api running');
});

const socketIo = require("socket.io");
const http = require("http");
const server = http.createServer(app);

// Allow cors for socket.io
const io = socketIo(server,  {cors: {
    origin: '*',
  }} );

const game_io = require('./game')(io);




server.listen(PORT, () => {
    console.log(`Server started on port ${PORT}`);
});

