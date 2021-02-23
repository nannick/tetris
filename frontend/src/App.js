import logo from './logo.svg';
import './App.css';

import React, { useState, useEffect } from "react";
import io from "socket.io-client"


import { Provider } from 'react-redux'
import store from './store'
import Tetris from './components/Tetris';

const ENDPOINT = "http://localhost:5000";
const socket = io(ENDPOINT);
var game_id;

// https://dev.to/bravemaster619/how-to-use-socket-io-client-correctly-in-react-app-o65

const a = function(game_id){
  socket.emit('get_piece',{num_pieces : 1, game_id : game_id});
}

function App() {
  
    var [response, setResponse] = useState("");

    useEffect(() => {
      socket.emit('new_game',{num_rows : '11', num_columns : 9, difficulty : 1});

      socket.on("give_game_id", args =>{
       console.log(`Game id is ${args.game_id}`);
       game_id = args.game_id;
        socket.emit('get_piece',{num_pieces : 1, game_id : game_id});

      }); 

      socket.on('fail', args =>{

        console.log("Fail");
      });

      socket.on('give_piece', args =>{
        console.log(args);
      });
      

    }, []);
  
    return (
      <Provider store={store}>

     <Tetris numRows = {20} numColumns = {10}/>
     
      </Provider>
      

    );
}

export default App;
