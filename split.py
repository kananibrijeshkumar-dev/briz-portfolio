import re
import os

with open('index.html', 'r') as f:
    content = f.read()

# 1. Update the navigation links in the content
nav_pattern = re.compile(r'<ul class="nav-links">.*?</ul>', re.DOTALL)
new_nav = """<ul class="nav-links">
                    <li><a href="index.html">Home</a></li>
                    <li><a href="about.html">About</a></li>
                    <li><a href="services.html">Services</a></li>
                    <li><a href="projects.html">Projects</a></li>
                    <li><a href="contact.html">Contact</a></li>
                </ul>"""
content = nav_pattern.sub(new_nav, content)

# Also update the hero buttons
content = content.replace('href="#projects"', 'href="projects.html"')
content = content.replace('href="#contact"', 'href="contact.html"')

# 2. Extract sections
# Top part (up to the end of social-sidebar)
top_match = re.search(r'(.*?<div class="social-sidebar">.*?</div>)', content, re.DOTALL)
top_part = top_match.group(1) if top_match else ""

# Sections
home_match = re.search(r'(<!-- Hero Section -->.*?)</section>', content, re.DOTALL)
about_match = re.search(r'(<!-- About Section.*?)</section>', content, re.DOTALL)
services_match = re.search(r'(<!-- Services Section.*?)</section>', content, re.DOTALL)
projects_match = re.search(r'(<!-- Projects Section.*?)</section>', content, re.DOTALL)
contact_match = re.search(r'(<!-- Contact Section.*?)</section>', content, re.DOTALL)

home_sec = home_match.group(1) + "</section>\n" if home_match else ""
about_sec = about_match.group(1) + "</section>\n" if about_match else ""
services_sec = services_match.group(1) + "</section>\n" if services_match else ""
projects_sec = projects_match.group(1) + "</section>\n" if projects_match else ""
contact_sec = contact_match.group(1) + "</section>\n" if contact_match else ""

# Footer and script
bottom_match = re.search(r'(<!-- Footer -->.*)', content, re.DOTALL)
bottom_part = bottom_match.group(1) if bottom_match else ""

# Replace the scroll script with an autoplay script
old_script = """        window.addEventListener('scroll', () => {
            const scrollTop = document.documentElement.scrollTop;
            const maxScrollTop = document.documentElement.scrollHeight - window.innerHeight;
            
            // Calculate the fraction of the page that has been scrolled
            const scrollFraction = scrollTop / maxScrollTop;
            
            // Map the scroll fraction to a frame index (0 to 239)
            const frameIndex = Math.min(
                frameCount - 1,
                Math.max(0, Math.floor(scrollFraction * frameCount))
            );
            
            // Only draw if the frame has changed to optimize performance
            if (frameIndex !== lastFrameIndex && images[frameIndex] && images[frameIndex].complete) {
                requestAnimationFrame(() => {
                    context.drawImage(images[frameIndex], 0, 0);
                });
                lastFrameIndex = frameIndex;
            }
        });"""

new_script = """        // Autoplay loop
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

bottom_part_home = bottom_part.replace(old_script, new_script)

# For inner pages, remove the canvas entirely from top_part and remove canvas script from bottom_part
top_part_inner = re.sub(r'<!-- Background Video Canvas -->.*?<div class="overlay"></div>', '', top_part, flags=re.DOTALL)

# For inner bottom part, we keep the project filtering logic but remove canvas logic
inner_script_start = bottom_part.find('// Project Filtering Logic')
if inner_script_start != -1:
    bottom_part_inner = "<!-- Footer -->\n" + bottom_part[:bottom_part.find('<script>')] + "<script>\n" + bottom_part[inner_script_start:]
else:
    bottom_part_inner = bottom_part # fallback

# Generate index.html
with open('index.html', 'w') as f:
    f.write(top_part + "\n" + home_sec + "\n" + bottom_part_home)

# Generate about.html
with open('about.html', 'w') as f:
    f.write(top_part_inner + "\n<br><br><br><br>\n" + about_sec + "\n" + bottom_part_inner)

# Generate services.html
with open('services.html', 'w') as f:
    f.write(top_part_inner + "\n<br><br><br><br>\n" + services_sec + "\n" + bottom_part_inner)

# Generate projects.html
with open('projects.html', 'w') as f:
    f.write(top_part_inner + "\n<br><br><br><br>\n" + projects_sec + "\n" + bottom_part_inner)

# Generate contact.html
with open('contact.html', 'w') as f:
    f.write(top_part_inner + "\n<br><br><br><br>\n" + contact_sec + "\n" + bottom_part_inner)

print("Split complete!")
