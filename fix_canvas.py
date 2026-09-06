import glob

html_files = glob.glob("*.html")

canvas_html = """
    <!-- Background Video Canvas -->
    <canvas id="hero-canvas"></canvas>
    <div class="overlay"></div>

    <!-- Main Content -->"""

canvas_script = """
    <script>
        document.addEventListener('DOMContentLoaded', () => {
            const canvas = document.getElementById("hero-canvas");
            if (!canvas) return;
            const context = canvas.getContext("2d");
            const frameCount = 240;
            
            const currentFrame = index => (`video_frames_24fps/frame_${index.toString().padStart(4, '0')}.jpg`);

            const images = [];
            let loadedCount = 0;
            let firstImg = new Image();
            firstImg.src = currentFrame(1);
            
            // Load frame 1 instantly so we have a background
            firstImg.onload = () => {
                canvas.width = firstImg.width;
                canvas.height = firstImg.height;
                context.drawImage(firstImg, 0, 0);
                images[0] = firstImg;
                loadedCount++;
                
                // Wait for the rest of the page to load (images, fonts, css) before grabbing 64MB of frames
                window.addEventListener('load', () => {
                    // Lazy load the rest in the background
                    for (let i = 2; i <= frameCount; i++) {
                        const img = new Image();
                        img.src = currentFrame(i);
                        img.onload = () => { loadedCount++; };
                        images[i-1] = img;
                    }
                    
                    // Start animation loop
                    let currentFrameIndex = 0;
                    function playAnimation() {
                        if (images[currentFrameIndex] && images[currentFrameIndex].complete) {
                            context.drawImage(images[currentFrameIndex], 0, 0);
                        }
                        currentFrameIndex = (currentFrameIndex + 1) % frameCount;
                        setTimeout(() => requestAnimationFrame(playAnimation), 1000 / 24);
                    }
                    
                    setTimeout(playAnimation, 500); // Small delay to ensure smooth start
                });
            };
        });
    </script>
"""

for file in html_files:
    if file == 'index.html':
        continue
        
    with open(file, 'r') as f:
        content = f.read()

    # Check if we already injected the HTML canvas element
    if '<canvas id="hero-canvas">' not in content:
        content = content.replace("<!-- Main Content -->", canvas_html)
        
    # Check if we already injected the javascript for the canvas
    if 'document.getElementById("hero-canvas")' not in content:
        content = content.replace("</body>", canvas_script + "\n</body>")

    with open(file, 'w') as f:
        f.write(content)

print("Canvas successfully injected into all sub-pages!")
