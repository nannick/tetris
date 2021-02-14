
const GAME = {
    MIN_COLUMN_NUM : 8,
    MAX_COLUMN_NUM :  10,
    MIN_ROW_NUM : 10,
    MAX_ROW_NUM : 20,
    MIN_BLOCKS : 1,
    MAX_BLOCKS : 3,
    MAX_GAMES : 1
};

const DIFFICULTY = {
    MIN : 0,
    MAX : 1,
}

const SERVER = {
    DEFAULT_PORT : 5000
}

const SOCKET = {
    NEW_GAME : "new_game",
    GIVE_GAME_ID : "give_game_id",
    CLOSE_GAME : "close_game",
    GET_PIECE : "get_piece",
    GIVE_PIECE : "give_piece",
    FAIL : "fail"
}


module.exports = Object.freeze({
    GAME,
    DIFFICULTY,
    SERVER,
    SOCKET
});