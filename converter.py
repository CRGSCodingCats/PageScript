# converter.py

import re
import sys

def parse_pagescript(pagescript):
    html = []
    lines = pagescript.strip().split('\n')

    for line in lines:
        line = line.strip()

        if not line:
            continue
        elif line.startswith('#'):
            html.append(f"<h1>{line[1:].strip()}</h1>")
        elif line == '---':
            html.append("<hr>")
        elif line.startswith('[image:'):
            src = re.findall(r'''

\[image:\s*(.*?)\]

''', line)
            if src:
                html.append(f'<img src="{src[0]}" alt="Image">')
        elif line.startswith('[button:'):
            match = re.match(r'''

\[button:\s*(.*?)\s*>\s*(.*?)\]

''', line)
            if match:
                text, link = match.groups()
                html.append(f'<a href="{link}"><button>{text}</button></a>')
        elif line.startswith('[link:'):
            match = re.match(r'''

\[link:\s*(.*?)\s*>\s*(.*?)\]

''', line)
            if match:
                text, url = match.groups()
                html.append(f'<a href="{url}">{text}</a>')
        else:
            line = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', line)
            line = re.sub(r'\*(.*?)\*', r'<em>\1</em>', line)
            html.append(f"<p>{line}</p>")

    return '\n'.join(html)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python converter.py your_file.pagescript")
        sys.exit(1)

    input_path = sys.argv[1]

    try:
        with open(input_path, 'r', encoding='utf-8') as file:
            content = file.read()
        output = parse_pagescript(content)
        output_filename = input_path.rsplit('.', 1)[0] + '.html'
        with open(output_filename, 'w', encoding='utf-8') as file:
            file.write(output)
        print(f"Converted '{input_path}' → '{output_filename}'")
    except FileNotFoundError:
        print(f"File '{input_path}' not found.")
