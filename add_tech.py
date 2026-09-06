import glob
import os
import shutil

html_files = glob.glob("*.html")

nav_search = '<li><a href="projects.html">Projects</a></li>'
nav_replace = '<li><a href="projects.html">Projects</a></li>\n                    <li><a href="tech.html">Tech Stack</a></li>'

for file in html_files:
    if file == 'tech.html':
        continue
    with open(file, 'r') as f:
        content = f.read()
    
    if 'href="tech.html"' not in content:
        content = content.replace(nav_search, nav_replace)
        
    with open(file, 'w') as f:
        f.write(content)

# Now create tech.html from services.html
if os.path.exists('services.html'):
    shutil.copy('services.html', 'tech.html')
    
    with open('tech.html', 'r') as f:
        tech_content = f.read()
    
    # Update active class in nav
    tech_content = tech_content.replace('<li><a href="services.html" class="active">', '<li><a href="services.html">')
    # Actually wait, services.html might not have class="active", in this template they might not be using it. Let's just do a generic replace if it exists.
    
    # Replace the Services section with Tech Stack section
    import re
    # Find the section with id="services" up to </section>
    services_pattern = re.compile(r'<section id="services" class="container">.*?</section>', re.DOTALL)
    
    tech_section = """<section id="tech" class="container">
            <div class="section-header text-center" style="text-align: center;">
                <h4>My Arsenal</h4>
                <h2>Tech Stack</h2>
            </div>
            <div class="tech-grid" style="margin-top: 3rem;">
                <div class="tech-item">
                    <i class="ph ph-atom"></i>
                    <span>React</span>
                </div>
                <div class="tech-item">
                    <i class="ph ph-hexagon"></i>
                    <span>Node.js</span>
                </div>
                <div class="tech-item">
                    <i class="ph ph-file-code"></i>
                    <span>JavaScript</span>
                </div>
                <div class="tech-item">
                    <i class="ph ph-file-html"></i>
                    <span>HTML5</span>
                </div>
                <div class="tech-item">
                    <i class="ph ph-file-css"></i>
                    <span>CSS3</span>
                </div>
                <div class="tech-item">
                    <i class="ph ph-wind"></i>
                    <span>Tailwind</span>
                </div>
                <div class="tech-item">
                    <i class="ph ph-database"></i>
                    <span>MongoDB</span>
                </div>
                <div class="tech-item">
                    <i class="ph ph-robot"></i>
                    <span>AI / LLMs</span>
                </div>
                <div class="tech-item">
                    <i class="ph ph-git-branch"></i>
                    <span>Git</span>
                </div>
                <div class="tech-item">
                    <i class="ph ph-figma-logo"></i>
                    <span>Figma</span>
                </div>
                <div class="tech-item">
                    <i class="ph ph-video"></i>
                    <span>Premiere Pro</span>
                </div>
                <div class="tech-item">
                    <i class="ph ph-camera"></i>
                    <span>After Effects</span>
                </div>
            </div>
        </section>"""
        
    tech_content = services_pattern.sub(tech_section, tech_content)
    
    with open('tech.html', 'w') as f:
        f.write(tech_content)

print("Tech page and navigation added successfully!")
