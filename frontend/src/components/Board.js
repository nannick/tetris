import React from 'react';

const  Board = function(props) {

    const {pixelSize, numRows, numColumns, piece, cells, rotationPoint} = props
        const height = pixelSize * (numRows);
        const width = pixelSize *  (numColumns);

        var boardContainer = []

        for(var rowNum = 0 ; rowNum < numRows; rowNum++){
            var yPosition = (numRows - rowNum - 1) * pixelSize;
            var row = []
            for(var columnNum =0; columnNum < numColumns; columnNum++){
                    var xPosition = columnNum * pixelSize;
                    row[columnNum] = <rect fill={cells[rowNum][columnNum]} x={xPosition} y={yPosition} width={pixelSize} height={pixelSize}></rect>;
            }
            boardContainer.push(row);
        }

        const {x : center_x, y: center_y} = rotationPoint;
        piece.parts.forEach(element => {
            const {x : relative_x, y: relative_y} = element;
            const yIndex = center_y + relative_y;
            const xIndex = center_x + relative_x;
            var yPosition = (numRows - yIndex - 1) * pixelSize;
            var xPosition = xIndex * pixelSize;
            boardContainer[yIndex][xIndex] = <rect fill={piece.colour} x={xPosition} y={yPosition} width={pixelSize} height={pixelSize}></rect>        
         });
        return (
            <svg width={width} height={height}>
                {boardContainer}
            </svg>
        );
    }

export default Board;