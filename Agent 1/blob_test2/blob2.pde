class Blob2{
  float minx;
  float miny;
  float maxx;
  float maxy;
  ArrayList<PVector> points;
  
  Blob2(float x, float y){
    minx = x;
    miny = y;
    maxx = x;
    maxy = y;
    points = new ArrayList<PVector>();
    points.add(new PVector(x,y));
  }
  
  void show(){
    stroke(findColor2);
    noFill();
    strokeWeight(2);
    rectMode(CORNERS);
    rect(minx, miny, maxx, maxy);

    //float cx = (minx + maxx) / 2;
    //float cy = (miny + maxy) / 2;
    //println("center1:"+ cx + cy);
    //println("rect size1:" + size());
    //fill(0);
    //ellipse(cx,cy,1,1);
    fill(findColor2);
    rectMode(CORNERS);
    rect(minx, miny-20, minx+70, miny);
    textSize(20);
    fill(0);
    text("Agent2", minx, miny); 
    fill(255);
    noStroke();
    rectMode(CORNERS);
    rect(0, 0, width, 20);
    textSize(14);
    fill(0);
    text("Communicating with Agent 2...", 20, 15);
    myClient.write("hello Agent 2");
    //for(PVector v: points){
    //  stroke(255,255,0);
    //  point(v.x, v.y);
    //  //println("dots:" + points.size());     
    //}
  }
  
  void add(float x, float y) {
    PVector v = new PVector(x,y);
    points.add(v);
    minx = min(minx, x);
    miny = min(miny, y);
    maxx = max(maxx, x);
    maxy = max(maxy, y);
  }
  float size() {
    return (maxx-minx)*(maxy-miny);
  }
  boolean isNear(float x, float y) {
    float cx = (minx + maxx) / 2;
    float cy = (miny + maxy) / 2;

    float d = dist(cx, cy, x, y);
    if (d < distThreshold) {
      return true;
    } else {
      return false;
    }
  }
}
