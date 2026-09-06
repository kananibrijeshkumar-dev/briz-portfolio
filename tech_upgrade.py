import os
import glob
import re

html_files = glob.glob("*.html")

canvas_html = """
    <!-- Background Video Canvas -->
    <canvas id="hero-canvas"></canvas>
    <div class="overlay"></div>

    <!-- Main Content -->"""

canvas_script = """
    <script>
        const canvas = document.getElementById("hero-canvas");
        const context = canvas.getContext("2d");

        const frameCount = 240;
        
        // The frames are named frame_0001.jpg through frame_0240.jpg
        const currentFrame = index => (
            `video_frames_24fps/frame_${index.toString().padStart(4, '0')}.jpg`
        );

        // Preload all images to prevent flickering
        const images = [];
        let loadedCount = 0;
        for (let i = 1; i <= frameCount; i++) {
            const img = new Image();
            img.src = currentFrame(i);
            img.onload = () => {
                loadedCount++;
                // Wait for the first image to load to set the initial canvas dimensions and draw it
                if(i === 1) {
                    canvas.width = img.width;
                    canvas.height = img.height;
                    context.drawImage(img, 0, 0);
                }
            };
            images.push(img);
        }

        let lastFrameIndex = 0;

        // Autoplay loop
        let currentFrameIndex = 0;
        function playAnimation() {
            if (images[currentFrameIndex] && images[currentFrameIndex].complete) {
                context.drawImage(images[currentFrameIndex], 0, 0);
            }
            currentFrameIndex = (currentFrameIndex + 1) % frameCount;
            setTimeout(() => {
                requestAnimationFrame(playAnimation);
            }, 1000 / 24); // 24 FPS
        }
        
        // Start playing once first image is loaded
        const firstImg = images[0];
        if(firstImg) {
            firstImg.addEventListener('load', () => {
                playAnimation();
            });
        } else {
            setTimeout(playAnimation, 1000);
        }
"""

old_overlay_css = """        .overlay {
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: linear-gradient(180deg, rgba(0,0,0,0.1) 0%, rgba(0,0,0,0.8) 100%);
            z-index: 1;
            pointer-events: none;
        }"""

new_overlay_css = """        .overlay {
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: linear-gradient(180deg, rgba(0,0,0,0.1) 0%, rgba(0,0,0,0.85) 100%),
                        linear-gradient(rgba(255, 69, 0, 0.03) 1px, transparent 1px),
                        linear-gradient(90deg, rgba(255, 69, 0, 0.03) 1px, transparent 1px);
            background-size: 100% 100%, 40px 40px, 40px 40px;
            z-index: 1;
            pointer-events: none;
        }"""

for file in html_files:
    with open(file, 'r') as f:
        content = f.read()

    # 1. Update overlay CSS in all files
    content = content.replace(old_overlay_css, new_overlay_css)

    # 2. Add neon hover effects and terminal styling to CSS
    if "/* Projects */" in content and ".mac-dots" not in content:
        # Add mac dots CSS
        css_inject = """        /* Techie Enhancements */
        .hero-tag { font-family: 'Courier New', Courier, monospace; background: rgba(255,69,0,0.1); padding: 5px 10px; border-radius: 4px; border: 1px solid rgba(255,69,0,0.3); }
        .glass-panel:hover, .service-card:hover, .project-card:hover, .testi-card:hover {
            box-shadow: 0 0 20px rgba(255, 69, 0, 0.15);
            border-color: rgba(255, 69, 0, 0.5);
        }
        .mac-dots {
            height: 30px; background: #1a1a1a; border-bottom: 1px solid var(--border-glass);
            display: flex; align-items: center; padding: 0 15px; gap: 6px;
        }
        .mac-dot { width: 10px; height: 10px; border-radius: 50%; }
        .mac-dot.red { background: #ff5f56; }
        .mac-dot.yellow { background: #ffbd2e; }
        .mac-dot.green { background: #27c93f; }
        """
        content = content.replace("/* Projects */", css_inject + "\n        /* Projects */")
    
    # Add mac dots to project cards
    if '<div class="project-img"' in content:
        content = content.replace('<div class="project-img"', '<div class="mac-dots"><div class="mac-dot red"></div><div class="mac-dot yellow"></div><div class="mac-dot green"></div></div>\n                        <div class="project-img"')

    # 3. Add Canvas HTML and Script if it doesn't exist (excluding index.html which already has it)
    if file != 'index.html':
        if "hero-canvas" not in content:
            # Replace <!-- Main Content --> with canvas + main content
            content = content.replace("<!-- Main Content -->", canvas_html)
            
            # Find the easiest injection point for script: right before </body>
            content = content.replace("</body>", canvas_script + "\n</body>")

    with open(file, 'w') as f:
        f.write(content)

print("Tech upgrade applied to all files!")
