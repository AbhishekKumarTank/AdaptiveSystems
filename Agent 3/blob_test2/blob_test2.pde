import processing.net.*;
Client myClient;

/**
 *  Please note that the code for interfacing with Capture devices
 *  will change in future releases of this library. This is just a
 *  filler till something more permanent becomes available.
 *
 *  For use with the Raspberry Pi camera, make sure the camera is
 *  enabled in the Raspberry Pi Configuration tool and add the line
 *  "bcm2835_v4l2" (without quotation marks) to the file
 *  /etc/modules. After a restart you should be able to see the
 *  camera device as /dev/video0.
 */
//import processing.video.*;
import gohai.glvideo.*;
GLCapture video;

color findColor1;
color findColor2;
color findColor3;
float threshold = 15;
float distThreshold = 100;
float size=500;
int findColorID=-1;

ArrayList<Blob1> blobs1 = new ArrayList<Blob1>();
ArrayList<Blob2> blobs2 = new ArrayList<Blob2>();
ArrayList<Blob3> blobs3 = new ArrayList<Blob3>();

void setup() {
  //size(640, 480);
  size(320,240,P2D);
  noStroke();
  // this will use the first recognized camera
  String[] devices =GLCapture.list();
  video = new GLCapture(this, devices[0],width, height);
  video.start();
  findColor1 = -9961451;//Agent 1
  findColor2 = -6955132;//Agent 2, not calibrate yet
  findColor3 = -6955132;//Agent 4, not calibrate yet
  smooth();
  myClient = new Client(this,"192.168.1.253",5204);//self(Agent 3) ip

}

//for color calibration
void keyPressed() {
  if (key == 'a') {
    distThreshold++;
  } else if (key == 'z') {
    distThreshold--;
  }
  println(distThreshold);
  
  if (key == '1') {
    findColorID = 1;   
  } 
    else if (key == '2') {
    findColorID = 2;    
  } 
    else if (key == '4') {
    findColorID= 3;    
  } 
}

void draw() {
  background(0);
  if (video.available()) {
    video.read();
  }
  video.loadPixels();
  image(video, 0, 0, width, height);
  
  blobs1.clear();
  blobs2.clear();
  blobs3.clear();
  
  //float difference = 300;
  //int minX = 0;
  //int minY = 0;
  
  for(int x=0; x<video.width; x++){
    for(int y=0; y<video.height; y++){
      int loc = x + y*video.width;
      color videoColor = video.pixels[loc];
      float r = (videoColor >> 16) & 0xFF;
      float g = (videoColor >> 8) & 0xFF;
      float b = videoColor & 0xFF;
      float r1 = (findColor1 >> 16) & 0xFF;
      float g1 = (findColor1 >> 8) & 0xFF;
      float b1 = findColor1 & 0xFF;
      float r2 = (findColor2 >> 16) & 0xFF;
      float g2 = (findColor2 >> 8) & 0xFF;
      float b2 = findColor2 & 0xFF;
      float r3 = (findColor3 >> 16) & 0xFF;
      float g3 = (findColor3 >> 8) & 0xFF;
      float b3 = findColor3 & 0xFF;
      
      float d1 = dist(r, g, b, r1, g1, b1);
      float d2 = dist(r, g, b, r2, g2, b2);
      float d3 = dist(r, g, b, r3, g3, b3);
      
      if (d1<threshold){
        boolean found = false;
        for(Blob1 blob1: blobs1){
          if(blob1.isNear(x,y)){
          blob1.add(x,y);
          found = true;
          break;
          }
        }
        
        if(!found){
        Blob1 blob1= new Blob1(x,y);
        blobs1.add(blob1);
        }
    
      }
      if (d2<threshold){
        boolean found = false;
        for(Blob2 blob2: blobs2){
          if(blob2.isNear(x,y)){
          blob2.add(x,y);
          found = true;
          break;
          }
        }
        
        if(!found){
        Blob2 blob2= new Blob2(x,y);
        blobs2.add(blob2);
        }
    
      }
      if (d3<threshold){
        boolean found = false;
        for(Blob3 blob3: blobs3){
          if(blob3.isNear(x,y)){
          blob3.add(x,y);
          found = true;
          break;
          }
        }
        
        if(!found){
        Blob3 blob3= new Blob3(x,y);
        blobs3.add(blob3);
        }
    
      }
    }
  }

 int i = 0; 
  for (Blob1 b: blobs1){
    if(b.size()>size){
      if(i == 0){
    b.show(i);
    i++;
      }
    }
  } 
//for (Blob1 b: blobs1){
//  blobs1.get(0).show();

//}

for (Blob2 b: blobs2){
  blobs2.get(0).show();
}

for (Blob3 b: blobs3){
  blobs3.get(0).show();
}
// if (difference <threshold){
//    fill(findColor);
//    strokeWeight(2.0);
//    stroke(255);
//    rectMode(CENTER);
//    rect(minX,minY,60,60);
//  }
}

void mousePressed(){
  if(findColorID ==1){
    int loc =mouseX + mouseY*video.width;
    findColor1 = video.pixels[loc];
    println("color:" + findColor1);
  }
   else if(findColorID ==2){
    int loc =mouseX + mouseY*video.width;
    findColor2 = video.pixels[loc];
    println("color:" + findColor2);
  }
    else if(findColorID ==3){
    int loc =mouseX + mouseY*video.width;
    findColor3 = video.pixels[loc];
    println("color:" + findColor3);
  }
  
}
