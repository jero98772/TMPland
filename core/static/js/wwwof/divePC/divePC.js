let pc ;

function setup() {
	canvas = createCanvas(800,500) ;
	pc = new divePC();
}

function draw() {
	var time = 200
	background(150);
	var setup = pc.stepsetup();
	canvas.position(setup.x+250,(setup.y+250),'relative');
	pc.moves();	

	pc.liquid()
	//dont move draws 
	pc.arrow();
	pc.board();


}
