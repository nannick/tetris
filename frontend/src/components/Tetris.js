
import React, {Fragment} from 'react';
import Board  from './Board';
import Colour from '../colour';
class Tetris extends React.Component {

    constructor(props) {
        super(props);

        this.timeId = "";

        this.numRows = props.numRows;
        this.numColumns = props.numColumns;
        
        this.pieceQueue  = [];
        this.getPieces(2);
        
        this.state={
            current_rotation_point : {x : props.numColumns >> 1 , y: props.numRows -1},
            current_piece : this.pieceQueue.shift(),
            board : this.createEmptyBoard(props.numRows, props.numColumns)
        }

        window.addEventListener('keydown', (event) => {
          console.log(event);
          if (event.key == 'ArrowRight'){
            this.movePieceSide(1);

          }
          else if (event.key == 'ArrowLeft'){
            this.movePieceSide(-1);

          }
          else if (event.key == 'ArrowDown'){
            this.movePieceDown();
          }
        });
      
    }


    createEmptyRow(numColumns){
        var row = []
        for(var i = 0; i < numColumns; i ++){
            row.push(Colour.empty);
        }
        return row;
    }
    createEmptyBoard(numRows, numColumns){
        var board = new Array(numRows)
        for (var i = 0; i < numRows; i++) {
            board[i] = this.createEmptyRow(numColumns);
          }
        return board;
    }

    spinPiece(){

    }

    movePieceDown(){
      const nextPosition = {
        x : this.state.current_rotation_point.x,
        y : this.state.current_rotation_point.y - 1
      }
      if (!this.checkCollision(nextPosition)){
        
        this.setState({
          ...this.state, 
          current_rotation_point : nextPosition
        });
        
      }
      else{
        //Piece is stuck on board, so draw it permanently on 
        this.drawPiece(this.state.current_rotation_point, this.state.current_piece.colour);


        //Erase any full rows
        this.eraseLines();

        // Get another piece, move to next piece and update the rotation point
        this.getPieces(1);
        this.setState({
          ...this.state,
          current_rotation_point : {
            x : this.numColumns >> 1 , 
            y: this.numRows - 1
          }, 
          current_piece : this.pieceQueue.shift()
        });

      }
    }

    movePieceSide(dir){
      const nextPosition = {
        x : this.state.current_rotation_point.x + dir,
        y : this.state.current_rotation_point.y
      }

      if (!this.checkCollision(nextPosition)){
        this.setState({
          ...this.state, 
          current_rotation_point : nextPosition
        });
      }
    }

    checkYBounds(y_val){
      return y_val >= 0 && y_val < this.numRows;
    }
    checkXBounds(x_val){
      return x_val >= 0 && x_val < this.numColumns;
    }

    checkCollision(nextPosition){
      const  currX = nextPosition.x;
      const  currY = nextPosition.y;
      const num_parts = this.state.current_piece.parts.length;
 
      for (var i = 0; i < num_parts; i++){
        const  xShift = this.state.current_piece.parts[i].x;
        const  yShift = this.state.current_piece.parts[i].y;
        const newX = currX+xShift;
        const newY = currY+yShift;
        if (this.checkYBounds(newY) && this.checkXBounds(newX)){
          if(this.state.board[newY][newX] != Colour.empty ){
            return true;
          } 
        }
        else {
          return true;
        }      
      }
      return false;
    }

    drawPiece(pos,colour){
      const {x : current_x, y: current_y} = pos;
      this.state.current_piece.parts.forEach((shift) => {
        const {x : shift_x, y: shift_y} = shift;
        const newX = current_x + shift_x;
        const newY = current_y + shift_y;
        this.state.board[newY][newX] = colour;
      }
      );
    }

    eraseLines(){
      console.log("Erase lines func");
    }

    // TODO make call to backend to get pieces. Right now used fixed pieces
    getPieces(num_pieces){
      for (var i = 0; i < num_pieces; i++){
        this.pieceQueue.push({
          parts : [
            {
              x : 0,
              y : 0
            },
            {
              x : -1,
              y : 0
            }
        ],
          colour : Colour.piece_colours[0]
      });
      }
    }


    componentDidMount() {
        this.timeId = setInterval(
          () => {
            this.movePieceDown();
            },
          1000
        );
    }
    
    componentWillUnmount() {
        clearInterval(this.timeId);
    }

    render() {

      return (
      <div>
          <h1>
              Tetris Game
          </h1>
          
            <Board numRows= {this.numRows} numColumns= {this.numColumns} pixelSize= {15} cells ={this.state.board} piece = {this.state.current_piece} rotationPoint ={this.state.current_rotation_point} ></Board>
            
          
       
        




      </div>

      );
    }
}


export default Tetris;