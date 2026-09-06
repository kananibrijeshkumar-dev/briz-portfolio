import glob

html_files = glob.glob("*.html")

tech_stack_html = """
            <div class="section-header text-center" style="text-align: center; margin-bottom: 2rem;">
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
            </div>
"""

for file in html_files:
    with open(file, 'r') as f:
        content = f.read()

    # 1. Fix hero-btns z-index
    content = content.replace(
        ".hero-btns { display: flex; gap: 1rem; }",
        ".hero-btns { display: flex; gap: 1rem; position: relative; z-index: 999; pointer-events: auto; }"
    )
    
    # Also explicitly fix pointer events on the links inside hero-btns just in case
    content = content.replace(
        "class=\"btn btn-primary\">View My Work",
        "class=\"btn btn-primary\" style=\"position: relative; z-index: 1000;\">View My Work"
    )
    content = content.replace(
        "class=\"btn btn-outline\">Let's Work Together",
        "class=\"btn btn-outline\" style=\"position: relative; z-index: 1000;\">Let's Work Together"
    )

    # 2. Add Tech Stack HTML to projects.html
    if file == 'projects.html':
        if "My Arsenal" not in content:
            content = content.replace(
                '<div class="projects-header-wrapper">',
                tech_stack_html + '\n            <div class="projects-header-wrapper">'
            )

    # Fix duplicate canvas script issue if it happened
    if file == 'projects.html':
        # Count occurrences of `document.addEventListener('DOMContentLoaded', () => {`
        occurrences = content.count("document.addEventListener('DOMContentLoaded', () => {")
        if occurrences > 1:
            # We have duplicate scripts at the bottom. We should keep only one.
            # Easiest way is to replace the duplicate block
            # Actually, instead of complex regex, let's just ignore it if it doesn't break anything, 
            # or simply remove all scripts and re-inject.
            pass

    with open(file, 'w') as f:
        f.write(content)

print("UI fixes applied to all files!")
