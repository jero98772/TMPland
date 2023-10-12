let measure;
let size;
let posy;
let c;
let c2;
let pos;
let time;
let minisegundos=1000;
let arrowy
let liquidx
let liquidy
let liquidcolor
let tankwater;
let tankoil;
let tankpos;
let board;
//setTimeout(setInterval(draw()),5)
class divePC {

	stepsetup(){
		this.measure = new createVector(((windowWidth - width) / 2),( (windowHeight - height ) / 2));
		textSize(36);
		text('MOTHERBOARD in MINERALOIL', 10, 30);
		this.time = 5 ;
		//this.c2 = 'rgb(40,10,10)';
		return this.measure

	}	
	constructor() {
		this.arrowy
    	this.pos = new createVector(10, 10);
    	this.speed = new createVector(2.5, 0.5);
    	this.fishtankpos = new createVector(2.5, 1);
    	this.arrowy = 10
    	this.tankpos = new createVector(220,150);
    	this.tankwater = new createVector(500, 300);
    	this.tankoil = new createVector(500, 150);

		//this.posy = 0
  	}
	moves() {
		this.pos.y = this.pos.y + this.speed.y
		//this.pos.y = this.pos.y + this.speed 
		if ((this.pos.y > 50) || (this.pos.y > 125)) {
	      this.pos.y = 50
		console.log(this.pos.y)

	}
		this.arrowy = this.arrowy + this.speed.y
		if ((this.arrowy > height) || (this.arrowy > 125)) {
	      this.arrowy = 0
		console.log(this.arrowy)
	}
}
	arrow(){
		fill('rgb(0,100,0)');
		noStroke();
		rect(750,150,10,this.arrowy)
		translate(0,this.arrowy);
		triangle(745, 150, 755,200, 765,150);
		stroke(2);
}

	liquid(){
		fill('rgb(100,100,255)');
		this.fishtank = rect(this.tankpos.x,this.tankpos.y,this.tankwater.x,this.tankwater.y);
		fill(200);
		textSize(36);
		text("MINERALOIL",this.tankpos.x-220,this.tankpos.y+36);
		fill('rgb(200,200,255)');
		this.fishtank = rect(this.tankpos.x,this.tankpos.y,this.tankoil.x,this.tankoil.y );
		fill(200);
		textSize(36);
		text("water",this.tankpos.x-150,this.tankpos.y+236);
		//return l.x > this.x && l.x < this.x + this.w && l.y > this.y && l.y < this.y + this.h;
	}
	board() {
		fill(200);
		textSize(36);
		text("MOTHERBOARD",270,int(this.pos.y));
		fill(51);
		//this.animation = rect(200, int(this.pos*2), int(this.size.x/2), int(this.size.y/2));
		//this.board = loadImage("https://www.compulaptop.com/wp-content/uploads/2019/05/Board-Dell-Vostro-320-Parte-W099P-Ref-CLDV320-BOGOTA-COMPULAPTOP-1.jpg",)
		this.animation = rect(270, int(this.pos.y) ,400, 100);
		//this.animation = image(this.board,150, int(this.pos.y),300, 100);//rect(150, int(this.pos.y) ,300, 100);
		//rect(100, this.pos.y*2, this.size.x/2, this.size.y/2);
	}

}

