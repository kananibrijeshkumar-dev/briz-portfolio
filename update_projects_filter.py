import re

with open('projects.html', 'r') as f:
    content = f.read()

# 1. Remove the old massive tech stack grid
# The tech stack injected by fix_ui.py started with <div class="section-header text-center" and ended with </div> (multiple).
# Actually, it's easier to just find the exact string we injected and replace it.

old_tech_stack = """            <div class="section-header text-center" style="text-align: center; margin-bottom: 2rem;">
                <h4>My Arsenal</h4>
                <h2>Tech Stack</h2>
            </div>
            
            <div class="tech-grid" style="margin-bottom: 5rem;">
                <div class="tech-item active" data-filter="all">
                    <i class="ph ph-squares-four"></i>
                    <span>All</span>
                </div>
                <div class="tech-item" data-filter="react">
                    <i class="ph ph-atom"></i>
                    <span>React</span>
                </div>
                <div class="tech-item" data-filter="node">
                    <i class="ph ph-hexagon"></i>
                    <span>Node.js</span>
                </div>
                <div class="tech-item" data-filter="js">
                    <i class="ph ph-file-code"></i>
                    <span>JavaScript</span>
                </div>
                <div class="tech-item" data-filter="tailwind">
                    <i class="ph ph-wind"></i>
                    <span>Tailwind</span>
                </div>
                <div class="tech-item" data-filter="ai">
                    <i class="ph ph-robot"></i>
                    <span>AI Tools</span>
                </div>
            </div>"""

new_filter_bar = """            <div class="filter-bar" style="display: flex; justify-content: center; flex-wrap: wrap; gap: 1rem; margin-bottom: 4rem;">
                <button class="filter-pill active" data-filter="all">All Projects</button>
                <button class="filter-pill" data-filter="react">React</button>
                <button class="filter-pill" data-filter="node">Node.js</button>
                <button class="filter-pill" data-filter="js">JavaScript</button>
                <button class="filter-pill" data-filter="tailwind">Tailwind</button>
                <button class="filter-pill" data-filter="ai">AI / LLMs</button>
            </div>
            
            <style>
                .filter-pill {
                    background: rgba(255, 255, 255, 0.05);
                    border: 1px solid rgba(255, 255, 255, 0.1);
                    color: #A0A0A0;
                    padding: 0.6rem 1.5rem;
                    border-radius: 50px;
                    font-family: var(--font-body);
                    font-size: 0.9rem;
                    cursor: pointer;
                    transition: all 0.3s ease;
                }
                .filter-pill:hover, .filter-pill.active {
                    background: rgba(255, 69, 0, 0.15);
                    border-color: #FF4500;
                    color: #fff;
                    box-shadow: 0 0 15px rgba(255, 69, 0, 0.2);
                }
            </style>"""

content = content.replace(old_tech_stack, new_filter_bar)

# 2. Update the javascript that handles filtering to target .filter-pill instead of .tech-item
js_old = "const techItems = document.querySelectorAll('.tech-item');"
js_new = "const techItems = document.querySelectorAll('.filter-pill');"
content = content.replace(js_old, js_new)

with open('projects.html', 'w') as f:
    f.write(content)

print("Projects page filter updated successfully!")
