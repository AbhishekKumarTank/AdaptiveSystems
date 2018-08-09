function removeFromArray (arr, elt){
  for(var i = arr.length -1; i >= 0;i--){
    if(arr[i] == elt){
      arr.splice(i,1);
    }
  }
}

function heuristic(a,b){
  var d = abs(a.i-b.i)+abs(a.j-b.j);
  return d;
}

var cols = 3;
var rows = 3;
var grid = new Array(cols);
var openSet = [];
var closedSet = [];
var start;
var end;
var w,h;
var path = [];
var directions = [];
var dir = "N";

function Spot(i,j){
  this.i = i;
  this.j = j;
  this.f = 0;
  this.g = 0;
  this.h = 0;
  this.neighbors = [];
  this.previous = undefined;

  this.show = function(col){
    fill(col);
    noStroke();
    rect(this.i * w,this.j*h,w-1,h-1);

  }

  this.addneighbors = function(grid){
    var i = this.i;
    var j = this.j;
    if (i < cols -1){
      this.neighbors.push(grid[i+1][j]);
    }
    if (i > 0){
      this.neighbors.push(grid[i-1][j]);
    }
    if (j < rows -1){
      this.neighbors.push(grid[i][j+1]);
    }
    if (j > 0){
      this.neighbors.push(grid[i][j-1]);
    }
  }
}

function setup(){
  createCanvas(400,400);
  console.log('A*');
  w = width/cols;
  h = height/rows;

for(var i = 0; i < cols; i++){
  grid[i] = new Array (rows);
}

  for (var i = 0; i< cols; i++){
    for (var j = 0; j< rows; j++){
    grid[i][j] = new Spot(i, j);
  }
}
for (var i = 0; i< cols; i++){
  for (var j = 0; j< rows; j++){
  grid[i][j].addneighbors(grid);
}
}
  start = grid [1][2];
  end = grid [2][0];
  openSet.push(start);

  console.log(grid);
}

function draw(){
  if (openSet.length > 0){
    var winner = 0;
    for(var i = 0; i < openSet.length; i++){
      if(openSet[i].f < openSet[winner].f){
        winner = i;
      }
    }
    var current = openSet[winner];

    if (current == end) {
      path = [];
      var temp = current;
      path.push(temp);
      while (temp.previous){
        //console.log(temp.i, temp.j);
        path.push(temp.previous);
        temp = temp.previous;

      }

      console.log("Done!");
      for(var i = path.length -1; i >= 1; i--){
        //console.log(path[i].i,path[i].j,);
       var x1 = path[i].i;
       var y1 = path[i].j;
       var x2 = path[i-1].i;
       var y2 = path[i-1].j;
        if (dir == "N"){
          if(x2== x1){
            //console.log("straight");
            directions.push("straight");
            dir = "N";
          }
          else if(x2>x1){
            //console.log("right");
            directions.push("right");
            dir = "E";
          }
          else if(x2<x1){
            //console.log("left");
            directions.push("left");
            dir = "W";
          }
        }
        else if (dir == "S"){
          if(x2== x1){
            //console.log("straight");
            directions.push("straight");
            dir = "S";
          }
          else if(x2>x1){
            //console.log("left");
            directions.push("left");
            dir = "E";
          }
          else if(x2<x1){
            //console.log("right");
            directions.push("right");
            dir = "W";
          }
        }
        else if (dir == "W"){
          if(y2== y1){
            //console.log("straight");
            directions.push("straight");
            dir = "W";
          }
          else if(y2>y1){
            //console.log("left");
            directions.push("left");
            dir = "S";
          }
          else if(y2<y1){
            //console.log("right");
            directions.push("right");
            dir = "N";
          }
        }
        else if (dir == "E"){
          if(y2== y1){
            console.log("straight");
            directions.push("straight");
            dir = "E";
          }
          else if(y2>y1){
            console.log("right");
            directions.push("right");
            dir = "S";
          }
          else if(y2<y1){
            console.log("left");
            directions.push("left");
            dir = "N";
          }
        }


      }
      console.log(directions);

    }
    removeFromArray(openSet, current);
    closedSet.push(current);

    var neighbors = current.neighbors;
    for(var i = 0; i < neighbors.length; i++){
      var neighbor = neighbors[i];

      if(!closedSet.includes(neighbor)){
        var tempG = current.g + 1;

        if (openSet.includes(neighbor)){
          if(tempG < neighbor.g) {
            neighbor.g = tempG;
          }
        }
        else{
          neighbor.g = tempG;
          openSet.push(neighbor);
        }
        neighbor.h = heuristic(neighbor, end);
        neighbor.f = neighbor.g + neighbor.h;
        neighbor.previous = current;

      }

    }

  } else {

  }
  background(0);

  for (var i = 0; i < cols; i++){
    for (var j = 0; j < rows; j++){
      grid[i][j].show(color(255));
    }
  }

  for (var i = 0; i < closedSet.length; i++){
    closedSet[i].show(color(255,0,0));
  }
  for (var i = 0; i < openSet.length; i++){
    openSet[i].show(color(0,255,0));
  }
  for (var i = 0; i < path.length; i++){
    path[i].show(color(0,0,255));
  }

}
