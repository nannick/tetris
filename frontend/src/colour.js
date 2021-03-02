


const OPTIONS = [
    "#7FFFD4",
    "#D2691E",
    "#DC143C",
    "#00FFFF",
    "#7FFFD4",
    "#8A2BE2",
    "#7FFF00",
    "#8FBC8F",
    "#FF69B4"
];


module.exports = {
    empty : "#000000",
    white : "#FFFFFF",
    random_colour : function() {
        const cIndex =  Math.floor(Math.random()*OPTIONS.length);
        return  OPTIONS[cIndex];
    }

}