import glob
import re

html_files = glob.glob("*.html")

for file in html_files:
    with open(file, 'r') as f:
        content = f.read()

    # 1. Upgrade Navbar CSS
    # Find the block starting with /* Navbar */ and ending before /* Buttons */
    nav_pattern = re.compile(r'/\*\s*Navbar\s*\*/.*?/\*\s*Buttons\s*\*/', re.DOTALL)
    
    premium_nav = """/* Premium Navbar */
        nav {
            position: fixed; top: 0; width: 100%; z-index: 100;
            background: rgba(10, 10, 10, 0.65);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-bottom: 1px solid rgba(255, 69, 0, 0.2);
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5), 0 1px 15px rgba(255, 69, 0, 0.15);
            padding: 1.25rem 0;
            transition: all 0.3s ease;
        }
        .nav-inner { display: flex; justify-content: space-between; align-items: center; }
        .logo { font-size: 1.6rem; font-weight: 800; letter-spacing: 2px; color: #fff; text-decoration: none; display: flex; align-items: center; gap: 0.5rem; text-transform: uppercase; }
        .logo span.text-primary { 
            background: linear-gradient(135deg, #FF4500, #FFA500); 
            -webkit-background-clip: text; 
            -webkit-text-fill-color: transparent; 
            text-shadow: 0 0 20px rgba(255,69,0,0.5);
        }
        .nav-links { display: flex; gap: 2.5rem; list-style: none; }
        .nav-links a { color: var(--text-muted); text-decoration: none; font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 2px; transition: all 0.3s ease; position: relative; }
        .nav-links a::after {
            content: ''; position: absolute; width: 0; height: 2px; bottom: -5px; left: 0;
            background: var(--primary); transition: width 0.3s ease;
            box-shadow: 0 0 10px var(--primary);
        }
        .nav-links a:hover, .nav-links a.active { color: #fff; text-shadow: 0 0 10px rgba(255,255,255,0.5); }
        .nav-links a:hover::after, .nav-links a.active::after { width: 100%; }

        /* Buttons */"""
    
    content = nav_pattern.sub(premium_nav, content)

    # 2. Upgrade Footer CSS
    # Find the footer line: footer { padding: 2rem 0; text-align: center; border-top: 1px solid var(--border-glass); color: var(--text-muted); background: rgba(0,0,0,0.8); backdrop-filter: blur(10px); }
    footer_pattern = re.compile(r'footer\s*{\s*padding.*?backdrop-filter: blur\(10px\);\s*}', re.DOTALL)
    
    premium_footer = """/* Premium Footer */
        footer { 
            padding: 3rem 0; text-align: center; 
            border-top: 1px solid rgba(255, 69, 0, 0.2); 
            color: var(--text-muted); 
            background: linear-gradient(180deg, rgba(15,15,15,0.8) 0%, rgba(0,0,0,1) 100%); 
            backdrop-filter: blur(20px); 
            position: relative;
            overflow: hidden;
        }
        footer::before {
            content: ''; position: absolute; top: 0; left: 50%; transform: translateX(-50%);
            width: 50%; height: 1px; background: linear-gradient(90deg, transparent, var(--primary), transparent);
            box-shadow: 0 0 20px var(--primary);
        }"""
    
    content = footer_pattern.sub(premium_footer, content)

    with open(file, 'w') as f:
        f.write(content)

print("Premium header/footer upgrade applied to all files!")
