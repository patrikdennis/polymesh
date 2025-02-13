document.addEventListener("DOMContentLoaded", function () {
    let points = [];
    const canvas = document.getElementById("myCanvas");
    const ctx = canvas.getContext("2d");
    const finishBtn = document.getElementById("finishBtn");
    const clearBtn = document.getElementById("clearBtn");

    function drawPoint(x, y) {
        ctx.fillStyle = "red";
        ctx.beginPath();
        ctx.arc(x, y, 3, 0, 2 * Math.PI);
        ctx.fill();
    }

    function drawLine(x1, y1, x2, y2) {
        ctx.strokeStyle = "red";
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(x1, y1);
        ctx.lineTo(x2, y2);
        ctx.stroke();
    }

    function clearCanvas() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        points = [];
    }

    canvas.addEventListener("click", function (e) {
        const rect = canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        // Close the polygon if clicking near the first point
        if (points.length > 2) {
            const firstPoint = points[0];
            const dx = x - firstPoint[0];
            const dy = y - firstPoint[1];
            if (Math.sqrt(dx * dx + dy * dy) < 10) { // Close the polygon
                drawLine(points[points.length - 1][0], points[points.length - 1][1], firstPoint[0], firstPoint[1]);
                points.push(firstPoint);  
                return;
            }
        }

        // Draw point
        drawPoint(x, y);

        // Draw line to the previous point
        if (points.length > 0) {
            const lastPoint = points[points.length - 1];
            drawLine(lastPoint[0], lastPoint[1], x, y);
        }

        points.push([x, y]);
    });

    function sendPolygonToServer() {
        if (points.length < 3) {
            alert("You need at least 3 points to create a polygon!");
            return;
        }

        const csrfToken = document.getElementById("csrf_token") ? document.getElementById("csrf_token").value : "";
        
        fetch("/generate-mesh/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken(),
            },
            body: JSON.stringify({ points: points }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                drawMesh(data.edges);
            } else {
                alert("Error: " + data.error);
            }
        })
        .catch(err => {
            console.error("Fetch error:", err);
            alert("An error occurred. Check the console for details.");
        });
    }

    function drawMesh(edges) {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.strokeStyle = "blue";
        ctx.lineWidth = 1;

        edges.forEach(edge => {
            let [x1, y1] = edge[0];
            let [x2, y2] = edge[1];

            ctx.beginPath();
            ctx.moveTo(x1, y1);
            ctx.lineTo(x2, y2);
            ctx.stroke();
        });
    }

    finishBtn.addEventListener("click", sendPolygonToServer);
    clearBtn.addEventListener("click", clearCanvas);
});


function getCSRFToken() {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith("csrftoken=")) {
                cookieValue = cookie.substring("csrftoken=".length, cookie.length);
                break;
            }
        }
    }
    return cookieValue;
}


