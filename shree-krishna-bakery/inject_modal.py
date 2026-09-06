import os

pages = ['index.html', 'about-us.html', 'menu.html', 'franchise.html', 'contact-us.html']

header_target = '<a href="contact-us.html" class="cta-btn">Order Now</a>'
header_replacement = """<div class="header-actions">
            <button class="user-icon-btn" id="open-login-btn"><i class="ph-fill ph-user"></i></button>
            <a href="contact-us.html" class="cta-btn">Order Now</a>
        </div>"""

modal_html = """
    <!-- Login / Register Modal -->
    <div class="login-modal-overlay" id="login-modal">
        <div class="login-modal-box">
            <button class="login-modal-close" id="close-login-btn">&times;</button>
            <div class="login-modal-logo">
                <img src="assets/images/logo.png" alt="Shree Krishna Bakery">
            </div>
            <div class="login-modal-tabs">
                <div class="login-modal-tab active">LOGIN</div>
                <div class="login-modal-tab">REGISTER</div>
            </div>
            <form id="login-form">
                <div class="login-form-group">
                    <label>Username or email address *</label>
                    <input type="text" placeholder="Enter your username" required>
                </div>
                <div class="login-form-group">
                    <label>Password *</label>
                    <input type="password" placeholder="Enter your password" required>
                </div>
                <div class="login-form-options">
                    <label><input type="checkbox" style="margin-right: 5px;"> Remember me</label>
                    <a href="#">Lost your password?</a>
                </div>
                <button type="submit" class="login-submit-btn">Log in</button>
            </form>
        </div>
    </div>
"""

script_html = """
        // Login Modal Logic
        const loginModal = document.getElementById('login-modal');
        const openLoginBtn = document.getElementById('open-login-btn');
        const closeLoginBtn = document.getElementById('close-login-btn');

        if (openLoginBtn && closeLoginBtn && loginModal) {
            openLoginBtn.addEventListener('click', (e) => {
                e.preventDefault();
                loginModal.classList.add('active');
                document.body.style.overflow = 'hidden';
            });

            closeLoginBtn.addEventListener('click', () => {
                loginModal.classList.remove('active');
                document.body.style.overflow = 'auto';
            });
        }
"""

for page in pages:
    if not os.path.exists(page):
        continue
        
    with open(page, 'r') as f:
        content = f.read()
        
    # Replace header action
    if header_target in content:
        content = content.replace(header_target, header_replacement)
        
    # Inject Modal before body end
    if '<!-- Login / Register Modal -->' not in content:
        body_end_idx = content.find('</body>')
        if body_end_idx != -1:
            content = content[:body_end_idx] + modal_html + '\n' + content[body_end_idx:]
            
    # Inject script if missing
    if 'loginModal.classList.add' not in content:
        script_idx = content.find('// Scroll Effect on Nav')
        if script_idx != -1:
            content = content[:script_idx] + script_html + '\n' + content[script_idx:]
        else:
            # If no script tag exists, find closing body and add one
            body_end_idx = content.find('</body>')
            script_block = f"""
    <script>
{script_html}
    </script>
"""
            content = content[:body_end_idx] + script_block + content[body_end_idx:]
            
    with open(page, 'w') as f:
        f.write(content)
        
print("Successfully injected login modal into all pages.")
