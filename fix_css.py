import glob
import re

html_files = glob.glob("*.html")

old_css = """        @media (max-width: 900px) {
            .hero h1 { font-size: 3.8rem; }
            .about-grid, .contact-grid, .form-group { grid-template-columns: 1fr; }
            .social-sidebar { display: none; }
            .nav-links { display: none; }
            .projects-header-wrapper { flex-direction: column; align-items: flex-start; gap: 1rem; }
        }"""

new_css = """        @media (max-width: 900px) {
            .hero h1 { font-size: 3.8rem; }
            .about-grid, .contact-grid, .form-group { grid-template-columns: 1fr; }
            .projects-header-wrapper { flex-direction: column; align-items: flex-start; gap: 1rem; }
            
            /* Mobile Navigation Fix */
            nav { padding: 1rem 0; position: relative; }
            .nav-inner { flex-direction: column; gap: 1rem; text-align: center; }
            .nav-links { display: flex; flex-wrap: wrap; justify-content: center; gap: 1rem; }
            
            /* Mobile Social Sidebar Fix */
            .social-sidebar { position: relative; left: 0; transform: none; flex-direction: row; justify-content: center; padding: 2rem 0; width: 100%; background: #000; }
        }"""

for file in html_files:
    with open(file, 'r') as f:
        content = f.read()
    
    content = content.replace(old_css, new_css)
    
    with open(file, 'w') as f:
        f.write(content)

print("Fixed mobile CSS on all pages")
