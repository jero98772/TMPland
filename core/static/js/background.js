// Dynamic Fourier Series Wave Background
// Save this as: assets/js/fourier-waves.js

let waves = [];
let time = 0;
let particles = [];

function setup() {
  let canvas = createCanvas(windowWidth, windowHeight);
  canvas.parent('wave-container');
  canvas.style('display', 'block');
  canvas.style('position', 'fixed');
  canvas.style('top', '0');
  canvas.style('left', '0');
  canvas.style('z-index', '-1');
  
  // Create multiple dynamic Fourier series waves
  waves.push({
    freq: 0.008,
    amp: 120,
    phase: 0,
    speed: 0.025,
    terms: 9,
    green: [0, 255, 0],
    alpha: 60,
    yOffset: -100,
    thickness: 3
  });
  
  waves.push({
    freq: 0.012,
    amp: 90,
    phase: PI / 3,
    speed: -0.03,
    terms: 7,
    green: [50, 255, 50],
    alpha: 50,
    yOffset: -50,
    thickness: 2.5
  });
  
  waves.push({
    freq: 0.006,
    amp: 150,
    phase: PI / 2,
    speed: 0.02,
    terms: 11,
    green: [0, 200, 0],
    alpha: 45,
    yOffset: 0,
    thickness: 4
  });
  
  waves.push({
    freq: 0.015,
    amp: 70,
    phase: PI,
    speed: -0.035,
    terms: 6,
    green: [100, 255, 100],
    alpha: 55,
    yOffset: 50,
    thickness: 2
  });
  
  waves.push({
    freq: 0.01,
    amp: 100,
    phase: 3 * PI / 2,
    speed: 0.028,
    terms: 8,
    green: [0, 180, 0],
    alpha: 40,
    yOffset: 100,
    thickness: 3.5
  });
  
  waves.push({
    freq: 0.005,
    amp: 180,
    phase: PI / 6,
    speed: -0.015,
    terms: 12,
    green: [150, 255, 150],
    alpha: 35,
    yOffset: 150,
    thickness: 5
  });
  
  // Create glowing particles
  for (let i = 0; i < 50; i++) {
    particles.push({
      x: random(width),
      y: random(height),
      size: random(2, 6),
      speedX: random(-0.5, 0.5),
      speedY: random(-0.5, 0.5),
      green: [random(100, 255), 255, random(100, 255)],
      alpha: random(100, 200),
      pulse: random(TWO_PI)
    });
  }
}

function draw() {
  // Dark background with slight fade for trail effect
  background(0, 0, 0, 25);
  
  // Draw glowing particles
  for (let p of particles) {
    // Update particle position
    p.x += p.speedX;
    p.y += p.speedY;
    
    // Wrap around screen
    if (p.x < 0) p.x = width;
    if (p.x > width) p.x = 0;
    if (p.y < 0) p.y = height;
    if (p.y > height) p.y = 0;
    
    // Pulsing effect
    p.pulse += 0.05;
    let pulseSize = p.size + sin(p.pulse) * 2;
    
    // Draw glowing particle
    noStroke();
    for (let i = 3; i > 0; i--) {
      fill(p.green[0], p.green[1], p.green[2], p.alpha / (i * 2));
      circle(p.x, p.y, pulseSize * i * 2);
    }
    fill(p.green[0], p.green[1], p.green[2], p.alpha);
    circle(p.x, p.y, pulseSize);
  }
  
  // Draw each Fourier wave with glow effect
  for (let wave of waves) {
    drawFourierWave(wave);
  }
  
  // Draw intersection points highlights
  drawIntersections();
  
  time += 0.02;
}

function drawFourierWave(wave) {
  // Calculate wave points
  let points = [];
  for (let x = 0; x <= width; x += 3) {
    let y = height / 2 + wave.yOffset;
    
    // Fourier series summation
    for (let n = 1; n <= wave.terms; n++) {
      let amplitude = wave.amp / n;
      let frequency = wave.freq * n;
      let phaseShift = wave.phase + wave.speed * time * n;
      
      // Add some dynamic variation
      let dynamicPhase = phaseShift + sin(time * 0.5 + n) * 0.3;
      y += amplitude * sin(frequency * x + dynamicPhase);
    }
    
    points.push({x: x, y: y});
  }
  
  // Draw glow effect (multiple layers)
  for (let glowLayer = 4; glowLayer > 0; glowLayer--) {
    noFill();
    stroke(wave.green[0], wave.green[1], wave.green[2], wave.alpha / (glowLayer * 1.5));
    strokeWeight(wave.thickness + glowLayer * 3);
    
    beginShape();
    for (let p of points) {
      curveVertex(p.x, p.y);
    }
    endShape();
  }
  
  // Draw main wave line
  noFill();
  stroke(wave.green[0], wave.green[1], wave.green[2], wave.alpha * 2);
  strokeWeight(wave.thickness);
  
  beginShape();
  for (let p of points) {
    curveVertex(p.x, p.y);
  }
  endShape();
  
  // Add bright highlights at peaks
  for (let i = 0; i < points.length - 1; i += 15) {
    let p = points[i];
    let nextP = points[min(i + 1, points.length - 1)];
    let prevP = points[max(i - 1, 0)];
    
    // Detect peaks
    if ((p.y < prevP.y && p.y < nextP.y) || (p.y > prevP.y && p.y > nextP.y)) {
      noStroke();
      fill(wave.green[0], wave.green[1], wave.green[2], wave.alpha * 3);
      circle(p.x, p.y, wave.thickness * 2);
      
      // Glow around peak
      fill(wave.green[0], wave.green[1], wave.green[2], wave.alpha);
      circle(p.x, p.y, wave.thickness * 4);
    }
  }
}

function drawIntersections() {
  // Find and highlight wave intersections
  let samplePoints = 100;
  let step = width / samplePoints;
  
  for (let x = 0; x < width; x += step) {
    let yValues = [];
    
    for (let wave of waves) {
      let y = height / 2 + wave.yOffset;
      
      for (let n = 1; n <= wave.terms; n++) {
        let amplitude = wave.amp / n;
        let frequency = wave.freq * n;
        let phaseShift = wave.phase + wave.speed * time * n;
        let dynamicPhase = phaseShift + sin(time * 0.5 + n) * 0.3;
        y += amplitude * sin(frequency * x + dynamicPhase);
      }
      
      yValues.push(y);
    }
    
    // Check for intersections
    for (let i = 0; i < yValues.length; i++) {
      for (let j = i + 1; j < yValues.length; j++) {
        if (abs(yValues[i] - yValues[j]) < 10) {
          let avgY = (yValues[i] + yValues[j]) / 2;
          
          // Draw bright intersection point
          noStroke();
          fill(255, 255, 100, 150);
          circle(x, avgY, 8);
          
          fill(100, 255, 100, 100);
          circle(x, avgY, 16);
          
          fill(0, 255, 0, 50);
          circle(x, avgY, 24);
        }
      }
    }
  }
}

function windowResized() {
  resizeCanvas(windowWidth, windowHeight);
  
  // Reset particles for new dimensions
  particles = [];
  for (let i = 0; i < 50; i++) {
    particles.push({
      x: random(width),
      y: random(height),
      size: random(2, 6),
      speedX: random(-0.5, 0.5),
      speedY: random(-0.5, 0.5),
      green: [random(100, 255), 255, random(100, 255)],
      alpha: random(100, 200),
      pulse: random(TWO_PI)
    });
  }
}