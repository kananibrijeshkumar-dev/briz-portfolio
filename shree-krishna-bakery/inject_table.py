import re

with open('menu_full.html', 'r') as f:
    lines = f.readlines()

table_html = "".join(lines[423:1322])

with open('menu.html', 'r') as f:
    menu_content = f.read()

# Replace the PDF section with the table
start_marker = "<!-- Menu PDF Embed -->"
end_marker = "</section>"

start_idx = menu_content.find(start_marker)
end_idx = menu_content.find(end_marker, start_idx) + len(end_marker)

new_section = f"""<!-- Menu Table -->
    <section class="menu-page-section" style="padding-top: 2rem; padding-bottom: 6rem; max-width: 1000px; margin: 0 auto;">
{table_html}
    </section>"""

new_content = menu_content[:start_idx] + new_section + menu_content[end_idx:]

with open('menu.html', 'w') as f:
    f.write(new_content)
