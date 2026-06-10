import re
import pandas as pd
import math

def is_nan(val):
    if isinstance(val, float) and math.isnan(val):
        return True
    if str(val).strip() == '' or str(val).lower() == 'nan':
        return True
    return False

def p_format(val):
    if is_nan(val): return '<span class="empty">—</span>'
    s = str(val).strip()
    if 'Seasonal' in s: return '<span>Seasonal</span>'
    # Format with ₹ if it contains a digit and doesn't already have one
    if any(c.isdigit() for c in s):
        # if it's like 80/pc
        parts = s.split(' ', 1)
        if len(parts) == 2:
            return f'<span>₹{parts[0]} <span class="item-tag">{parts[1]}</span></span>'
        else:
            if '/' in s:
                num, den = s.split('/', 1)
                return f'<span>₹{num}<span class="item-tag">/{den}</span></span>'
            return f'<span>₹{s}</span>'
    return f'<span>{s}</span>'

panels = []

# Mandi Panel
mandi_items = [
    ("Al-Faham Mandi", 209, 420, 800, ""),
    ("Peri Peri Mandi", 230, 449, 819, ""),
    ("Honey Mandi", 249, 459, 819, ""),
    ("Royal Special Mandi", None, 459, 899, ""),
    ("Mutton Mandi", None, 999, 1999, ""),
    ("Fish Mandi", None, None, 1999, ""),
    ("Dynamite Mandi", 259, 469, 849, ""),
    ("Prawns Mandi", None, None, 1099, ""),
    ("Broasted Mandi", 209, 519, 1099, ""),
    ("Extra Mandi Rice", 150, 250, 400, "")
]
panel = '            <!-- MANDI -->\n            <div class="menu-panel active" id="panel-mandi">\n                <div class="menu-price-header">\n                    <span>QTR</span>\n                    <span>HALF</span>\n                    <span>FULL</span>\n                </div>\n                <div class="menu-list">\n'
for name, q, h, f, n in mandi_items:
    tag = f' <span class="item-tag">({n})</span>' if n else ''
    panel += f'                    <div class="menu-row-multi">\n                        <span class="menu-item-name">{name}{tag}</span>\n                        <div class="price-cols">{p_format(q)}{p_format(h)}{p_format(f)}</div>\n                    </div>\n'
panel += '                </div>\n            </div>\n'
panels.append(panel)


# Biryani Panel
biryani_items = [
    ("Chicken Biryani", None, 130, 180, ""),
    ("Mutton Biryani", None, 190, 270, ""),
    ("Prawns Biryani", None, 140, 190, "Seasonal"),
    ("Egg Biryani", None, None, 140, ""),
    ("Paneer Biryani", None, None, 160, "")
]
panel = '            <!-- BIRYANI -->\n            <div class="menu-panel" id="panel-biryani">\n                <div class="menu-price-header">\n                    <span>HALF</span>\n                    <span>FULL</span>\n                </div>\n                <div class="menu-list">\n'
for name, q, h, f, n in biryani_items:
    tag = f' <span class="item-tag">({n})</span>' if n else ''
    panel += f'                    <div class="menu-row-multi">\n                        <span class="menu-item-name">{name}{tag}</span>\n                        <div class="price-cols">{p_format(h)}{p_format(f)}</div>\n                    </div>\n'
panel += '                </div>\n            </div>\n'
panels.append(panel)

# Starters Panel
starters_items = [
    ("Chicken 65", None, None, 220, ""),
    ("Chicken Tikka", 80, 300, 600, ""),
    ("Chicken Alfam", 110, 240, 460, ""),
    ("Chicken Broasted", "80/pc", 300, 600, "Pc pricing"),
    ("Chicken Lolly Pop", None, "180/pc", "340 (8 Pc)", "Pc pricing"),
    ("Crispy Chicken Wings", None, None, "150 (5 Pc)", ""),
    ("Chicken Popcorn", None, None, "130 (M)", "")
]
panel = '            <!-- STARTERS -->\n            <div class="menu-panel" id="panel-starters">\n                <div class="menu-price-header">\n                    <span>QTR</span>\n                    <span>HALF</span>\n                    <span>FULL</span>\n                </div>\n                <div class="menu-list">\n'
for name, q, h, f, n in starters_items:
    tag = f' <span class="item-tag">({n})</span>' if n else ''
    panel += f'                    <div class="menu-row-multi">\n                        <span class="menu-item-name">{name}{tag}</span>\n                        <div class="price-cols">{p_format(q)}{p_format(h)}{p_format(f)}</div>\n                    </div>\n'
panel += '                </div>\n            </div>\n'
panels.append(panel)


def gen_single(name, pid, items):
    p = f'            <!-- {name.upper()} -->\n            <div class="menu-panel" id="panel-{pid}">\n                <div class="menu-list">\n'
    for item_name, f, n in items:
        tag = f' <span class="item-tag">({n})</span>' if n else ''
        pr = 'Seasonal' if 'Seasonal' in str(n) or 'Seasonal' in str(f) else f'₹{f}'
        p += f'                    <div class="menu-row">\n                        <span class="menu-item-name">{item_name}{tag}</span>\n                        <span class="menu-item-price">{pr}</span>\n                    </div>\n'
    p += '                </div>\n            </div>\n'
    return p

veg = [("Paneer Chilly", 220, ""), ("Paneer Manchurian", 220, ""), ("Gobi Manchurian", 150, ""), ("Gobi Chilly", 170, ""), ("Dal Fry", 90, ""), ("Paneer Kadai", 220, ""), ("Paneer Butter Masala", 220, "")]
panels.append(gen_single("Veg", "veg", veg))

chinese = [("Chicken Chilly", 250, ""), ("Chicken Ghee Roast", 280, ""), ("Chicken Manchury", 250, ""), ("Chicken Pepper", 250, ""), ("Garlic Chicken", 250, ""), ("Chicken Kondattam", 250, ""), ("Mutton Chilly", 350, ""), ("Mutton Garlic", 350, ""), ("Mutton Manchury", 350, ""), ("Mutton Ghee Roast", 380, "")]
panels.append(gen_single("Chinese", "chinese", chinese))

noodles = [("Chicken Noodles", 170, ""), ("Egg Noodles", 140, ""), ("Mixed Noodles", 170, ""), ("Chicken Schezwan Noodles", 190, ""), ("Paneer Noodles", 160, ""), ("Veg Noodles", 110, "")]
panels.append(gen_single("Noodles", "noodles", noodles))

pizza = [("Crispy Chicken Pizza", 260, ""), ("BBQ Chicken Pizza", 250, ""), ("Tandoori Tikka Pizza", 280, ""), ("Veg Pizza", 220, "")]
panels.append(gen_single("Pizza", "pizza", pizza))

burger = [("Chicken Zinger Burger", 129, ""), ("Chicken Peri Peri Burger", 120, ""), ("Big Daddy Burger", 170, ""), ("No Bun Burger", 150, ""), ("Jumbo Burger", 180, "")]
panels.append(gen_single("Burger", "burger", burger))

soup = [("Chicken Manchous Soup", 100, ""), ("Chicken Hot & Sour Soup", 100, ""), ("Chicken Sweet Corn Soup", 120, ""), ("Mutton Manchous Soup", 130, ""), ("Mutton Hot & Sour Soup", 130, ""), ("Mutton Sweet Corn Soup", 150, ""), ("Veg Manchous Soup", 80, ""), ("Veg Hot & Sour Soup", 80, ""), ("Veg Sweet Corn Soup", 90, "")]
panels.append(gen_single("Soup", "soup", soup))

fish = [("Prawns Sukka", "Seasonal", "Seasonal"), ("Prawns Chilly", "Seasonal", "Seasonal"), ("Prawns Pepper", "Seasonal", "Seasonal"), ("Prawns Manchurian", "Seasonal", "Seasonal"), ("Prawns Tawa Fry", "Seasonal", "Seasonal"), ("Squid Chilly", "Seasonal", "Seasonal"), ("Squid Sukka", "Seasonal", "Seasonal"), ("Squid Manchurian", "Seasonal", "Seasonal"), ("Fish Chilly", "Seasonal", "Seasonal"), ("Fish Kabab", "Seasonal", "Seasonal")]
panels.append(gen_single("Fish", "fish", fish))

combos = [("2 Burger + 1 Pizza + 2 Broasted + 1 French Fries + 1 Dip Ketchup + 750ml Soft Drinks", 749, ""), ("Family Meal Combo - 2 Pc Broasted + 1 Kubbus + French Fries + Garlic Dip + 200ml Soft Drinks", 229, ""), ("Family Meal Combo - 4 Pc Broasted + 2 Kubbus + French Fries + 2 Garlic Dip + 750ml Soft Drinks", 399, ""), ("Family Meal Combo - 8 Pc Broasted + 4 Zinger Burger + 2 Crispy Chicken Pizza + 2 French Fries + 8 Kubbus + 4 Dip Garlic Ketchup + Chicken Popcorn + 750ml (2) Soft Drinks", 1999, ""), ("Family Meal Combo - 10 Pc Broasted + 5 Kubbus + French Fries + 4 Pc Garlic Dip + Ketchup + 750ml (2) Soft Drinks", 899, ""), ("Family Meal Combo - 15 Pc Broasted + 7 Kubbus + French Fries + 4 Dip Mayo + Ketchup + 750ml (3) Soft Drinks + Chicken Popcorn", 1499, "")]
panels.append(gen_single("Combos", "combos", combos))

kunafa = [("Classic Cream Kunafa", 350, ""), ("Cream Cheese Kunafa", 380, "")]
panels.append(gen_single("Kunafa", "kunafa", kunafa))

rotis = [("Porota", 15, ""), ("Chapati", 15, ""), ("Kubbus", 12, "")]
panels.append(gen_single("Rotis", "rotis", rotis))

full_html = """    <!-- Full Menu Tabbed Section -->
    <section class="full-menu" id="full-menu">
        <div class="menu-tabs-wrapper">
            <div class="section-header animate-on-scroll">
                <div class="section-eyebrow">OUR COMPLETE MENU</div>
                <h2 class="section-heading">Royal Mandi House Menu</h2>
            </div>

            <div class="menu-tabs" id="menu-tabs">
                <button class="menu-tab active" data-tab="mandi">Mandi</button>
                <button class="menu-tab" data-tab="biryani">Biryani</button>
                <button class="menu-tab" data-tab="starters">Starters</button>
                <button class="menu-tab" data-tab="veg">Veg</button>
                <button class="menu-tab" data-tab="chinese">Chinese</button>
                <button class="menu-tab" data-tab="noodles">Noodles</button>
                <button class="menu-tab" data-tab="pizza">Pizza</button>
                <button class="menu-tab" data-tab="burger">Burger</button>
                <button class="menu-tab" data-tab="soup">Soup</button>
                <button class="menu-tab" data-tab="fish">Fish</button>
                <button class="menu-tab" data-tab="combos">Combos</button>
                <button class="menu-tab" data-tab="kunafa">Kunafa</button>
                <button class="menu-tab" data-tab="rotis">Rotis</button>
                <div class="tab-indicator" id="tab-indicator"></div>
            </div>

"""

for p in panels:
    full_html += p + '\n'

full_html += """        </div>
    </section>"""

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the block
pattern = re.compile(r'<!-- Full Menu Tabbed Section -->.*?</section>', re.DOTALL)
new_content = pattern.sub(full_html, content, count=1)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Menu updated successfully.")
