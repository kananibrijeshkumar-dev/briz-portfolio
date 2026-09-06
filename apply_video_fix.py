import glob
import re

html_files = glob.glob("*.html")

canvas_html = """    <!-- Background Video Canvas -->
    <canvas id="hero-canvas"></canvas>
    <div class="overlay"></div>"""

video_html = """    <!-- Background Video -->
    <video id="hero-canvas" src="background.mp4" autoplay loop muted playsinline></video>
    <div class="overlay"></div>"""

# The script block to remove starts with <script> and ends with </script>
# It contains the "hero-canvas" and "video_frames_24fps" logic
script_pattern = re.compile(r'<script>\s*document\.addEventListener\(\'DOMContentLoaded\', \(\) => \{\s*const canvas = document\.getElementById\("hero-canvas"\);.*?\}\);\s*\}\);\s*</script>', re.DOTALL)

for file in html_files:
    with open(file, 'r') as f:
        content = f.read()

    # Replace canvas element with video element
    content = content.replace(canvas_html, video_html)
    
    # Just in case the previous replacement logic missed it, also do a direct replace:
    content = content.replace('<canvas id="hero-canvas"></canvas>', '<video id="hero-canvas" src="background.mp4" autoplay loop muted playsinline></video>')
    
    # Remove the heavy javascript
    content = script_pattern.sub('', content)

    with open(file, 'w') as f:
        f.write(content)

print("Canvas replaced with MP4 video tag on all pages!")
