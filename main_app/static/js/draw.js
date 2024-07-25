const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
let isDrawing = false;

canvas.addEventListener('mousedown', startDrawing);
canvas.addEventListener('mousemove', draw);
canvas.addEventListener('mouseup', stopDrawing);
canvas.addEventListener('mouseout', stopDrawing);

function startDrawing(e) {
    isDrawing = true;
    draw(e);
}

function draw(e) {
    if (!isDrawing) return;
    ctx.lineWidth = 15;
    ctx.lineCap = 'round';
    ctx.strokeStyle = 'rgba(255, 0, 0, 0.5)'; 
    const { offsetX, offsetY } = e;
    ctx.lineTo(offsetX, offsetY);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(offsetX, offsetY);
}

function stopDrawing() {
    isDrawing = false;
    ctx.beginPath();
}

document.getElementById('file-upload').addEventListener('change', function(e) {
    const file = e.target.files[0];
    const reader = new FileReader();
    reader.onload = function(event) {
        const img = new Image();
        img.onload = function() {
            const scaleFactor = Math.min(canvas.width / img.width, canvas.height / img.height);
            const centerX = (canvas.width - img.width * scaleFactor) / 2;
            const centerY = (canvas.height - img.height * scaleFactor) / 2;
            ctx.drawImage(img, centerX, centerY, img.width * scaleFactor, img.height * scaleFactor);
        };
        img.src = event.target.result;
    };
    reader.readAsDataURL(file);
});

function incrementCount(itemId) {
    var countSpan = document.getElementById('count_' + itemId);
    var currentCount = parseInt(countSpan.innerHTML);
    countSpan.innerHTML = currentCount + 1;
}

function decrementCount(itemId) {
    var countSpan = document.getElementById('count_' + itemId);
    var currentCount = parseInt(countSpan.innerHTML);
    if (currentCount > 0) {
        countSpan.innerHTML = currentCount - 1;
    }
}

// JavaScript function to increment orientation count
function incrementOrientationCount(itemId) {
    var orientationCountSpan = document.getElementById('orientation_count_' + itemId);
    var currentCount = parseInt(orientationCountSpan.innerHTML);
    orientationCountSpan.innerHTML = currentCount + 1;
}

// JavaScript function to decrement orientation count
function decrementOrientationCount(itemId) {
    var orientationCountSpan = document.getElementById('orientation_count_' + itemId);
    var currentCount = parseInt(orientationCountSpan.innerHTML);
    if (currentCount > 0) {
        orientationCountSpan.innerHTML = currentCount - 1;
    }
}