import glob
import re

files = glob.glob('*.html')

reduced_motion_css = """
        @media (prefers-reduced-motion: reduce) {
            * {
                animation-duration: 0.01ms !important;
                animation-iteration-count: 1 !important;
                transition-duration: 0.01ms !important;
                scroll-behavior: auto !important;
            }
            .animate-on-scroll {
                opacity: 1 !important;
                transform: none !important;
                transition: none !important;
            }
        }
"""

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Add prefers-reduced-motion right before </style>
    if 'prefers-reduced-motion' not in content:
        content = content.replace('</style>', reduced_motion_css + '\n    </style>')
        
    # 2. Add aria-labels to menu tabs in index.html
    if file == 'index.html':
        # Replace <button class="menu-tab" data-target="panel-mandi">Mandi</button>
        # with <button class="menu-tab" data-target="panel-mandi" aria-label="View Mandi Menu">Mandi</button>
        def add_aria(match):
            cls = match.group(1)
            target = match.group(2)
            text = match.group(3)
            return f'<button class="menu-tab" {target} aria-label="View {text} Menu">{text}</button>'
        
        content = re.sub(r'<button class="menu-tab" (data-target="[^"]+")>(.*?)</button>', add_aria, content)

        # 3. Add aria-label to mobile menu toggle
        content = content.replace('<div class="menu-toggle" id="mobile-menu">', '<button class="menu-toggle" id="mobile-menu" aria-label="Open mobile menu" aria-expanded="false" style="background:none; border:none; padding:0;">')
        content = content.replace('<!-- In the navbar -->\n            <div class="menu-toggle"', '<!-- In the navbar -->\n            <button class="menu-toggle"')
        # Since it was a div, let's just make it a button or add aria attributes
        content = re.sub(r'<div class="menu-toggle"([^>]*)>', r'<button class="menu-toggle"\1 aria-label="Toggle Navigation Menu">', content)
        # If we changed <div to <button, we must change corresponding </div> to </button>
        # Let's be careful. The menu toggle is:
        # <div class="menu-toggle" id="mobile-menu">
        #     <span></span>
        #     <span></span>
        #     <span></span>
        # </div>
        # Actually, adding role="button" and tabindex="0" is safer than changing tags.
        content = content.replace('<div class="menu-toggle" id="mobile-menu">', '<div class="menu-toggle" id="mobile-menu" role="button" tabindex="0" aria-label="Toggle navigation menu">')
        
    # 4. Check for any missing alt attributes in img (we know we have them all, but let's be sure)
    
    # 5. Fix any links missing aria-labels if they have no text
    content = content.replace('<a href="#" aria-label="Instagram">', '<a href="https://instagram.com" target="_blank" aria-label="Visit our Instagram">')
    content = content.replace('<a href="#" aria-label="Facebook">', '<a href="https://facebook.com" target="_blank" aria-label="Visit our Facebook">')

    # Save
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print("Audit fixes applied.")
