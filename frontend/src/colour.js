








module.exports = {
    empty : "#000000",
    white : "#FFFFFF",
    piece_colours : [
        "#7FFFD4",
        "#D2691E",
        "#DC143C"
    ],
    random_colour : function() {
        return  '#' + Math.floor(Math.random()*16777215).toString(16);
    }

}