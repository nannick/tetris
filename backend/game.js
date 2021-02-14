
const Validator = require('validatorjs');
const { v4: uuidv4 } = require('uuid');

const CONSTANTS = require("./constants");
const GAME = CONSTANTS.GAME;
const DIFFICULTY = CONSTANTS.DIFFICULTY;
const SOCKET = CONSTANTS.SOCKET;

let NEW_GAME_RULES = {
    num_rows : ['required', 'integer', {max : GAME.MAX_ROW_NUM, min : GAME.MIN_ROW_NUM}],
    num_columns : ['required','integer',{max : GAME.MAX_COLUMN_NUM, min : GAME.MIN_COLUMN_NUM}],
    difficulty : ['required','integer',{max : DIFFICULTY.MAX, min : DIFFICULTY.MIN}]
}

let GET_PIECE_RULES = {
    num_pieces : ['required', 'integer', {max : GAME.MAX_BLOCKS, min : GAME.MIN_BLOCKS}],
    game_id : ['required']
}

let CLOSE_GAME_RULES = {
    game_id : ['required']
}

var games = {};

const add_game = function(game_id, num_rows, num_columns, difficulty){
    const new_game = {
        num_rows,
        num_columns,
        difficulty
    };
    games[game_id] = new_game;
};
const get_pieces = function(num_pieces, difficulty){
    return {pieces : new Array(num_pieces)};
}


module.exports= function(io){
io.on('connection', (socket) => {
    console.log(`New connection ${socket.id}`);

    socket.on("client",p => {
        console.log(p);
    });

    socket.on(SOCKET.NEW_GAME,args=>{
        let v = new Validator(args,NEW_GAME_RULES);
        if (v.passes() ){
            const {num_rows, num_columns, difficulty} = args;

            const game_id = socket.id;
            add_game(game_id,num_columns, num_rows,difficulty);
            io.to(socket.id).emit(SOCKET.GIVE_GAME_ID,{game_id});
        }
        else{
            io.to(socket.id).emit(SOCKET.FAIL);
        }
    });

    socket.on(SOCKET.CLOSE_GAME,args=>{
        let v = new Validator(args,CLOSE_GAME_RULES);
        if (v.passes()){
            const {game_id} = args;
            if (game_id in games){
                games.delete(game_id);
            }
        }
    });

    socket.on(SOCKET.GET_PIECE,args=>{
        var fail = true;
        let v = new Validator(args,GET_PIECE_RULES);

        if (v.passes()){
            
            const {game_id, num_pieces} = args;
            if (game_id in games){
                fail = false;
                const pieces = get_pieces(num_pieces,games[game_id].difficulty);
                io.to(socket.id).emit(SOCKET.GIVE_PIECE,pieces);
            }
        }
        if (fail){
            io.to(socket.id).emit(SOCKET.FAIL);
        }
    });

});
}