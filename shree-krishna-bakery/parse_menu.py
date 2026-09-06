import sys
from bs4 import BeautifulSoup

def parse_and_generate():
    with open('menu_full.html', 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table')
    if not table:
        print("Table not found!")
        return

    categories = []
    current_category = None

    for tr in table.find_all('tr'):
        # Check if it's a category header (uses th instead of td)
        ths = tr.find_all('th')
        if len(ths) == 1 and 'colspan' in ths[0].attrs:
            cat_name = ths[0].get_text(strip=True)
            current_category = {'name': cat_name, 'items': []}
            categories.append(current_category)
            continue
            
        tds = tr.find_all('td')
        if not tds:
            continue
        
        # Check if it's an item row (usually 4 columns: No, Name, Weight, Price)
        if len(tds) == 4 and current_category is not None:
            no = tds[0].get_text(strip=True)
            name = tds[1].get_text(strip=True)
            weight = tds[2].get_text(strip=True)
            price = tds[3].get_text(strip=True)
            if name: # skip empty rows
                current_category['items'].append({
                    'name': name,
                    'weight': weight,
                    'price': price
                })

    # Generate new HTML
    out_html = '<div class="premium-menu-container">\n'
    
    for cat in categories:
        if not cat['items']:
            continue
            
        out_html += f'  <div class="menu-category">\n'
        out_html += f'    <h3 class="menu-category-title"><span>{cat["name"]}</span></h3>\n'
        out_html += f'    <div class="menu-items-grid">\n'
        
        for item in cat['items']:
            # Format price nicely
            price_display = item['price'].replace(' /-', '') if item['price'] else ''
            weight_display = f"({item['weight']})" if item['weight'] and item['weight'] != '-' else ''
            
            out_html += f'      <div class="menu-item">\n'
            out_html += f'        <div class="menu-item-header">\n'
            out_html += f'          <span class="menu-item-name">{item["name"]} {weight_display}</span>\n'
            out_html += f'          <span class="menu-item-dots"></span>\n'
            out_html += f'          <span class="menu-item-price">₹{price_display}</span>\n'
            out_html += f'        </div>\n'
            out_html += f'      </div>\n'
            
        out_html += f'    </div>\n'
        out_html += f'  </div>\n'
        
    out_html += '</div>\n'

    # Inject into menu.html
    with open('menu.html', 'r', encoding='utf-8') as f:
        menu_content = f.read()
        
    start_marker = "<!-- Premium Menu Section -->"
    end_marker = "</section>"

    start_idx = menu_content.find(start_marker)
    end_idx = menu_content.find(end_marker, start_idx) + len(end_marker)

    if start_idx == -1 or end_idx < len(end_marker):
        print("Markers not found in menu.html")
        return

    new_section = f"""<!-- Premium Menu Section -->
    <section class="menu-page-section" style="padding-top: 2rem; padding-bottom: 6rem; max-width: 1200px; margin: 0 auto;">
{out_html}
    </section>"""

    new_content = menu_content[:start_idx] + new_section + menu_content[end_idx:]

    with open('menu.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
        
    print(f"Successfully injected {len(categories)} categories into menu.html")

if __name__ == "__main__":
    parse_and_generate()
