with open("index.html", "r") as f:
    content = f.read()

content = content.replace("Hi! I am Briz Patel\"s AI Assistant.", "Hi! I am Briz Patel\\'s AI Assistant.")

sidebar_css = """
        /* Social Sidebar */
        .social-sidebar { position: fixed; left: 2.5rem; top: 50%; transform: translateY(-50%); display: flex; flex-direction: column; gap: 1.5rem; z-index: 100; }
        .social-sidebar a { color: var(--text-secondary); font-size: 1.5rem; transition: color 0.3s, transform 0.3s; }
        .social-sidebar a:hover { color: var(--text-primary); transform: translateX(5px); }
        .social-sidebar .whatsapp-icon { color: #25D366; }
        @media (max-width: 900px) { .social-sidebar { display: none; } }
"""
content = content.replace("/* Shared Section Styles */", sidebar_css + "\n        /* Shared Section Styles */")

sidebar_html = """
    <!-- Social Sidebar -->
    <div class="social-sidebar">
        <a href="https://wa.me/918799036132" target="_blank" title="WhatsApp Me" class="whatsapp-icon"><i class="ph ph-whatsapp-logo"></i></a>
        <a href="#"><i class="ph ph-linkedin-logo"></i></a>
        <a href="#"><i class="ph ph-github-logo"></i></a>
        <a href="#"><i class="ph ph-twitter-logo"></i></a>
    </div>

    <main>
"""
content = content.replace("<main>", sidebar_html)

content = content.replace("border: 1px dashed var(--border-subtle);", "border: 2px dashed #FF4500;")
content = content.replace("[ Drop 3D Image Here ]", "<span style='color: #FF4500;'>[ 3D IMAGE PLACEHOLDER HERE ]</span>")

with open("index.html", "w") as f:
    f.write(content)
