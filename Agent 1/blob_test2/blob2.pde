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
    stroke(0);
    fill(255);
    strokeWeight(2);
    rectMode(CORNERS);
    rect(minx,miny,maxx,maxy);
    
    float cx = (minx + maxx) / 2;
    float cy = (miny + maxy) / 2;
    println("center2:"+ cx + cy);
    println("rect size2:" + size());
    //fill(0);
    //ellipse(cx,cy,1,1);
    textSize(32);
    fill(findColor2);
    text("Agent2", cx,cy); 
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
