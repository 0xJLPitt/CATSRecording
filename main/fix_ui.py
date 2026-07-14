import re
import os

def scale_ui_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'from app_config import CONFIG' not in content:
        if 'from PyQt5 import' in content:
            content = content.replace('from PyQt5 import', 'from app_config import CONFIG\nfrom PyQt5 import', 1)
        else:
            content = 'from app_config import CONFIG\n' + content

    def repl_font(m):
        val = int(m.group(1)) * 2
        # Turn "font-size: 22px; color: yellow;" into f"font-size: {int(44 * CONFIG['ui_scale'])}px; color: yellow;"
        # Wait, the match might include color and other things. Let's just find "font-size: 22px" and replace it.
        # Actually, in ui_frontend, I have string literals like: "font-size: 22px; color: yellow;"
        return m.group(0).replace(m.group(1), f"{{int({val} * CONFIG['ui_scale'])}}")
        
    def repl_str(m):
        # Add f prefix to strings that match the pattern
        s = m.group(0)
        # Check if it already has f
        if s.startswith('f"'): return s
        if 'font-size' in s and 'px' in s:
            s = 'f' + s
            # Now replace the value inside the string
            s = re.sub(r'font-size:\s*(\d+)px', repl_font, s)
        return s

    content = re.sub(r'\"font-size:\s*\d+px[^\"]*\"', repl_str, content)
    
    def repl_size(m):
        func_name = m.group(0).split('(')[0]
        w = int(m.group(1)) * 2
        h = int(m.group(2)) * 2
        return f"{func_name}(int({w} * CONFIG['ui_scale']), int({h} * CONFIG['ui_scale']))"

    content = re.sub(r'setFixedSize\((\d+),\s*(\d+)\)', repl_size, content)
    content = re.sub(r'setMinimumSize\((\d+),\s*(\d+)\)', repl_size, content)
    content = re.sub(r'QSize\((\d+),\s*(\d+)\)', repl_size, content)

    def repl_pt(m):
        val = int(m.group(1)) * 2
        return f"setPointSize(int({val} * CONFIG['ui_scale']))"

    content = re.sub(r'setPointSize\((\d+)\)', repl_pt, content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

scale_ui_file('C:/Users/User/CATSRecording/main/ui.py')
scale_ui_file('C:/Users/User/CATSRecording/main/ui_frontend.py')
print('UI scaling variables injected.')
