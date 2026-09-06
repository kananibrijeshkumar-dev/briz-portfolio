import glob
import re

html_files = glob.glob("*.html")

new_script = """    <script>
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
"""

# The regex matches from <script> that contains "hero-canvas" up to the end of the old script logic (the if(firstImg) ... else ... block)
pattern = re.compile(r'<script>\s*const canvas = document\.getElementById\("hero-canvas"\);.*?setTimeout\(playAnimation, 1000\);\s*\}', re.DOTALL)

for file in html_files:
    with open(file, 'r') as f:
        content = f.read()
    
    content = pattern.sub(new_script, content)
    
    with open(file, 'w') as f:
        f.write(content)

print("Lazy loading optimization applied to all files!")
