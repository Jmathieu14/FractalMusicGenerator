// inlets and outlets
inlets = 1;
outlets = 1;
// global variables
var ncols=4; // default columns
var nrows=4; // default rows
var vbrgb = [0.8,1.,0.8,0.5];
var vmrgb = [0.9,0.5,0.5,0.75];
var vfrgb = [1.,0.,0.2,1.];
// initialize state array
var state = new Array(8);
for(i=0;i<8;i++) 
{
state[i] = new Array(8);
for(j=0;j<64;j++) 
{
state[i][j] = 0;
}
}
// set up jsui defaults to 2d
sketch.default2d();
// initialize graphics
draw();
refresh();