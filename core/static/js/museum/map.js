const keys = {};
const FOV = Math.PI / 3;
const HALF_FOV = FOV / 2;
const NUM_RAYS = 320; // Reduced from 720
const MAX_DEPTH = 800;
const DELTA_ANGLE = FOV / NUM_RAYS;

let fps = 0;
let lastTime = 0;
let frameCount = 0;
let fpsTime = 0;

let lookingAtDoor = false;
let currentDoorInfo = null;
let lastDoorCheck = 0;

// Portal state
let readmeOpen = false;
const readmeOverlay = document.getElementById('readme-overlay');
const readmeContent = document.getElementById('readme-content');
const closeBtn = document.getElementById('close-readme');
const doorText = document.getElementById('door-text');
const doorDescription = document.getElementById('door-description');
const repoTitle = document.getElementById('repo-title');
const readmeDescription = document.getElementById('readme-description');

closeBtn.addEventListener('click', closeReadme);

function closeReadme() {
    readmeOpen = false;
    readmeOverlay.classList.remove('active');
}

function openReadme(repoInfo) {
    readmeOpen = true;
    readmeOverlay.classList.add('active');
    
    // Set title and description
    repoTitle.textContent = `📦 ${repoInfo.title}`;
    readmeDescription.innerHTML = `
        <strong>${repoInfo.title}</strong><br>
        ${repoInfo.description}<br>
        <a href="${repoInfo.url}" target="_blank" style="color: #FFD700;">${repoInfo.url}</a>
    `;
    
    // Render markdown
    try {
        readmeContent.innerHTML = marked.parse(repoInfo.readme);
    } catch (e) {
        readmeContent.innerHTML = `<pre>${repoInfo.readme}</pre>`;
    }
}

function getMapValue(x, y) {
    const mx = Math.floor(x / TILE_SIZE);
    const my = Math.floor(y / TILE_SIZE);
    if (mx < 0 || mx >= MAP_SIZE || my < 0 || my >= MAP_SIZE) return 1;
    return map[my][mx];
}

function checkCollision(x, y) {
    const val = getMapValue(x, y);
    return val === 1 || val === 2;
}

function checkLookingAtDoor() {
    const dirX = Math.cos(player.angle);
    const dirY = Math.sin(player.angle);
    const checkDist = 80;
    
    const checkX = player.x + dirX * checkDist;
    const checkY = player.y + dirY * checkDist;
    
    const mx = Math.floor(checkX / TILE_SIZE);
    const my = Math.floor(checkY / TILE_SIZE);
    
    if (mx >= 0 && mx < MAP_SIZE && my >= 0 && my < MAP_SIZE) {
        const val = map[my][mx];
        if (val === 2) {
            const doorKey = `${mx},${my}`;
            const portalIndex = doorPortalMap[doorKey];
            if (portalIndex !== undefined) {
                return {
                    isDoor: true,
                    repoInfo: portalSites[portalIndex],
                    coords: doorKey
                };
            }
        }
    }
    return { isDoor: false };
}

function interact() {
    const dirX = Math.cos(player.angle);
    const dirY = Math.sin(player.angle);
    const checkDist = 80;
    
    const checkX = player.x + dirX * checkDist;
    const checkY = player.y + dirY * checkDist;
    
    const mx = Math.floor(checkX / TILE_SIZE);
    const my = Math.floor(checkY / TILE_SIZE);
    const val = map[my][mx];
    
    if (val === 2) {
        // Open repository README
        const doorKey = `${mx},${my}`;
        const portalIndex = doorPortalMap[doorKey];
        if (portalIndex !== undefined) {
            openReadme(portalSites[portalIndex]);
        }
    }
}

function castRay(angle) {
    const rayX = Math.cos(angle);
    const rayY = Math.sin(angle);
    
    let depth = 0;
    let hit = false;
    let hitValue = 0;
    let hitX = 0;
    let hitY = 0;
    
    // DDA algorithm for faster raycasting
    const stepSize = 4; // Jump in larger steps
    
    while (!hit && depth < MAX_DEPTH) {
        depth += stepSize;
        const targetX = player.x + rayX * depth;
        const targetY = player.y + rayY * depth;
        
        hitValue = getMapValue(targetX, targetY);
        if (hitValue > 0) {
            // Fine-tune hit position
            depth -= stepSize;
            for (let i = 0; i < stepSize; i++) {
                depth += 1;
                const tx = player.x + rayX * depth;
                const ty = player.y + rayY * depth;
                if (getMapValue(tx, ty) > 0) {
                    hitX = tx;
                    hitY = ty;
                    hitValue = getMapValue(tx, ty);
                    hit = true;
                    break;
                }
            }
            break;
        }
    }
    
    if (!hit) {
        hitX = player.x + rayX * depth;
        hitY = player.y + rayY * depth;
    }
    
    // Calculate texture coordinate
    const relX = hitX % TILE_SIZE;
    const relY = hitY % TILE_SIZE;
    let textureX;
    
    if (Math.abs(relX) < 2 || Math.abs(relX - TILE_SIZE) < 2) {
        textureX = relY / TILE_SIZE;
    } else {
        textureX = relX / TILE_SIZE;
    }
    
    return { depth, hitValue, textureX };
}

function drawWall(x, wallHeight, hitValue, shade, textureX) {
    const stripWidth = WIDTH / NUM_RAYS + 1;
    const wallTop = (HEIGHT - wallHeight) / 2;
    
    if (hitValue === 2) {
        // Draw textured door with GitHub logo (same as walls)
        if (textures.github.complete && textures.github.naturalWidth > 0) {
            const imgX = Math.floor(textureX * textures.github.width) % textures.github.width;
            
            ctx.save();
            ctx.globalAlpha = shade;
            ctx.drawImage(
                textures.github,
                imgX, 0, 1, textures.github.height,
                x, wallTop, stripWidth, wallHeight
            );
            ctx.restore();
        } else {
            // Fallback to colored door
            ctx.fillStyle = shadeColor('#FFD700', shade);
            ctx.fillRect(x, wallTop, stripWidth, wallHeight);
        }
    } else if (hitValue === 1) {
        // Draw textured wall with column sampling
        if (textures.wall.complete && textures.wall.naturalWidth > 0) {
            const imgX = Math.floor(textureX * textures.wall.width) % textures.wall.width;
            
            ctx.save();
            ctx.globalAlpha = shade;
            ctx.drawImage(
                textures.wall,
                imgX, 0, 1, textures.wall.height,
                x, wallTop, stripWidth, wallHeight
            );
            ctx.restore();
        } else {
            ctx.fillStyle = shadeColor('#808080', shade);
            ctx.fillRect(x, wallTop, stripWidth, wallHeight);
        }
    }
}

function shadeColor(color, amount) {
    const num = parseInt(color.slice(1), 16);
    const r = Math.max(0, Math.min(255, (num >> 16) * amount));
    const g = Math.max(0, Math.min(255, ((num >> 8) & 0x00FF) * amount));
    const b = Math.max(0, Math.min(255, (num & 0x0000FF) * amount));
    return `rgb(${r},${g},${b})`;
}

function drawTexturedFloor() {
    if (!textures.floor.complete || textures.floor.naturalWidth === 0) {
        ctx.fillStyle = '#34495E';
        ctx.fillRect(0, HEIGHT / 2, WIDTH, HEIGHT / 2);
        return;
    }
    
    const floorHeight = HEIGHT / 2;
    const stepY = 8; // Skip rows for performance
    const stepX = 8; // Skip columns for performance
    
    for (let y = 0; y < floorHeight; y += stepY) {
        const screenY = HEIGHT / 2 + y;
        const rayDirX0 = Math.cos(player.angle - HALF_FOV);
        const rayDirY0 = Math.sin(player.angle - HALF_FOV);
        const rayDirX1 = Math.cos(player.angle + HALF_FOV);
        const rayDirY1 = Math.sin(player.angle + HALF_FOV);
        
        const rowDistance = (HEIGHT / 2) / (y + 0.1);
        
        const floorStepX = rowDistance * (rayDirX1 - rayDirX0) / WIDTH;
        const floorStepY = rowDistance * (rayDirY1 - rayDirY0) / WIDTH;
        
        let floorX = player.x + rowDistance * rayDirX0;
        let floorY = player.y + rowDistance * rayDirY0;
        
        const shade = Math.max(0.3, 1 - rowDistance / MAX_DEPTH);
        ctx.globalAlpha = shade;
        
        for (let x = 0; x < WIDTH; x += stepX) {
            const tx = Math.floor((floorX % TILE_SIZE) / TILE_SIZE * textures.floor.width) % textures.floor.width;
            const ty = Math.floor((floorY % TILE_SIZE) / TILE_SIZE * textures.floor.height) % textures.floor.height;
            
            ctx.drawImage(
                textures.floor,
                tx, ty, 1, 1,
                x, screenY, stepX, stepY
            );
            
            floorX += floorStepX * stepX;
            floorY += floorStepY * stepX;
        }
    }
    
    ctx.globalAlpha = 1.0;
}

function render() {
    // Draw ceiling
    ctx.fillStyle = '#2C3E50';
    ctx.fillRect(0, 0, WIDTH, HEIGHT / 2);
    
    // Draw textured floor
    drawTexturedFloor();
    
    // Cast rays for walls
    for (let i = 0; i < NUM_RAYS; i++) {
        const rayAngle = player.angle - HALF_FOV + (i * DELTA_ANGLE);
        const { depth, hitValue, textureX } = castRay(rayAngle);
        
        // Fix fish-eye effect
        const distance = depth * Math.cos(rayAngle - player.angle);
        const wallHeight = (TILE_SIZE * HEIGHT) / (distance + 0.0001);
        
        // Calculate shading based on distance
        const shade = Math.max(0.3, 1 - distance / MAX_DEPTH);
        
        drawWall(i * (WIDTH / NUM_RAYS), wallHeight, hitValue, shade, textureX);
    }
    
    // Show door text if looking at repository door
    if (lookingAtDoor && currentDoorInfo) {
        doorDescription.innerHTML = `<strong>${currentDoorInfo.repoInfo.title}</strong><br>${currentDoorInfo.repoInfo.description}`;
        doorText.classList.add('show');
    } else {
        doorText.classList.remove('show');
    }
}

function drawMinimap() {
    const scale = minimap.width / (MAP_SIZE * TILE_SIZE);
    mmCtx.fillStyle = '#000';
    mmCtx.fillRect(0, 0, minimap.width, minimap.height);
    
    // Draw map
    for (let y = 0; y < MAP_SIZE; y++) {
        for (let x = 0; x < MAP_SIZE; x++) {
            const val = map[y][x];
            if (val === 1) mmCtx.fillStyle = '#fff';
            else if (val === 2) mmCtx.fillStyle = '#ff0';
            else mmCtx.fillStyle = '#222';
            
            mmCtx.fillRect(x * TILE_SIZE * scale, y * TILE_SIZE * scale, 
                           TILE_SIZE * scale, TILE_SIZE * scale);
        }
    }
    
    // Draw player
    mmCtx.fillStyle = '#f00';
    mmCtx.beginPath();
    mmCtx.arc(player.x * scale, player.y * scale, 3, 0, Math.PI * 2);
    mmCtx.fill();
    
    // Draw direction
    mmCtx.strokeStyle = '#f00';
    mmCtx.beginPath();
    mmCtx.moveTo(player.x * scale, player.y * scale);
    mmCtx.lineTo(
        player.x * scale + Math.cos(player.angle) * 15,
        player.y * scale + Math.sin(player.angle) * 15
    );
    mmCtx.stroke();
}

function update(deltaTime) {
    const moveSpeed = player.speed;
    
    // Movement
    if (keys['w'] || keys['ArrowUp']) {
        const newX = player.x + Math.cos(player.angle) * moveSpeed;
        const newY = player.y + Math.sin(player.angle) * moveSpeed;
        if (!checkCollision(newX, newY)) {
            player.x = newX;
            player.y = newY;
        }
    }
    if (keys['s'] || keys['ArrowDown']) {
        const newX = player.x - Math.cos(player.angle) * moveSpeed;
        const newY = player.y - Math.sin(player.angle) * moveSpeed;
        if (!checkCollision(newX, newY)) {
            player.x = newX;
            player.y = newY;
        }
    }
    
    // Rotation
    if (keys['a'] || keys['ArrowLeft']) {
        player.angle -= player.rotSpeed;
    }
    if (keys['d'] || keys['ArrowRight']) {
        player.angle += player.rotSpeed;
    }
    
    // Check if looking at door
    const now = Date.now();
    if (now - lastDoorCheck > 100) {
        const doorCheck = checkLookingAtDoor();
        lookingAtDoor = doorCheck.isDoor;
        currentDoorInfo = doorCheck.isDoor ? doorCheck : null;
        lastDoorCheck = now;
    }
    
    // Interaction
    if (keys['e']) {
        interact();
        keys['e'] = false; // Prevent repeated triggers
    }
    
    // Update HUD
    document.getElementById('pos').textContent = 
        `${Math.floor(player.x / TILE_SIZE)}, ${Math.floor(player.y / TILE_SIZE)}`;
}

function gameLoop(timestamp) {
    if (readmeOpen) {
        requestAnimationFrame(gameLoop);
        return;
    }
    
    const deltaTime = timestamp - lastTime;
    lastTime = timestamp;
    
    // Calculate FPS
    frameCount++;
    fpsTime += deltaTime;
    if (fpsTime >= 1000) {
        fps = Math.round(frameCount * 1000 / fpsTime);
        document.getElementById('fps').textContent = fps;
        frameCount = 0;
        fpsTime = 0;
    }
    
    update(deltaTime);
    render();
    drawMinimap();
    
    requestAnimationFrame(gameLoop);
}

// Event listeners
window.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && readmeOpen) {
        closeReadme();
    }
    keys[e.key.toLowerCase()] = true;
});

window.addEventListener('keyup', (e) => {
    keys[e.key.toLowerCase()] = false;
});

// Don't start game until textures are loaded
// The game loop is started by the texture load handler in the HTML file